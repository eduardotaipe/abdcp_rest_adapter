# -*- coding: utf-8 -*-
import time

from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ESC_ABDCP_XML_Message, CPAC_ABDCP_XML_Message, CPOCC_ABDCP_XML_Message, CPSPR_ABDCP_XML_Message, SAC_ABDCP_XML_Message, PEP_ABDCP_XML_Message, OCC_ABDCP_XML_Message
from abdcp_messages import strings
from abdcp_messages import constants
from abdcp_messages.xmlbuilders import SAC_XMLBuilder,OCC_XMLBuilder

from abdcp_processes import ABDCP_Message
from abdcp_processes.cp import ECPC,CPAC
from abdcp_processes import settings
from abdcp_processes.tasks import process_message

from operators.models import Operator

# solicitud de retorno
class SR(ABDCP_Message):
    """Inicio de retorno de portabilidad"""
    pass

# solicitud de retorno
class AR(ABDCP_Message):
    """Retorno de portabilidad Aceptado"""
    pass

