from pypushwoosh.constants import PLATFORMS, PLATFORM_NAMES, LINK_MINIMIZERS,\
    TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN, \
    TAG_FILTER_OPERATOR_BETWEEN


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
        TAG_FILTER_OPERATOR_LTE: (int, ),
        TAG_FILTER_OPERATOR_GTE: (int, ),
        TAG_FILTER_OPERATOR_BETWEEN: (list, ),
        TAG_FILTER_OPERATOR_EQ: (int, basestring),
        TAG_FILTER_OPERATOR_IN: (int, basestring, list)
    }
    return valid_operand(operand, _map[operator])


def render_attrs(src, dst, attr_names):
    for attr_name in attr_names:
            attr = getattr(src, attr_name)
            if attr is not None:
                dst[attr_name] = attr
