# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

# ABDCP Messages

ABDCP_MESSAGE_MESSAGE_ID = _(u'ID de mensaje')
ABDCP_MESSAGE_SENDER = _(u'Solicitante')
ABDCP_MESSAGE_RECIPIENT = _(u'Receptor')
ABDCP_MESSAGE_TRANSACTION_ID = _(u'ID de transacción')
ABDCP_MESSAGE_REQUEST_DOCUMENT = _(u'Documento con solicitud')
ABDCP_MESSAGE_RESPONSE_DOCUMENT = _(u'Documento con respuesta')
ABDCP_MESSAGE_PROCESS_TYPE = _(u'Tipo de proceso')
ABDCP_MESSAGE_MESSAGE_TYPE = _(u'Tipo de Mensaje')
ABDCP_MESSAGE_STATED_CREATION = _(u'Fecha y hora de creación indicada')
ABDCP_MESSAGE_CREATED = _(u'Fecha y hora de creación')
ABDCP_MESSAGE_RESPONDED = _(u'Fecha y hora de respuesta')
ABDCP_MESSAGE_DELIVERED = _(u'Fecha y hora de entrega')
ABDCP_MESSAGE_UPDATED = _(u'Fecha y hora de modificación')

ABDCP_MESSAGE_MODEL_NAME = _(u'Mensaje XML ABDCP')
ABDCP_MESSAGE_MODEL_NAME_PLURAL = _(u'Mensajes XML ABDCP')

# ABDCP Processes

ABDCP_PROCESS_01_SP = _(
    u'Proceso de Solicitud de Portabilidad y Programación'
)

ABDCP_PROCESS_02_RP = _(
    u'Proceso de Retorno de Números'
)

ABDCP_PROCESS_04_DE = _(
    u'Proceso de Detección de Errores'
)

ABDCP_PROCESS_05_CP = _(
    u'Proceso de Consulta Previa'
)

# ABDCP Message Types

ABDCP_MESSAGE_TYPE_CP = _(u'(CP) Consulta Previa')
ABDCP_MESSAGE_TYPE_ANCP = _(u'(ANCP) Asignación de número de consulta previa')
ABDCP_MESSAGE_TYPE_CPRABD = _(u'(CPRABD) Consulta previa rechazada por el ABDCP')
ABDCP_MESSAGE_TYPE_ECPC = _(u'(ECPC) Envío de consulta previa al cedente')

ABDCP_MESSAGE_TYPE_CPOCC = _(u'(CPOCC) Consulta previa objeción del concesionario cedente')

ABDCP_MESSAGE_TYPE_CPAC = _(u'(CPAC) Consulta previa aceptada por el cedente')
ABDCP_MESSAGE_TYPE_CPPR = _(u'(CPPR) Consulta previa procedente')
ABDCP_MESSAGE_TYPE_SP = _(u'(SP) Solicitud de portabilidad')
ABDCP_MESSAGE_TYPE_ANS = _(u'(ANS) Asignación de número de solicitud de portabilidad')
ABDCP_MESSAGE_TYPE_ESC = _(u'(ESC) Envío de solicitud al cedente')

ABDCP_MESSAGE_TYPE_OCC = _(u'(OCC) Objeción del concesionario cedente a la solicitud de portabilidad')

ABDCP_MESSAGE_TYPE_SAC = _(u'(SAC) Solicitud aceptada por el cedente')
ABDCP_MESSAGE_TYPE_APD = _(u'(APD) Acreditación pago deuda')
ABDCP_MESSAGE_TYPE_APDC = _(u'(APDC) Acreditación pago deuda al cedente')

ABDCP_MESSAGE_TYPE_RABDCP = _(u'(RABDCP) Solicitud de portabilidad rechazada por el ABDCP')

ABDCP_MESSAGE_TYPE_SPR = _(u'(SPR) Solicitud de portabilidad procedente')

ABDCP_MESSAGE_TYPE_CPSPR = _(u'(CPSPR) Solicitud de portabilidad procedente por consulta previa procedente')

ABDCP_MESSAGE_TYPE_CNPF = _(u'(CNPF) Cancelación de portabilidad por no programación')

ABDCP_MESSAGE_TYPE_PP = _(u'(PP) Programación de portabilidad')
ABDCP_MESSAGE_TYPE_FLEP = _(u'(FLEP) Fuera del límite para ejecutar la portabilidad')
ABDCP_MESSAGE_TYPE_PEP = _(u'(PEP) Programada para ejecutar portabilidad')
ABDCP_MESSAGE_TYPE_SR = _(u'(SR) Solicitud de retorno')
ABDCP_MESSAGE_TYPE_AR = _(u'(AR) Retorno de número aceptado')
ABDCP_MESSAGE_TYPE_DR = _(u'(DR) Denegación de retorno')
ABDCP_MESSAGE_TYPE_NI = _(u'(NI) No integridad')
ABDCP_MESSAGE_TYPE_NE = _(u'(NE) Notificación de error')



ABDCP_MESSAGE_PREVIOUS_CONSULT_ACCEPT = _(
    u'Previous Consultation Donor Acceptance Response'
)

ABDCP_MESSAGE_PORT_REQUEST_ACCEPT = _(u'Donor Port Acceptance Response')

# Validators

MESSAGE_ID_VALIDATION_ERROR = _(
    u'The value \'%(message_id)s\' does not seem to be '
    u'a valid message id'
)

TRANSACTION_ID_VALIDATION_ERROR = _(
    u'The value \'%(transaction_id)s\' does not seem to be '
    u'a valid transaction id'
)

SENDER_CODE_VALIDATION_ERROR = _(
    u'The value \'%(code)s\' does not seem to be a valid sender code'
)

RECIPIENT_CODE_VALIDATION_ERROR = _(
    u'The value \'%(code)s\' does not seem to be a valid recipient code'
)

STATED_CREATION_DATE_VALIDATION_ERROR = _(
    u'The value \'%(date)s\' does not seem to be a valid ABDCP date '
    u'in the \'%%Y%%m%%d%%H%%M%%S\' format'
)

# RESTful API

JSON_REQUIRED_RESTFUL_API_ERROR = _(
    u'The request body content type must be application/json'
)

INVALID_JSON_RESTFUL_API_ERROR = _(
    u'The request body must contain a valid JSON document'
)

UNEXPECTED_STRUCTURE_RESTFUL_API_ERROR = _(
    u'The JSON body does not seem to have the expected structure'
)

INVALID_CREDENTIALS_RESTFUL_API_ERROR = _(
    u'Invalid ABDCP credentials: userID and/or password is wrong'
)

INVALID_XML_DOCUMENT_RESTFUL_API_ERROR = _(
    u'Invalid ABDCP XML document: one or more validation error(s) found'
)

DUPLICATED_MESSAGE_RESTFUL_API_ERROR = _(
    u'The message with id %(message_id)s already exists'
)

MESSAGE_NOT_CREATED_RESTFUL_API_ERROR = _(
    u'The message with id %(message_id)s could not be created due '
    u'to an application error. Please report the incident'
)


