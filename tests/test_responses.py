import unittest
from surveylang.models.responses import ResponseInstance, ResponseGroup, ResponseMatrix


class TestResponses(unittest.TestCase):
    def test_response_instance(self):
        response_instance = ResponseInstance(1, "1", 1, 1, 1, 1, 1, 1)
        self.assertEqual(response_instance.val, 1)
        self.assertEqual(response_instance.raw, "1")
        self.assertEqual(response_instance.section_idx, 1)
        self.assertEqual(response_instance.question_idx, 1)
        self.assertEqual(response_instance.battery_idx, 1)
        self.assertEqual(response_instance.segment_idx, 1)
        self.assertEqual(response_instance.item_idx, 1)
        self.assertEqual(response_instance.option_idx, 1)

    def test_response_group(self):
        response_group = ResponseGroup([ResponseInstance(1, "1", 1, 1, 1, 1, 1, 1)])
        self.assertEqual(len(response_group), 1)