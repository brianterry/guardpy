"""Exercise the installed wheel across its supported Python ABI."""

import importlib
import os
import unittest

guard = importlib.import_module(os.environ.get("GUARDPY_MODULE", "guardpy"))

RULES = "rule check_value { value == 1 }"
ERROR = "rules is required and must be non-empty"


class WheelTest(unittest.TestCase):
    def test_validation_call_shapes(self):
        for value, expected in ((1, "PASS"), (2, "FAIL")):
            for verbose in (False, True):
                for shape in ("positional", "verbose_keyword", "all_keywords"):
                    with self.subTest(value=value, verbose=verbose, shape=shape):
                        template = '{"value": %d}' % value
                        if shape == "positional":
                            result = guard.validate_with_guard(template, RULES, verbose)
                        elif shape == "verbose_keyword":
                            result = guard.validate_with_guard(
                                template, RULES, verbose=verbose
                            )
                        else:
                            result = guard.validate_with_guard(
                                template_content=template, rules=RULES, verbose=verbose
                            )
                        self.assertEqual(result["tool"], "guard")
                        self.assertIs(result["success"], True)
                        status = result["result"]
                        if verbose:
                            status = status["container"]["FileCheck"]
                        self.assertEqual(status["status"], expected)

    def test_missing_or_empty_rules(self):
        for rules in (None, ""):
            for shape in ("verbose_keyword", "all_keywords"):
                with self.subTest(rules=rules, shape=shape):
                    if shape == "verbose_keyword":
                        result = guard.validate_with_guard(
                            '{"value": 1}', rules, verbose=True
                        )
                    else:
                        result = guard.validate_with_guard(
                            template_content='{"value": 1}', rules=rules, verbose=True
                        )
                    self.assertEqual(result["tool"], "guard")
                    self.assertIs(result["success"], False)
                    self.assertEqual(result["error"], ERROR)

    def test_default_missing_rules(self):
        result = guard.validate_with_guard('{"value": 1}')
        self.assertEqual(result["tool"], "guard")
        self.assertIs(result["success"], False)
        self.assertEqual(result["error"], ERROR)


if __name__ == "__main__":
    unittest.main()
