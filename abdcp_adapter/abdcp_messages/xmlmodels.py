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

    @classmethod
    def abdcp_date_as_datetime(cls, value):
        value = datetime.datetime.strptime(value,'%Y%m%d%H%M%S')
        value = value.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return value

    def get_message_creation_date_as_datetime(self):
        value = self.message_creation_date
        return ABDCP_XML_Message.abdcp_date_as_datetime(value)

    def get_process_type(self):
        try:
            return constants.ABDCP_MESSAGE_TO_PROCESS_MAP[self.message_type]
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

# ECCP - Consulta Previa Envio Cedente
class ECPC_ABDCP_XML_Message(ABDCP_XML_Message):

    fecha_referencia_abdcp = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/FechaReferenciaABDCP"
    )
    
    numeracion = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/Numeracion"
    )
    
    codigo_receptor = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/CodigoReceptor"
    )
    
    codigo_cedente = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/CodigoCedente"
    )
    
    tipo_documento_identidad = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/TipoDocumentoIdentidad"
    )
    
    numero_documento_identidad = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/NumeroDocumentoIdentidad"
    )
    
    tipo_portabilidad = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/TipoPortabilidad"
    )
    
    nombre_contacto = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/NombreContacto"
    )
    
    email_contacto = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/EmailContacto"
    )
    
    telefono_contacto = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/TelefonoContacto"
    )
    
    fax_contacto = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/FaxContacto"
    )
    
    tipo_servicio = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/TipoServicio"
    )
    
    cliente = xmlmodels.XPathTextField(
        "//CuerpoMensaje/ConsultaPreviaEnvioCedente/Cliente"
    )
    
# ESC - Envio Solicitud Cedente
class ESC_ABDCP_XML_Message(ABDCP_XML_Message):

    fecha_referencia = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/FechaReferenciaABDCP'
    )

    numeracion = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/Numeracion'
    )

    codigo_receptor = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/CodigoReceptor'
    )

    codigo_cedente = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/CodigoCedente'
    )

    tipo_documento_identidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/TipoDocumentoIdentidad'
    )
    
    numero_documento_identidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/NumeroDocumentoIdentidad'
    )

    tipo_portabilidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/TipoPortabilidad'
    )

    nombre_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/NombreContacto'
    )

    email_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/EmailContacto'
    )

    telefono_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/TelefonoContacto'
    )

    fax_contacto = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/FaxContacto'
    )

    tipo_servicio = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/TipoServicio'
    )

    cliente = xmlmodels.XPathTextField(
        '//CuerpoMensaje/EnvioSolicitudCedente/Cliente'
    )

    def get_abdcp_reference_date_as_datetime(self):
        value = self.fecha_referencia
        return ABDCP_XML_Message.abdcp_date_as_datetime(value)



# PEP - Programacion de Ejecucion Portabilidad
class PEP_ABDCP_XML_Message(ABDCP_XML_Message):
    fecha_ejecucion_portabilidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/ProgramadaEjecutarPortabilidad/FechaEjecucionPortabilidad'
    )

    def get_scheduling_for_port_date_as_datetime(self):
        value = self.fecha_ejecucion_portabilidad
        return ABDCP_XML_Message.abdcp_date_as_datetime(value)

# SPR - Solicitud Procedente
class SPR_ABDCP_XML_Message(ABDCP_XML_Message):

    fecha_limite_programacion_portabilidad = xmlmodels.XPathTextField(
        '//CuerpoMensaje/SolicitudProcedente/FechaLimiteProgramacionPortabilidad'
    )

    fecha_referencia_abdcp = xmlmodels.XPathTextField(
        '//CuerpoMensaje/SolicitudProcedente/FechaReferenciaABDCP'
    )
