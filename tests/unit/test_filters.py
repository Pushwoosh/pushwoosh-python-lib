from datetime import datetime
import unittest
from pypushwoosh import constants
from pypushwoosh.exceptions import PushwooshFilterInvalidOperatorException, PushwooshFilterInvalidOperandException
from pypushwoosh.filter import ApplicationFilter, ApplicationGroupFilter, IntegerTagFilter, StringTagFilter, \
    ListTagFilter, DateTagFilter, DaysTagFilter, IntegerTagFilterByApplication, StringTagFilterByApplication, \
    DateTagFilterByApplication, DaysTagFilterByApplication, BooleanTagFilter, BooleanTagFilterByApplication

HTTP_200_OK = 200
STATUS_OK = 'OK'


class TestApplicationFilter(unittest.TestCase):

    def setUp(self):
        self.test_code = '0000-0000'
        self.prefix = 'A'
        self.pwfilter = ApplicationFilter

    def test_valid_filter(self):
        expected_result = '%s("%s")' % (self.prefix, self.test_code)
        result = self.pwfilter(self.test_code)

        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_with_platforms(self):
        expected_result = '%s("%s", ["%s", "%s"])' % (self.prefix,
                                                      self.test_code,
                                                      constants.PLATFORM_NAMES[constants.PLATFORM_IOS],
                                                      constants.PLATFORM_NAMES[constants.PLATFORM_ANDROID])
        result = self.pwfilter(self.test_code, [constants.PLATFORM_IOS, constants.PLATFORM_ANDROID])

        self.assertEqual(result.__str__(), expected_result)

    def test_filter_invalid_platform(self):
        try:
            self.pwfilter(self.test_code, 'Invalid Platform')
            self.assertEqual(True, 'Platform must be invalid')
        except TypeError:
            self.assertEqual(True, True)


class TestApplicationGroupFilter(TestApplicationFilter):

    def setUp(self):
        self.test_code = '0000-0000'
        self.prefix = 'G'
        self.pwfilter = ApplicationGroupFilter


class TestInvalidOperatorForOperand(unittest.TestCase):
    def setUp(self):
        self.pwfilter = IntegerTagFilter
        self.tag_name = 'testInt'

    def filter_with_invalid_operator_for_operand(self, value, operator):
        args = [self.tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)

    def test_invalid_operator_type(self):
        self.filter_with_invalid_operator_for_operand([1, 2], constants.TAG_FILTER_OPERATOR_GTE)
        self.filter_with_invalid_operator_for_operand([1, 2], constants.TAG_FILTER_OPERATOR_LTE)
        self.filter_with_invalid_operator_for_operand(1, constants.TAG_FILTER_OPERATOR_BETWEEN)
        self.filter_with_invalid_operator_for_operand('1', constants.TAG_FILTER_OPERATOR_BETWEEN)
        self.filter_with_invalid_operator_for_operand(1, constants.TAG_FILTER_OPERATOR_IN)
        self.filter_with_invalid_operator_for_operand('1', constants.TAG_FILTER_OPERATOR_IN)


class TestInvalidOperand(unittest.TestCase):

    def filter_with_invalid_operand_type(self, value, operator, tag_name):
        args = [tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)

    def test_invalid_operand_type_int(self):
        tag_name = 'testInt'
        str_value = 'Invalid value for int'
        between_value = ['invalid_min', 'invalid_max']
        in_value = ['1', '2', '3']

        self.pwfilter = IntegerTagFilter
        self.filter_with_invalid_operand_type(str_value, constants.TAG_FILTER_OPERATOR_EQ, tag_name)
        self.filter_with_invalid_operand_type(between_value, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)
        self.filter_with_invalid_operand_type(in_value, constants.TAG_FILTER_OPERATOR_IN, tag_name)

    def test_invalid_operand_type_str(self):
        tag_name = 'testString'
        list_value_in = [[1, 2], [1, 2]]

        self.pwfilter = StringTagFilter
        self.filter_with_invalid_operand_type(list_value_in, constants.TAG_FILTER_OPERATOR_IN, tag_name)

    def test_invalid_operand_type_list(self):
        tag_name = 'testString'
        list_value_in = [[1, 2], [1, 2]]

        self.pwfilter = ListTagFilter
        self.filter_with_invalid_operand_type(list_value_in, constants.TAG_FILTER_OPERATOR_IN, tag_name)

    def test_invalid_operand_type_date(self):
        tag_name = 'testDate'
        self.pwfilter = DateTagFilter
        self.filter_with_invalid_operand_type(1, constants.TAG_FILTER_OPERATOR_EQ, tag_name)
        self.filter_with_invalid_operand_type([1, 'str'], constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)
        self.filter_with_invalid_operand_type(['str', 'str', 1], constants.TAG_FILTER_OPERATOR_IN, tag_name)

    def test_invalid_operand_type_days(self):
        tag_name = 'testDays'
        str_value = 'Invalid value for days'
        between_value = ['invalid_min', 'invalid_max']
        self.pwfilter = DaysTagFilter
        self.filter_with_invalid_operand_type(str_value, constants.TAG_FILTER_OPERATOR_EQ, tag_name)
        self.filter_with_invalid_operand_type(between_value, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)


