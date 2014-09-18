# -*- coding: utf-8 -*-

import json
import base64

from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError

from django.db.utils import OperationalError
from django.db.utils import IntegrityError

from django_restful.http import HttpResponseConflict
from django_restful.http import HttpResponseNoContent
from django_restful.views import ControllerResourceView
from django_restful.utils import json_error_document

from abdcp_adapter.auth import abdcp_check_credentials

from abdcp_messages.xmlmodels import ABDCP_XML_Message
from abdcp_messages.models import ABDCPMessage
from abdcp_messages import strings
from abdcp_messages import utils

from abdcp_processes.tasks import process_message

class ABDCPMessageCreation(ControllerResourceView):

    def get_document(self):
        return getattr(self, 'doc', None)


    def check_request_content_type(self):
        content_type = self.request.META.get('CONTENT_TYPE', None)
        return content_type == 'application/json'


    def parse_request_body(self):
        try:
            self.doc = json.loads(self.request.body)
            return True
        except ValueError:
            return False


    def check_request_document_structure(self):
        doc = self.get_document()
        if doc is not None:
            REQUIRED_KEYS = ['userID', 'password', 'xmlMsg']
            for k in REQUIRED_KEYS:
                if k not in self.doc:
                    return False
            # All keys are present
            return True
        else:
            # No document present
            return False


    def get_username(self):
        doc = self.get_document()
        if doc is not None:
            return doc.get('userID', None)
        else:
            return None


    def decode_password(self):
        doc = self.get_document()
        if doc is not None and 'password' in doc:
            try:
                return base64.b64decode(doc['password'])
            except TypeError:
                pass
        # Something went wrong
        return None


    def not_empty_credentials(self, username, password):
        username = username if username is not None else ''
        password = password if password is not None else ''
        return len(username)> 0 and len(password)>0


    def check_credentials(self):
        username = self.get_username()
        password = self.decode_password()
        if self.not_empty_credentials(username, password):
            return abdcp_check_credentials(username, password)
        else:
            return False


    def get_xml_message(self):
        doc = self.get_document()
        if doc is not None and 'xmlMsg' in doc:
            return doc['xmlMsg']
        else:
            return None


    def get_xml_model(self):
        xml = self.get_xml_message()
        if xml is not None:
            return ABDCP_XML_Message.create_from_string(xml)
        else:
            return None


    def check_xml_document(self):
        xmlstr = self.get_xml_message()
        if xmlstr is not None:
            (self.xml_is_valid, self.xml_errors) = \
                utils.abdcp_validate_xml_message(xmlstr)
            return self.xml_is_valid
        else:
            return None


    def get_xml_errors(self, as_unicode=True):
        errors = getattr(self, 'xml_errors', [])
        if as_unicode:
            return [unicode(e) for e in errors]
        else:
            return errors


    def check_duplicated_message(self):
        xmlmodel = self.get_xml_model()
        if xmlmodel is not None:
            self.message_id = xmlmodel.message_id
            return ABDCPMessage.is_duplicated(self.message_id)
        else:
            return None


    def create_message(self):
        xmlstr = self.get_xml_message()
        try:
            obj = utils.create_abdcp_message_from_xml_string(xmlstr)
            return True
        except (OperationalError, IntegrityError) as e:
            print e
            self.message_creation_errors = [e]
            return False


    def get_message_creation_errors(self, as_unicode=True):
        errors = getattr(self, 'message_creation_errors', [])
        if as_unicode:
            return [unicode(e) for e in errors]
        else:
            return errors

    def bad_request(self, error_messages):
        response = HttpResponseBadRequest(json_error_document(error_messages))
        response['Content-Type'] = 'application/json'
        return response


    def forbidden(self, error_messages):
        response = HttpResponseForbidden(json_error_document(error_messages))
        response['Content-Type'] = 'application/json'
        return response


    def conflict(self, error_messages):
        response = HttpResponseConflict(json_error_document(error_messages))
        response['Content-Type'] = 'application/json'
        return response


    def server_error(self, error_messages):
        response = HttpResponseServerError(json_error_document(error_messages))
        response['Content-Type'] = 'application/json'
        return response


    def no_content(self):
        return HttpResponseNoContent()


    def run(self, request):
        # Checking the proper content type
        if not self.check_request_content_type():
            error_messages = [
                unicode(strings.JSON_REQUIRED_RESTFUL_API_ERROR)
            ]
            return self.bad_request(error_messages)
        # Parsing the body
        if not self.parse_request_body():
            error_messages = [
                unicode(strings.INVALID_JSON_RESTFUL_API_ERROR)
            ]
            return self.bad_request(error_messages)
        # Checking document structure
        if not self.check_request_document_structure():
            error_messages = [
                unicode(strings.UNEXPECTED_STRUCTURE_RESTFUL_API_ERROR)
            ]
            return self.bad_request(error_messages)
        # Checking credentials
        if not self.check_credentials():
            error_messages = [
                unicode(strings.INVALID_CREDENTIALS_RESTFUL_API_ERROR)
            ]
            return self.forbidden(error_messages)
        # Validating the XML document structure
        if not self.check_xml_document():
            error_messages = [
                unicode(strings.INVALID_XML_DOCUMENT_RESTFUL_API_ERROR)
            ]
            error_messages += self.get_xml_errors()
            return self.bad_request(error_messages)
        # Check for a duplicated message
        if self.check_duplicated_message():
            msg = strings.DUPLICATED_MESSAGE_RESTFUL_API_ERROR % {
                'message_id': self.message_id
            }
            error_messages = [unicode(msg)]
            return self.conflict(error_messages)
        # Everything seems to be OK, lets create the message
        if self.create_message():
            # Message created
            process_message.delay(self.message_id)
            return self.no_content()
        else:
            # Some sort of error has happened
            msg = strings.MESSAGE_NOT_CREATED_RESTFUL_API_ERROR % {
                'message_id': self.message_id
            }
            error_messages = [unicode(msg)]
            error_messages += self.get_message_creation_errors()
            return self.server_error(error_messages)
