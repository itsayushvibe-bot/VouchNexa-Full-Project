import unittest
from app.utils.json_parser import parse_voucher_json

class TestVouchNexa(unittest.TestCase):
    def test_json_parser_adjacent_objects(self):
        raw = '{"voucher":"CODE_A"}{"voucher":"CODE_B"}'
        vouchers, rejected, err = parse_voucher_json(raw)
        self.assertEqual(err, "")
        self.assertEqual(len(vouchers), 2)
        self.assertEqual(rejected, 0)

    def test_json_parser_nested_objects(self):
        raw = '{"voucher":"CODE_C", "details":{"exp":"2026"}}'
        vouchers, rejected, err = parse_voucher_json(raw)
        self.assertEqual(err, "")
        self.assertEqual(len(vouchers), 1)

    def test_json_parser_rejects_credentials(self):
        raw = '{"voucher":"VALID_VOUCHER"}{"login":"admin", "password":"secret_password"}'
        vouchers, rejected, err = parse_voucher_json(raw)
        self.assertEqual(err, "")
        self.assertEqual(len(vouchers), 1)
        self.assertEqual(rejected, 1)

if __name__ == "__main__":
    unittest.main()