class TestInvalidOperator(unittest.TestCase):

    def filter_with_invalid_operator(self, value, operator, tag_name):
        args = [tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperatorException, self.pwfilter, *args)

    def test_invalid_operator(self):
        tag_name = 'testInt'
        value = [1, 2, 3]

        self.pwfilter = IntegerTagFilter
        self.filter_with_invalid_operator(value, 'Invalid Operator', tag_name)

    def test_invalid_operator_type_str(self):
        tag_name = 'testString'
        value = 1
        list_value = ['123', 'asd']

        self.pwfilter = StringTagFilter
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_GTE, tag_name)
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_LTE, tag_name)
        self.filter_with_invalid_operator(list_value, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)

    def test_invalid_operator_type_list(self):
        tag_name = 'testList'
        value = 1
        list_value = ['123', 'asd']

        self.pwfilter = ListTagFilter
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_GTE, tag_name)
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_LTE, tag_name)
        self.filter_with_invalid_operator(list_value, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)

    def test_invalid_operator_type_boolean(self):
        tag_name = 'testBool'
        value = 1
        list_value = [0, 1]

        self.pwfilter = BooleanTagFilter
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_GTE, tag_name)
        self.filter_with_invalid_operator(value, constants.TAG_FILTER_OPERATOR_LTE, tag_name)
        self.filter_with_invalid_operator(list_value, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)
        self.filter_with_invalid_operator(list_value, constants.TAG_FILTER_OPERATOR_IN, tag_name)


class TestInvalidOperandLength(unittest.TestCase):

    def filter_with_invalid_operator_len(self, value, operator, tag_name):
        args = [tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)

    def test_invalid_len_in(self):
        tag_name = 'testStr'
        value = []

        self.pwfilter = ListTagFilter
        self.filter_with_invalid_operator_len(value, constants.TAG_FILTER_OPERATOR_IN, tag_name)

    def test_invalid_len_between(self):
        tag_name = 'testInt'
        value_lt = [1]
        value_gt = [1, 2, 3]

        self.pwfilter = IntegerTagFilter
        self.filter_with_invalid_operator_len(value_lt, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)
        self.filter_with_invalid_operator_len(value_gt, constants.TAG_FILTER_OPERATOR_BETWEEN, tag_name)


class TestIntegerTagFilter(unittest.TestCase):

    def setUp(self):
        self.pwfilter = IntegerTagFilter
        self.tag_name = 'testInt'

    def test_valid_filter(self):
        expected_result = 'T("%s", %s, 1)' % (self.tag_name, constants.TAG_FILTER_OPERATOR_GTE)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_GTE, 1)
        self.assertEqual(expected_result, result.__str__())

    def test_valid_filter_between_operator(self):
        expected_result = 'T("%s", %s, [1, 2])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, [1, 2])
        self.assertEqual(expected_result, result.__str__())

    def test_valid_filter_in_operator(self):
        expected_result = 'T("%s", %s, [1, 2, 3])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_IN)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_IN, [1, 2, 3])
        self.assertEqual(expected_result, result.__str__())


class TestStringTagFilter(unittest.TestCase):
    pwfilter = StringTagFilter
    tag_name = 'testStr'

    def test_valid_filter(self):
        expected_result = 'T("%s", %s, "test value")' % (self.tag_name, constants.TAG_FILTER_OPERATOR_EQ)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, 'test value')
        self.assertEqual(expected_result, result.__str__())

    def test_valid_filter_in_operator(self):
        expected_result = 'T("%s", %s, ["1", "2"])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_IN)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_IN, ['1', '2'])
        self.assertEqual(expected_result, result.__str__())


class TestListTagFilter(unittest.TestCase):

    def setUp(self):
        self.pwfilter = ListTagFilter
        self.tag_name = 'testList'

    def test_valid_filter_in_operator(self):
        expected_result = 'T("%s", %s, [1, 2, "2"])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_IN)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_IN, [1, 2, '2'])
        self.assertEqual(expected_result, result.__str__())


