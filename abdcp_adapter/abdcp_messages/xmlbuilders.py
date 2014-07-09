# -*- coding: utf-8 -*-

import time
import datetime

from collections import OrderedDict
from abdcp_messages import utils

class BaseXMLBuilder(OrderedDict):

    def __init__(self):
        super(BaseXMLBuilder, self).__init__()


    def as_xml(self, pretty_print=True):
        xmlstr = utils.dict_to_xmlstr(self)
        if pretty_print:
            xmlstr = utils.beautify_xmlstr(xmlstr)
        return xmlstr


    def as_xml_root_element(self):
        from lxml import etree
        return etree.XML(self.as_xml())


class ABDCPXMLBuilder(BaseXMLBuilder):

    def __init__(self, **params):
        super(ABDCPXMLBuilder, self).__init__()
        
        message_type = params.get('message_type')
        message_id = params.get('message_id')
        process_id = params.get('process_id')
        sender_code = params.get('sender_code')
        recipient_code = params.get('recipient_code')

        stated_creation = params.get(
            'stated_creation',
            datetime.datetime.now()
        )

        self['MensajeABDCP'] = OrderedDict()
        self['MensajeABDCP']['CabeceraMensaje'] = OrderedDict()
        self['MensajeABDCP']['CuerpoMensaje'] = OrderedDict()

        message_head = self.get_message_head()
        message_body = self.get_message_body()

        message_body['@IdMensaje'] = message_type
        message_head['IdentificadorMensaje'] = message_id
        message_head['Remitente'] = sender_code
        message_head['Destinatario'] = recipient_code
        message_head['IdentificadorProceso'] = process_id
        message_head['FechaCreacionMensaje'] = self.format_date(
            stated_creation
        )

        self.build_payload()


    def get_message_head(self):
        return self['MensajeABDCP']['CabeceraMensaje']


    def get_message_body(self):
        return self['MensajeABDCP']['CuerpoMensaje']


    def build_payload(self, value=OrderedDict()):
        message_body = self.get_message_body()
        if hasattr(self, 'payload_name'):
            message_body[self.payload_name] = value


    def get_payload_name(self):
        return getattr(self, 'payload_name', None)


    def get_payload(self):
        payload_name = self.get_payload_name()
        message_body = self.get_message_body()
        if payload_name is not None:
            return message_body.get(payload_name, None)
        else:
            return None


    def format_date(self, dt):
        fmtstr = '%Y%m%d%H%M%S'
        return time.strftime(fmtstr, dt.timetuple())


class CPAC_XMLBuilder(ABDCPXMLBuilder):

    payload_name = 'ConsultaPreviaAceptadaCedente'

    def __init__(self, **params):

        params['message_type'] = 'CPAC'

        super(CPAC_XMLBuilder, self).__init__(**params)
        
        numeracion = params.get('numeracion')
        observaciones = params.get('observaciones')

        payload = self.get_payload()

        if payload is not None:
            payload['numeracion'] = numeracion
            payload['observaciones'] = observaciones
