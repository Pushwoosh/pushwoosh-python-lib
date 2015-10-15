from datetime import datetime, date

from six import string_types

from .constants import PLATFORMS, PLATFORM_NAMES, LINK_MINIMIZERS,\
    TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN, \
    TAG_FILTER_OPERATOR_BETWEEN, TAG_FILTER_OPERATOR_NOTIN, TAG_FILTER_OPERATOR_NOTEQ


def valid_platform(platform):
    return platform in PLATFORMS


def platform_names(platforms):
    return [PLATFORM_NAMES[platform] for platform in platforms]


def valid_link_minimizer(link_minimizer):
    return link_minimizer in LINK_MINIMIZERS


def valid_operand(operand, types):
    for t in types:
        if isinstance(operand, t):
            return True
    return False


def valid_operand_list(operand_list, types):
    for operand in operand_list:
        if not valid_operand(operand, types):
            return False
    return True


def valid_operator(operator, operators):
    return operator in operators


def valid_operand_for_operator(operand, operator):
    _map = {
        TAG_FILTER_OPERATOR_LTE: (int, string_types, date, datetime),
        TAG_FILTER_OPERATOR_GTE: (int, string_types, date, datetime),
        TAG_FILTER_OPERATOR_BETWEEN: (list,),
        TAG_FILTER_OPERATOR_EQ: (int, string_types, list, date, datetime),
        TAG_FILTER_OPERATOR_NOTEQ: (int, string_types, date, datetime),
        TAG_FILTER_OPERATOR_IN: (list,),
        TAG_FILTER_OPERATOR_NOTIN: (list,),
    }
    return valid_operand(operand, _map[operator])


def valid_days(operand):
    if isinstance(operand, int):
        return operand > 0
    elif isinstance(operand, list):
        for value in operand:
            if value <= 0:
                return False
        return True
    return False


def valid_bool(operand):
    if isinstance(operand, string_types):
        values = ['true', 'false']
        return operand.lower() in values
    else:
        values = [0, 1]
        return operand in values


def set_date_value(operand):
    datetime_formats_map = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M',
    ]
    for f in datetime_formats_map:
        try:
            operand = datetime.strptime(str(operand), f).strftime('%Y-%m-%d %H:%M:%S')
            return operand
        except ValueError:
            continue
    return False


def set_dates_in_list(operand):
    operand = [set_date_value(v) for v in operand]

    if False in operand:
        return False
    return operand


def parse_date(operand):
    if isinstance(operand, string_types):
        return set_date_value(operand)
    elif isinstance(operand, list):
        return set_dates_in_list(operand)
    elif isinstance(operand, date):
        return operand.strftime('%Y-%m-%d')
    elif isinstance(operand, datetime):
        return operand.strftime('%Y-%m-%d %H:%M:%S')

    return False


def render_attrs(src, dst, attr_names):
    for attr_name in attr_names:
        attr = getattr(src, attr_name)
        if attr is not None:
            dst[attr_name] = attr
