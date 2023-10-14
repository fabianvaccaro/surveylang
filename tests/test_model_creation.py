import unittest
from surveylang.models.instrument_component_base import InstrumentComponentBase
from surveylang.models import instrument_components as components


class TestModelCreation(unittest.TestCase):
    def test_model_creation(self):
        instrument_component_base = InstrumentComponentBase()
        instrument_component_base.set_shortname("shortname")
        self.assertEqual(instrument_component_base.get_shortname(), "shortname")

    def test_add_option(self):
        option1 = components.Option()
        option1.set_value(1)
        option1.set_text("option1")

        item1 = components.Item()
        item1.set_shortname("item1")

        item1.add_child(option1)

        self.assertEqual(item1.get_options()[0].get_value(), 1)

    def test_sequential_add(self):
        option1 = components.Option()
        option1.set_value(1)
        option1.set_text("option1")

        option2 = components.Option()
        option2.set_value(2)
        option2.set_text("option2")

        item1 = components.Item()
        item1.set_shortname("item1")

        item1.add_child(option1)
        item1.add_child(option2)

        self.assertTrue(item1.verify())


if __name__ == '__main__':
    unittest.main()
