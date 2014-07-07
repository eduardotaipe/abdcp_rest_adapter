# -*- coding: utf-8 -*-

from easyxsd import xsd_from_file
from easyxsd import xml_from_string
from easyxsd import xsd_error_log_as_simple_strings
from easyxsd import validate

from abdcp_messages import settings as abdcp_messages_settings

def abdcp_validate_xml_message(xmlstr):
    xml = xml_from_string(xmlstr)
    xsd = xsd_from_file(abdcp_messages_settings.ABDCP_MESSAGE_XSD_FILEPATH)
    is_valid = validate(xml, xsd)
    errors = xsd_error_log_as_simple_strings(xsd.error_log)
    return (is_valid, errors, )
