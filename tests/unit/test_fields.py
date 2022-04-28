import unittest
from utils import cases
import api


class TestField(unittest.TestCase):

    @cases([
        [False, False, 'something'],
        [False, False, 1],

        [True, False, 'something'],
        [True, False, 1],

        [True, True, ''],
        [True, True, 'something'],
        [True, True, 1],

        [False, True, ''],
        [False, True, 'something'],
        [False, True, 1],
    ])
    def test_base_valid(self, case):
        required, nullable, value = case
        field = api.BaseField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, ''],
        [False, False, None],

        [True, False, ''],
        [True, False, None],

        [True, True, None],
    ])
    def test_base_invalid(self, case):
        required, nullable, value = case
        field = api.BaseField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, 'something'],

        [True, False, 'something'],

        [True, True, ''],
        [True, True, 'something'],

        [False, True, ''],
        [False, True, 'something'],
    ])
    def test_char_valid(self, case):
        required, nullable, value = case
        field = api.CharField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, ''],
        [False, False, None],
        [False, False, 1],
        [False, False, {}],

        [True, False, ''],
        [True, False, None],
        [True, False, 1],
        [True, False, []],

        [True, True, None],
        [True, True, 1],
    ])
    def test_char_invalid(self, case):
        required, nullable, value = case
        field = api.CharField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, {"key": 'value'}],

        [True, False, {"key": 'value'}],

        [True, True, {"key": 'value'}],
        [True, True, {}],

        [False, True, {"key": 'value'}],
        [False, True, {}],

    ])
    def test_argument_valid(self, case):
        required, nullable, value = case
        field = api.ArgumentsField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, ''],
        [False, False, None],
        [False, False, 1],
        [False, False, {}],

        [True, False, ''],
        [True, False, '1'],
        [True, False, None],
        [True, False, 1],
        [True, False, {}],

        [True, True, None],
        [True, True, 1],
        [True, True, '1'],
        [True, True, ''],
    ])
    def test_argument_invalid(self, case):
        required, nullable, value = case
        field = api.ArgumentsField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, 'something@'],

        [True, False, 'somethi@ng'],

        [True, True, ''],
        [True, True, 'somethi@ng'],

        [False, True, ''],
        [False, True, 'someth@ing'],
    ])
    def test_email_valid(self, case):
        required, nullable, value = case
        field = api.EmailField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, ''],
        [False, False, 'something'],
        [False, False, None],
        [False, False, 1],
        [False, False, {}],

        [True, False, ''],
        [True, False, 'something'],
        [True, False, None],
        [True, False, 1],
        [True, False, []],

        [False, True, 'something'],

        [True, True, None],
        [True, True, 'something'],
        [True, True, 1],
    ])
    def test_email_invalid(self, case):
        required, nullable, value = case
        field = api.EmailField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, '79061545455'],
        [False, False, 79061545455],

        [True, False, '79061545455'],
        [True, False, 79061545455],

        [True, True, '79061545455'],
        [True, True, 79061545455],

        [False, True, None],
        [False, True, '79061545455'],
        [False, True, 79061545455],
    ])
    def test_phone_valid(self, case):
        required, nullable, value = case
        field = api.PhoneField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, '89061545455'],
        [False, False, ''],
        [False, False, None],
        [False, False, 9055555555],
        [False, False, {}],
        [False, False, {'key': 'value'}],

        [True, False, '89061545455'],
        [True, False, ''],
        [True, False, None],
        [True, False, 9055555555],
        [True, False, {}],
        [True, False, {'key': 'value'}],

        [True, True, None],
        [True, True, 89061545455],
        [True, True, {}],
        [True, True, {'key': 'value'}],
    ])
    def test_phone_invalid(self, case):
        required, nullable, value = case
        field = api.PhoneField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, '10.10.2022'],

        [True, False, '10.10.2023'],

        [True, True, ''],
        [True, True, '10.10.2024'],

        [False, True, ''],
        [False, True, None],
        [False, True, '10.10.2025'],
    ])
    def test_date_valid(self, case):
        required, nullable, value = case
        field = api.DateField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, '10/10/2022'],
        [False, False, None],
        [False, False, ''],

        [True, False, '10-10-2023'],
        [True, False, ''],
        [True, False, '2022'],

        [True, True, '10.2024'],

        [False, True, '10.10..2025'],
    ])
    def test_date_invalid(self, case):
        required, nullable, value = case
        field = api.DateField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, '10.10.2022'],

        [True, False, '10.10.2023'],

        [True, True, ''],
        [True, True, '10.10.2024'],

        [False, True, ''],
        [False, True, None],
        [False, True, '10.10.2025'],
    ])
    def test_bdate_valid(self, case):
        required, nullable, value = case
        field = api.BirthDayField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, '10/10/2022'],
        [False, False, '10.10.1950'],
        [False, False, None],
        [False, False, ''],

        [True, False, '10-10-2023'],
        [True, False, '10.10.1951'],
        [True, False, ''],
        [True, False, '2022'],

        [True, True, '10.2024'],
        [True, True, '10.10.1951'],

        [False, True, '10.10..2025'],
        [False, True, '10.10.1951'],
    ])
    def test_bdate_invalid(self, case):
        required, nullable, value = case
        field = api.BirthDayField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, 1],
        [True, False, 2],

        [True, True, 0],
        [True, True, ''],

        [False, True, 1],
        [False, True, ''],
        [False, True, None],
    ])
    def test_gender_valid(self, case):
        required, nullable, value = case
        field = api.GenderField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, ''],
        [False, False, 8],
        [False, False, None],
        [False, False, 'rty'],

        [True, False, ''],
        [True, False, 5],
        [True, False, None],
        [True, False, '2022'],

        [True, True, 5],
        [True, True, None],
        [True, True, '2022'],

        [False, True, 5],
        [False, True, '2022'],
    ])
    def test_gender_invalid(self, case):
        required, nullable, value = case
        field = api.GenderField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)

    @cases([
        [False, False, [2022]],

        [True, False, [1, 2]],

        [True, True, [1, 2]],

        [False, True, [1, 2]],
        [False, True, []],
    ])
    def test_id_valid(self, case):
        required, nullable, value = case
        field = api.ClientIDsField(required, nullable)
        self.assertEqual(field.valid(value), None)

    @cases([
        [False, False, '10/10/2022'],
        [False, False, None],
        [False, False, 45],
        [False, False, ['']],

        [True, False, '10/10/2022'],
        [True, False, None],
        [True, False, 45],
        [True, False, ['']],

        [True, True, '10/10/2022'],
        [True, True, None],
        [True, True, 45],
        [True, True, ['']],

        [False, True, '10/10/2022'],
        [False, True, None],
        [False, True, 45],
        [False, True, ['']],
    ])
    def test_id_invalid(self, case):
        required, nullable, value = case
        field = api.ClientIDsField(required, nullable)
        with self.assertRaises(api.ValidationError):
            field.valid(value)


if __name__ == '__main___':
    unittest.main()
