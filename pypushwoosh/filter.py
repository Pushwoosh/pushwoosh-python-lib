from pypushwoosh.utils import valid_platform, platform_names, valid_operand_for_operator, valid_operand_list, \
    valid_operand, valid_operator
from pypushwoosh.constants import TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, \
    TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_BETWEEN


class BaseFilter(object):
    def union(self, other):
        return UnionFilter(self, other)

    def intersect(self, other):
        return IntersectFilter(self, other)

    def subtract(self, other):
        return SubtractFilter(self, other)


class BaseOperatorFilter(BaseFilter):
    operation_sign = None

    def __init__(self, first_filter, second_filter):
        self.first_filter = first_filter
        self.second_filter = second_filter

    def __str__(self):
        return '(%s %s %s)' % (self.first_filter, self.operation_sign, self.second_filter)


class UnionFilter(BaseOperatorFilter):
    operation_sign = '+'


class IntersectFilter(BaseOperatorFilter):
    operation_sign = '*'


class SubtractFilter(BaseOperatorFilter):
    operation_sign = '\\'


class ApplicationFilter(BaseFilter):
    prefix = 'A'

    def __init__(self, code, platforms=None):
        self.code = code

        if platforms is not None:
            if not isinstance(platforms, list):
                platforms = [platforms]

            for platform in platforms:
                if not valid_platform(platform):
                    raise TypeError

        self.platforms = platforms

    def __str__(self):
        platforms_str = ''
        if self.platforms is not None:
            platforms_str = '", "'.join(platform_names(self.platforms))
            platforms_str = ', ["%s"]' % platforms_str
        return '%s("%s"%s)' % (self.prefix, self.code, platforms_str)


class ApplicationGroupFilter(ApplicationFilter):
    prefix = 'G'


class BaseTagFilter(BaseFilter):
    prefix = 'T'
    operators = tuple()
    value_types = tuple()

    def __init__(self, tag_name, operator, operand):
        self.tag_name = tag_name

        assert valid_operator(operator, self.operators), 'Invalid operator %s for %s' % (operator, self.__class__.__name__)
        assert valid_operand_for_operator(operand, operator), 'Invalid operand type %s for operator %s' % (type(operand).__name__, operator)
        if isinstance(operand, list):
            assert valid_operand_list(operand, self.value_types), 'Invalid operand list value for %s' % (self.__class__.__name__)
        else:
            assert valid_operand(operand, self.value_types), 'Invalid operand type %s for %s' % (type(operand).__name__, self.__class__.__name__)

        if operator == TAG_FILTER_OPERATOR_BETWEEN:
            assert len(operand) == 2, 'Invalid operand len for operator %s' % operator
        elif operator == TAG_FILTER_OPERATOR_IN:
            assert len(operand) > 0, 'Invalid operand len for operator %s' % operator

        self.operator = operator
        self.operand = operand

    def __str__(self):
        return '%s("%s", %s, %s)' % (self.prefix, self.tag_name, self.operator, self._render_operand())

    def _render_operand(self):
        if isinstance(self.operand, list):
            return self._render_list_operand(self.operand)
        elif isinstance(self.operand, int):
            return self._render_int_operand(self.operand)
        elif isinstance(self.operand, basestring):
            return self._render_str_operand(self.operand)
        raise NotImplementedError()

    def _render_list_operand(self, operand):
        result = []
        for op in operand:
            if isinstance(op, int):
                result.append(self._render_int_operand(op))
            elif isinstance(op, basestring):
                result.append(self._render_str_operand(op))
        return '[%s]' % ', '.join(result)

    def _render_str_operand(self, operand):
        return '"%s"' % operand

    def _render_int_operand(self, operand):
        return '%d' % operand


class IntegerTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN,
                 TAG_FILTER_OPERATOR_BETWEEN,)
    value_types = (int,)


class StringTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN,)
    value_types = (int, basestring,)


class ListTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_IN,)
    value_types = (int, basestring)
