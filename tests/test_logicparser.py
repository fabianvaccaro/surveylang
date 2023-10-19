import unittest
from surveylang.logicelements.logicparser import CisaLogicParser
from surveylang.logicelements.logicparser import ItemIndexable, SectionIndexable
from surveylang.logicelements.logicparser import LT, LTE, GT, GTE, EQ
from surveylang.logicelements.logicparser import SLT, SLTE, SGT, SGTE, IN
from surveylang.logicelements.logicparser import ANY, ALL, \
    NOT  # OR y AND son simplemente ANY(x1,x2) y ALL(x1,x2) respectivamente.
from surveylang.logicelements.logicparser import CisaLogicEvaluator


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cisaparser = CisaLogicParser()
        self.section_responses = [
            [1, 2, 3],
            [9],
            [10, 11],
            [8],
            [99]
        ]

        self.ref_index_dict: dict[str, int] = {
            'S1': 0,
            'S2': 1,
            'S3': 2,
            'S4': 3,
            'S5': 4,
            'I1': 0,
            'I2': 1,
            'I3': 2,
            'I4': 3,
            'I5': 4,
            'I6': 5,
            'I7': 6,
            'I8': 7,
            '@HERE': 1,
            '@NEXT': 2
        }

    def test_slt(self):
        expr = 'SLT(7, S1)'
        parsed = self.cisaparser.parse(expr)
        manual = SLT(7, SectionIndexable('S1'))
        self.assertEqual(parsed, manual, msg="Error de parseo para SLT")

    def test_slte(self):
        expr = 'SLTE(2, S1)'
        parsed = self.cisaparser.parse(expr)
        manual = SLTE(2, SectionIndexable(ref='S1'))
        self.assertEqual(parsed, manual, msg="Error de parseo para SLTE")

    def test_any_with_3_elems(self):
        expr = 'ANY(SLTE(2,S1), SGTE(5,S4), SLTE(6, S5))'
        parsed = self.cisaparser.parse(expr)
        manual = ANY([SLTE(2, SectionIndexable('S1'), ),
                      SGTE(5, SectionIndexable('S4')),
                      SLTE(6, SectionIndexable('S5'))])
        self.assertEqual(parsed, manual, msg="Error de parseo para ANY")

    def test_all_only_one_elem(self):
        expr = 'ALL(SLTE(2,S1));'
        parsed = self.cisaparser.parse(expr)
        manual = ALL([SLTE(2, SectionIndexable('S1'))])
        self.assertEqual(parsed, manual, msg="Error de parseo para ALL")

    def test_any_2_elems(self):
        expr = 'ANY(LT(2, I1),SLT(6, S5))'
        parsed = self.cisaparser.parse(expr)
        manual = ANY([LT(2, ItemIndexable('I1')),
                      SLT(6, SectionIndexable('S5'))])
        self.assertEqual(parsed, manual, msg="Error de parseo para ANY")

    def test_and(self):
        expr = 'SGTE(2, S1) AND GTE(6, I5)'
        parsed = self.cisaparser.parse(expr)
        manual = ALL([SGTE(2, SectionIndexable('S1')),
                      GTE(6, ItemIndexable('I5'))])
        self.assertEqual(parsed, manual, msg="Error de parseo para AND")

    def test_not_or(self):
        expr = 'NOT EQ(2, I1) OR GT(6, I5)'
        parsed = self.cisaparser.parse(expr)
        manual = NOT(ANY([EQ(2, ItemIndexable('I1')),
                          GT(6, ItemIndexable('I5'))]))
        self.assertEqual(parsed, manual, msg="Error de parseo para AND")

    def test_other_expressions(self):
        expr = '    ANY ( LTE( 4, I3 ), SGT(9,S2), IN(4,S3) AND NOT(EQ(5,I12))) '
        parsed = self.cisaparser.parse(expr)
        manual = ANY([LTE(4, ItemIndexable('I3')),
                      SGT(9, SectionIndexable('S2')),
                      ALL([IN(4, SectionIndexable('S3')),
                           NOT(EQ(5, ItemIndexable('I12')))])])
        self.assertEqual(parsed, manual,
                         msg="Error de parseo:\n Resultado: {}\n Esperado: {}".format(str(parsed), str(manual)))

    def test_eval_in(self):
        expr = 'IN(2, S1)'
        parsed = self.cisaparser.parse(expr)
        evaluator = CisaLogicEvaluator(ref_dict=self.ref_index_dict, section_responses=self.section_responses)
        res = evaluator.eval(parsed)
        self.assertTrue(res)

    def test_eval_not_in(self):
        expr = 'NOT IN(8, S1)'
        parsed = self.cisaparser.parse(expr)
        evaluator = CisaLogicEvaluator(ref_dict=self.ref_index_dict, section_responses=self.section_responses)
        res = evaluator.eval(parsed)
        self.assertTrue(res)

    def test_eval_gt(self):
        expr = 'GT(8, I4)'
        parsed = self.cisaparser.parse(expr)
        evaluator = CisaLogicEvaluator(ref_dict=self.ref_index_dict, section_responses=self.section_responses)
        res = evaluator.eval(parsed)
        self.assertTrue(res)

    def test_eval_gte(self):
        expr = 'GTE(11, I6)'
        parsed = self.cisaparser.parse(expr)
        evaluator = CisaLogicEvaluator(ref_dict=self.ref_index_dict, section_responses=self.section_responses)
        res = evaluator.eval(parsed)
        self.assertTrue(res)

    def test_eval_any(self):
        expr = 'ANY(GT(8, I4), GT(16, I6))'
        parsed = self.cisaparser.parse(expr)
        evaluator = CisaLogicEvaluator(ref_dict=self.ref_index_dict, section_responses=self.section_responses)
        res = evaluator.eval(parsed)
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
