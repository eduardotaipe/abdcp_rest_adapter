# -*- coding: utf-8 -*-

import xmldict
import xmltodict

from easyxsd import xsd_from_file
from easyxsd import xml_from_string
from easyxsd import xsd_error_log_as_simple_strings
from easyxsd import validate

from abdcp_messages import constants
from abdcp_messages import settings as abdcp_messages_settings
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ABDCP_XML_Message

def abdcp_validate_xml_message(xmlstr):
    xml = xml_from_string(xmlstr)
    xsd = xsd_from_file(abdcp_messages_settings.ABDCP_MESSAGE_XSD_FILEPATH)
    # Some of the files is not valid XML
    if xml is None or xsd is None:
        return (False, [], )
    # Performing the actual validation
    is_valid = validate(xml, xsd)
    errors = xsd_error_log_as_simple_strings(xsd.error_log)
    return (is_valid, errors, )


def create_abdcp_message_from_xml_string(xmlstr, commit=True):
    xmlmodel = ABDCP_XML_Message.create_from_string(xmlstr)
    message = ABDCPMessage(
        message_id=xmlmodel.message_id,
        sender=xmlmodel.get_sender_as_operator(),
        recipient=xmlmodel.get_recipient_as_operator(),
        transaction_id=xmlmodel.transaction_id,
        stated_creation=xmlmodel.get_message_creation_date_as_datetime(),
        message_type=xmlmodel.message_type,
        process_type=xmlmodel.get_process_type(),
        request_document=xmlstr
    )
    if commit:
        message.save()
    return message


def process_type_from_message_type(message_type):
    try:
        constants.ABDCP_MESSAGE_TO_PROCESS_MAP[message_type]
    except KeyError:
        return None


def xmlstr_to_dict(xmlstr):
    """
    Converts an XML string into a Python dictionary using the
    'xmltodict' module
    """
    return xmltodict.parse(str(xmlstr))


def dict_to_xmlstr(value):
    """
    Converts a Python dictionary into an XML string using the 
    'xmldict' module
    """
    return xmldict.dict_to_xml(value)


def beautify_xmlstr(xmlstr):
    """
    Beautifies string containing a valid XML document
    """
    from lxml import etree
    root = etree.XML(xmlstr.strip())
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').strip()


def pretty_print_xmlstr(xmlstr):
    """
    Pretty-prints a string containing a valid XML document
    """
    print beautify_xmlstr(xmlstr)