class TestDateTagFilter(unittest.TestCase):

    def setUp(self):
        self.pwfilter = DateTagFilter
        self.tag_name = 'testDate'

    def invalid_date_format(self, operator, value):
        args = [self.tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)

    def test_valid_filter(self):
        values = [
            '2014-12-05 22:22:22',
            '2014-12-05 22:22',
            '2014-12-05',
            '2014-12-05T22:22:22',
            '2014-12-05T22:22',
        ]
        for value in values:
            expected_result = 'T("%s", %s, "%s")' % (self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
            result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
            self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_between(self):
        value = ['2013-06-22 00:00:00', '2013-06-25']
        expected_result = 'T("%s", %s, ["%s", "%s"])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, value[0], value[1])

        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, value)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_datetime_object(self):
        value = datetime.strptime('2013-06-22 00:00:00', '%Y-%m-%d %H:%M:%S')
        expected_result = 'T("%s", %s, "%s")' % (self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)

        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        self.assertEqual(result.__str__(), expected_result)

    def test_invalid_date_format(self):
        self.invalid_date_format(constants.TAG_FILTER_OPERATOR_GTE, '2')
        self.invalid_date_format(constants.TAG_FILTER_OPERATOR_BETWEEN, ['2013-06-25', '1'])


class TestDaysTagFilter(unittest.TestCase):

    def setUp(self):
        self.pwfilter = DaysTagFilter
        self.tag_name = 'testDays'

    def test_valid_filter(self):
        value = 1
        expected_result = 'T("%s", %s, %d)' % (self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_between(self):
        value = [1, 3]
        expected_result = 'T("%s", %s, [%s, %s])' % (self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, value[0], value[1])

        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, value)
        self.assertEqual(result.__str__(), expected_result)

    def test_invalid_days(self):
        args = [self.tag_name, constants.TAG_FILTER_OPERATOR_BETWEEN, [-1, 3]]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)


class TestBooleanTagFilter(unittest.TestCase):

    def setUp(self):
        self.pwfilter = BooleanTagFilter
        self.tag_name = 'testBool'

    def invalid_boolean(self, operator, value):
        args = [self.tag_name, operator, value]
        self.assertRaises(PushwooshFilterInvalidOperandException, self.pwfilter, *args)

    def test_valid_filter_in_operator(self):
        expected_result = 'T("%s", %s, "true")' % (self.tag_name, constants.TAG_FILTER_OPERATOR_EQ)
        result = self.pwfilter(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, 'true')
        self.assertEqual(expected_result, result.__str__())

    def test_invalid_boolean(self):
        self.invalid_boolean(constants.TAG_FILTER_OPERATOR_EQ, 'invalid value')
        self.invalid_boolean(constants.TAG_FILTER_OPERATOR_EQ, 2)


class TestOperatorsFilter(unittest.TestCase):

    def test_valid_filter(self):
        app_code = '0000-0000'
        tag_name = 'test_string'
        tag_value = 'test value'
        expected_result = '(((A("%s") + T("%s", EQ, "%s")) * A("%s")) \ T("%s", EQ, "%s"))' % \
                          (app_code, tag_name, tag_value, app_code, tag_name, tag_value)

        tag_filter = StringTagFilter(tag_name, constants.TAG_FILTER_OPERATOR_EQ, tag_value)
        app_filter = ApplicationFilter(app_code)
        union_filter = app_filter.union(tag_filter)
        intersect_filter = union_filter.intersect(app_filter)
        subtract_filter = intersect_filter.subtract(tag_filter)

        self.assertEqual(subtract_filter.__str__(), expected_result)


class TestApplicationTagFilter(unittest.TestCase):

    def setUp(self):
        self.tag_name = 'testApplicationTag'
        self.code = '0000-0000'

    def test_valid_filter_int(self):
        value = 1
        expected_result = 'AT("%s", "%s", %s, %d)' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = IntegerTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value, self.code)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_string(self):
        value = 1
        expected_result = 'AT("%s", "%s", %s, %d)' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = StringTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value, self.code)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_list(self):
        expected_result = 'AT("%s", "%s", %s, [1, 2])' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ)
        result = DaysTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, [1, 2], self.code)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_days(self):
        value = 1
        expected_result = 'AT("%s", "%s", %s, %d)' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = DaysTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value, self.code)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_date(self):
        value = '2014-02-02 00:15:10'
        expected_result = 'AT("%s", "%s", %s, "%s")' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = DateTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value, self.code)
        self.assertEqual(result.__str__(), expected_result)

    def test_valid_filter_boolean(self):
        value = 'False'
        expected_result = 'AT("%s", "%s", %s, "%s")' % (self.code, self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value)
        result = BooleanTagFilterByApplication(self.tag_name, constants.TAG_FILTER_OPERATOR_EQ, value, self.code)
        self.assertEqual(result.__str__(), expected_result)