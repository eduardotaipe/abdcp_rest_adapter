# -*- coding: utf-8 -*-

import datetime
import pytz

from django.conf import settings
from djxml import xmlmodels
from operators.models import Operator
from abdcp_messages.models import ABDCPMessage
from abdcp_messages import constants

class ABDCP_XML_Message(xmlmodels.XmlModel):

    message_id = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/IdentificadorMensaje'
    )

    sender = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/Remitente'
    )

    recipient = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/Destinatario'
    )

    message_creation_date = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/FechaCreacionMensaje'
    )

    transaction_id = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/IdentificadorProceso'
    )

    message_type = xmlmodels.XPathTextField(
        '//MensajeABDCP/CuerpoMensaje/@IdMensaje'
    )

    def get_sender_as_operator(self):
        try:
            return Operator.objects.get(code=self.sender)
        except Operator.DoesNotExist:
            return None

    def get_recipient_as_operator(self):
        try:
            return Operator.objects.get(code=self.recipient)
        except Operator.DoesNotExist:
            return None

    def get_message_as_model(self):
        try:
            return ABDCPMessage.objects.get(message_id=self.message_id)
        except ABDCPMessage.DoesNotExist:
            return None

    def get_message_creation_date_as_datetime(self):
        src = self.message_creation_date
        value = datetime.datetime.strptime(src,'%Y%m%d%H%M%S')
        value = value.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return value

    def get_process_type(self):
        try:
            constants.ABDCP_MESSAGE_TO_PROCESS_MAP[self.message_type]
        except KeyError:
            return None


# CP - Consulta Previa

class CP_ABDCP_XML_Message(ABDCP_XML_Message):

    codigo_receptor = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/CodigoReceptor'
    )

    codigo_cedente = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/CodigoCedente'
    )

    tipo_documento_identidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/TipoDocumentoIdentidad'
    )
    
    numero_documento_identidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/NumeroDocumentoIdentidad'
    )

    cantidad_numeraciones = xmlmodels.XPathIntegerField(
        '//CuerpoMensaje/ConsultaPrevia/CantidadNumeraciones'
    )

    inicio_rango = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/NumeracionSolicitada'
        '/RangoNumeracion/InicioRango'
    )

    final_rango = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/NumeracionSolicitada'
        '/RangoNumeracion/FinalRango'
    )

    tipo_portabilidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/NumeracionSolicitada'
        '/RangoNumeracion/TipoPortabilidad'
    )

    nombre_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/NombreContacto'
    )

    email_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/EmailContacto'
    )

    telefono_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/TelefonoContacto'
    )

    fax_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/FaxContacto'
    )

    tipo_servicio = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/TipoServicio'
    )

    cliente = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ConsultaPrevia/Cliente'
    )
