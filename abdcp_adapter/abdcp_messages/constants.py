# -*- coding: utf-8 -*-

from collections import OrderedDict
from common.datastructures import Enumeration
from abdcp_messages import strings

ABDCP_MESSAGE_ID_MASK = 'OOAAAAMMDDTICCCCC'
ABDCP_MESSAGE_ID_LENGTH = len(ABDCP_MESSAGE_ID_MASK)

ABDCP_TRANSACTION_ID_MASK = 'OOAAAAMMDDTICCCCC'
ABDCP_TRANSACTION_ID_LENGTH = len(ABDCP_TRANSACTION_ID_MASK)

# Enumerations

ABDCP_PROCESS_CHOICES = Enumeration([
    ('01', 'SP', strings.ABDCP_PROCESS_01_SP),
    ('02', 'RP', strings.ABDCP_PROCESS_02_RP),
    ('04', 'DE', strings.ABDCP_PROCESS_04_DE),
    ('05', 'CP', strings.ABDCP_PROCESS_05_CP)
])

ABDCP_MESSAGE_TYPE_CHOICES = Enumeration([
    ('CP', 'CP', strings.ABDCP_MESSAGE_TYPE_CP),
    ('ANCP', 'ANCP', strings.ABDCP_MESSAGE_TYPE_ANCP),
    ('CPRABD', 'CPRABD', strings.ABDCP_MESSAGE_TYPE_CPRABD),
    ('ECPC', 'ECPC', strings.ABDCP_MESSAGE_TYPE_ECPC),
    ('CPOCC', 'CPOCC', strings.ABDCP_MESSAGE_TYPE_CPOCC),
    ('CPAC', 'CPAC', strings.ABDCP_MESSAGE_TYPE_CPAC),
    ('CPPR', 'CPPR', strings.ABDCP_MESSAGE_TYPE_CPPR),
    ('SP', 'SP', strings.ABDCP_MESSAGE_TYPE_SP),
    ('ANS', 'ANS', strings.ABDCP_MESSAGE_TYPE_ANS),
    ('ESC', 'ESC', strings.ABDCP_MESSAGE_TYPE_ESC),
    ('OCC', 'OCC', strings.ABDCP_MESSAGE_TYPE_OCC),
    ('SAC', 'SAC', strings.ABDCP_MESSAGE_TYPE_SAC),
    ('APD', 'APD', strings.ABDCP_MESSAGE_TYPE_APD),
    ('APDC', 'APDC', strings.ABDCP_MESSAGE_TYPE_APDC),
    ('RABDCP', 'RABDCP', strings.ABDCP_MESSAGE_TYPE_RABDCP),
    ('SPR', 'SPR', strings.ABDCP_MESSAGE_TYPE_SPR),
    ('CPSPR', 'CPSPR', strings.ABDCP_MESSAGE_TYPE_CPSPR),
    ('CNPF', 'CNPF', strings.ABDCP_MESSAGE_TYPE_CNPF),
    ('PP', 'PP', strings.ABDCP_MESSAGE_TYPE_PP),
    ('FLEP', 'FLEP', strings.ABDCP_MESSAGE_TYPE_FLEP),
    ('PEP', 'PEP', strings.ABDCP_MESSAGE_TYPE_PEP),
    ('SR', 'SR', strings.ABDCP_MESSAGE_TYPE_SR),
    ('AR', 'AR', strings.ABDCP_MESSAGE_TYPE_AR),
    ('DR', 'DR', strings.ABDCP_MESSAGE_TYPE_DR),
    ('NI', 'NI', strings.ABDCP_MESSAGE_TYPE_NI),
    ('NE', 'NE', strings.ABDCP_MESSAGE_TYPE_NE)
])

ABDCP_MESSAGE_TYPES_BY_PROCESS_TYPE = OrderedDict([
    ('01', [ 'SP', 'ANS', 'ESC', 'OCC', 'SAC', 'APD', 'APDC',
            'RABDCP', 'SPR', 'CPSPR', 'CNPF', 'PP', 'FLEP', 'PEP']),
    ('02', [ 'SR', 'AR', 'DR']),
    ('04', [ 'NI', 'NE']),
    ('05', [ 'CP', 'ANCP', 'CPRABD', 'ECPC', 'CPOCC', 'CPAC', 'CPPR'])
])

ABDCP_MESSAGE_TO_PROCESS_MAP = OrderedDict()

for process_type, message_types in \
    ABDCP_MESSAGE_TYPES_BY_PROCESS_TYPE.iteritems():
    for mt in message_types:
        ABDCP_MESSAGE_TO_PROCESS_MAP[mt] = process_type

ABDCP_MESSAGE_XSD_FILENAME = 'iconectivSchemaABDCP_01042016.xsd'
ABDCP_MESSAGE_XSD_DIRPATH = '%(DATA_DIR)s/xsd'

#OBJECTION CAUSE DONNOR
ABDCP_OC_SUSPEND_SERVICE        = 'REC01PRT01'
ABDCP_OC_PHONE_NOT_OWNED        = 'REC01PRT05'
ABDCP_OC_INVALID_SERVICE_TYPE   = 'REC01PRT06'
ABDCP_OC_INVALID_ID_CUSTOMER    = 'REC01PRT07'
ABDCP_OC_INVALID_MODE           = 'REC01PRT08'
ABDCP_OC_HAS_DEBT               = 'REC01PRT09'

OBJECTION_CAUSE = {}
OBJECTION_CAUSE[ABDCP_OC_SUSPEND_SERVICE] = "El servicio esta suspendido"
OBJECTION_CAUSE[ABDCP_OC_PHONE_NOT_OWNED] = "El tel??fono no nos pertenece"
OBJECTION_CAUSE[ABDCP_OC_INVALID_SERVICE_TYPE] = "El n??mero telef??nico no pertenece al Tipo de Servicio indicado"
OBJECTION_CAUSE[ABDCP_OC_INVALID_ID_CUSTOMER] = "El documento de identidad no corresponde al cliente"
OBJECTION_CAUSE[ABDCP_OC_INVALID_MODE] = "El modo solicitado no es POSTPAGO"
OBJECTION_CAUSE[ABDCP_OC_HAS_DEBT] = "El tel??fono tiene deudas"

ABDCP_PORTABILITY_TYPE = {'01':'PREPAGO','02':'POSTPAGO'}

ABDCP_MESSAGE_TYPE_ESC = "ESC"

LINE_TYPE_FIX = 1