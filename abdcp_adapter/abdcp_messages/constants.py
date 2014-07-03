# -*- coding: utf-8 -*-

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

