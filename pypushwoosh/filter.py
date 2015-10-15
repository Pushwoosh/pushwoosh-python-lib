from datetime import datetime, date

from six import string_types

from .utils import valid_platform, platform_names, valid_operand_for_operator, valid_operand_list, \
    valid_operand, valid_operator, valid_days, valid_bool, parse_date
from .constants import TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, \
    TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_BETWEEN, TAG_FILTER_OPERATOR_NOTEQ, TAG_FILTER_OPERATOR_NOTIN
from .exceptions import PushwooshFilterInvalidOperandException, PushwooshFilterInvalidOperatorException


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
        self.semantic_validation(operator, operand)

        self.tag_name = tag_name
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return '%s("%s", %s, %s)' % (self.prefix, self.tag_name, self.operator, self._render_operand())

    def semantic_validation(self, operator, operand):
        if not valid_operator(operator, self.operators):
            raise PushwooshFilterInvalidOperatorException('Invalid operator %s for %s' % (operator, self.__class__.__name__))

        if not valid_operand_for_operator(operand, operator):
            raise PushwooshFilterInvalidOperandException('Invalid operand type %s for operator %s' % (type(operand).__name__, operator))

        if isinstance(operand, list) and not valid_operand_list(operand, self.value_types):
            raise PushwooshFilterInvalidOperandException('Invalid operand list value for %s' % self.__class__.__name__)

        if not isinstance(operand, list) and not valid_operand(operand, self.value_types):
            raise PushwooshFilterInvalidOperandException('Invalid operand type %s for %s' % (type(operand).__name__, self.__class__.__name__))

        if operator == TAG_FILTER_OPERATOR_BETWEEN and len(operand) != 2:
            raise PushwooshFilterInvalidOperandException('Invalid operand len for operator %s' % operator)

        if operator == TAG_FILTER_OPERATOR_IN and len(operand) == 0:
            raise PushwooshFilterInvalidOperandException('Invalid operand len for operator %s' % operator)

    def _render_operand(self):
        if isinstance(self.operand, list):
            return self._render_list_operand(self.operand)
        elif isinstance(self.operand, int):
            return self._render_int_operand(self.operand)
        elif isinstance(self.operand, string_types) or isinstance(self.operand, datetime) or isinstance(self.operand, date):
            return self._render_str_operand(self.operand)

        raise NotImplementedError()

    def _render_list_operand(self, operand):
        result = []
        for op in operand:
            if isinstance(op, int):
                result.append(self._render_int_operand(op))
            elif isinstance(op, string_types):
                result.append(self._render_str_operand(op))
        return '[%s]' % ', '.join(result)

    def _render_str_operand(self, operand):
        return '"%s"' % operand

    def _render_int_operand(self, operand):
        return '%d' % operand


class ApplicationBaseTagFilter(BaseTagFilter):
    prefix = 'AT'

    def __init__(self, tag_name, operator, operand, code):
        super(ApplicationBaseTagFilter, self).__init__(tag_name, operator, operand)
        self.code = code

    def __str__(self):
        return '%s("%s", "%s", %s, %s)' % (self.prefix, self.code, self.tag_name, self.operator,
                                           self._render_operand())


class IntegerTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTEQ, TAG_FILTER_OPERATOR_NOTIN)
    value_types = (int,)


class StringTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTEQ, TAG_FILTER_OPERATOR_NOTIN)
    value_types = (int, string_types,)


class ListTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN,)
    value_types = (int, string_types,)


class DateTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTIN, TAG_FILTER_OPERATOR_NOTEQ)
    value_types = (string_types, date, datetime)

    def semantic_validation(self, operator, operand):
        super(DateTagFilter, self).semantic_validation(operator, operand)
        self.operand = parse_date(operand)
        if not self.operand:
            raise PushwooshFilterInvalidOperandException('Invalid date format')


class DaysTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTIN, TAG_FILTER_OPERATOR_NOTEQ)
    value_types = (int,)

    def semantic_validation(self, operator, operand):
        super(DaysTagFilter, self).semantic_validation(operator, operand)
        if not valid_days(operand):
            raise PushwooshFilterInvalidOperandException('Days count must be greater than 0')


class BooleanTagFilter(BaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ,)
    value_types = (int, string_types)

    def semantic_validation(self, operator, operand):
        super(BooleanTagFilter, self).semantic_validation(operator, operand)
        if not valid_bool(operand):
            raise PushwooshFilterInvalidOperandException('%s value must be 0, 1, "true" or "false"' % self.__class__.__name__)


# Application tag filters
class IntegerTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTEQ, TAG_FILTER_OPERATOR_NOTIN)
    value_types = (int,)


class StringTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTEQ, TAG_FILTER_OPERATOR_NOTIN)
    value_types = (int, string_types,)


class ListTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_IN,)
    value_types = (int, string_types,)


class DateTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTIN, TAG_FILTER_OPERATOR_NOTEQ)
    value_types = (string_types,)

    def semantic_validation(self, operator, operand):
        super(DateTagFilterByApplication, self).semantic_validation(operator, operand)
        self.operand = parse_date(operand)
        if not self.operand:
            raise PushwooshFilterInvalidOperandException('Invalid date format')


class DaysTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_LTE, TAG_FILTER_OPERATOR_GTE, TAG_FILTER_OPERATOR_EQ, TAG_FILTER_OPERATOR_BETWEEN,
                 TAG_FILTER_OPERATOR_IN, TAG_FILTER_OPERATOR_NOTIN, TAG_FILTER_OPERATOR_NOTEQ)
    value_types = (int,)

    def semantic_validation(self, operator, operand):
        super(DaysTagFilterByApplication, self).semantic_validation(operator, operand)
        if not valid_days(operand):
            raise PushwooshFilterInvalidOperandException('Days count must be greater than 0')


class BooleanTagFilterByApplication(ApplicationBaseTagFilter):
    operators = (TAG_FILTER_OPERATOR_EQ,)
    value_types = (int, string_types)

    def semantic_validation(self, operator, operand):
        super(BooleanTagFilterByApplication, self).semantic_validation(operator, operand)
        if not valid_bool(operand):
            raise PushwooshFilterInvalidOperandException('%s value must be 0, 1, "true" or "false"' % self.__class__.__name__)
