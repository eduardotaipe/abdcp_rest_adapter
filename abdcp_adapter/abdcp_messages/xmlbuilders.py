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

        message_head = self['MensajeABDCP']['CabeceraMensaje']
        message_body =  self['MensajeABDCP']['CuerpoMensaje']

        message_head['@IdMensaje'] = message_type
        message_head['IdentificadorMensaje'] = message_id
        message_head['Remitente'] = sender_code
        message_head['Destinatario'] = recipient_code
        message_head['IdentificadorProceso'] = process_id
        message_head['FechaCreacionMensaje'] = self.format_date(
            stated_creation
        )


    def format_date(self, dt):
        fmtstr = '%Y%m%d%H%M%S'
        return time.strftime(fmtstr, dt.timetuple())
