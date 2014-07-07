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
    ('SPC', 'SPC', strings.ABDCP_MESSAGE_TYPE_SPC),
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

ABDCP_MESSAGE_XSD_FILENAME = 'iconectivSchemaABDCP_04242014.xsd'
ABDCP_MESSAGE_XSD_DIRPATH = '%(DATA_DIR)s/xsd'

