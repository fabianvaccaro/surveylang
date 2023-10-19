# ----------------------------------------
# Just make an instance of CisaLogicParser() and call the parse(expr) method.
#
# Operators:
#  LT, LTE, GT, GTE and EQ work with Items
#  SLTE, SGTE, SLT, SGT and IN work with Sections
#  ANY, ALL and NOT are logic operators
# ----------------------------------------

from sly import Lexer, Parser


# Abstract CISA Logic classes
class CisaLogic:
    pass


# Abstract CISA Operators

class CisaIndexable():
    def __init__(self, ref: str):
        self.ref: str = ref

    def __str__(self):
        return self.ref


class CisaElemBinaryOperator(CisaLogic):
    """
    Operator with 2 values
    """

    def __init__(self, x: int, t: int | CisaIndexable):
        self.x: int = x
        self.t: int | CisaIndexable = t

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.x == other.x) and (self.t == other.t)

    def __str__(self):
        return '[{} x:{} t:{}]'.format(self.__class__.__name__, str(self.x), str(self.t))  # Force __str__ of elems.


class CisaSectionOperator(CisaElemBinaryOperator):
    def _eval(self, responses_roi: list):
        raise NotImplementedError


class CisaItemOperator(CisaElemBinaryOperator):
    pass


class CisaElemUnaryOperator(CisaLogic):
    """
    Operator with 1 value
    """

    def __init__(self, x: CisaLogic):
        self.x = x

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.x == other.x

    def __str__(self):
        return '[{} x:{}]'.format(self.__class__.__name__, str(self.x))


class CisaRecursiveOperator(CisaLogic):
    """
    Operator with list of values
    """

    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if len(self.v) != len(other.v):
            return False
        return all([sx == ox for (sx, ox) in zip(self.v, other.v)])

    def __str__(self):
        return '[{} v:{}]'.format(self.__class__.__name__, [str(x) for x in self.v])


# Base CISA Indexable Elements


class ItemIndexable(CisaIndexable):
    """
    Basic Item type
    """

    def __eq__(self, other):
        if not isinstance(other, ItemIndexable):
            return False
        return self.ref == other.ref

    def __str__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.ref)


class SectionIndexable(CisaIndexable):
    """
    Basic Section type
    """

    def __eq__(self, other):
        if not isinstance(other, SectionIndexable):
            return False
        return self.ref == other.ref

    def __str__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.ref)


# Section Operators

class IN(CisaSectionOperator):
    pass


class SLTE(CisaSectionOperator):
    pass


class SGTE(CisaSectionOperator):
    pass


class SLT(CisaSectionOperator):
    pass


class SGT(CisaSectionOperator):
    pass


# Item operators
class LTE(CisaItemOperator):
    pass


class GTE(CisaItemOperator):
    pass


class LT(CisaItemOperator):
    pass


class GT(CisaItemOperator):
    pass


class EQ(CisaItemOperator):
    pass


# LOGICAL OPERATORS
class ANY(CisaRecursiveOperator):
    pass


class ALL(CisaRecursiveOperator):
    pass


class NOT(CisaElemUnaryOperator):
    pass


class LogicLexer(Lexer):
    tokens = ('SLTE', 'SGTE', 'SLT', 'SGT', 'LTE', 'GTE', 'ANY', 'ALL', 'AND', 'OR', 'NOT', 'LT',
              'GT', 'EQ', 'IN', 'LPAREN', 'RPAREN', 'COMMA', 'SECTION', 'ITEM', 'NUMBER', 'END')

    # Operadores de logica
    SLTE = r'SLTE'
    SGTE = r'SGTE'
    SLT = r'SLT'
    SGT = r'SGT'
    LTE = r'LTE'
    GTE = r'GTE'
    ANY = r'ANY'
    ALL = r'ALL'
    AND = r'AND'
    NOT = r'NOT'
    OR = r'OR'
    LT = r'LT'
    GT = r'GT'
    EQ = r'EQ'
    IN = r'IN'

    # Cosas que no son logica.
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    SECTION = r'[sS][0-9]+'
    ITEM = r'[iI][0-9]+'
    NUMBER = r'[0-9]+'
    END = r';'

    ignore_spaces = r'[\ \t\n]+'


class LogicParser(Parser):
    tokens = LogicLexer.tokens

    # Grammar rules
    # LOGIC OPERATORS
    @_('ALL LPAREN n_ops RPAREN')
    def op(self, p):
        v = p.n_ops
        return ALL(v=v)

    @_('ANY LPAREN n_ops RPAREN')
    def op(self, p):
        v = p.n_ops
        return ANY(v)

    @_('NOT LPAREN op RPAREN')
    def op(self, p):
        return NOT(p.op)

    @_('op AND op')
    def op(self, p):
        v = [p.op0, p.op1]
        return ALL(v)

    @_('op OR op')
    def op(self, p):
        v = [p.op0, p.op1]
        return ANY(v)

    @_('NOT op')
    def op(self, p):
        return NOT(p.op)

    # DUAL OPERATORS
    @_('SLTE LPAREN number COMMA section RPAREN')
    def op(self, p):
        return SLTE(p.number, p.section)

    @_('SGTE LPAREN number COMMA section RPAREN')
    def op(self, p):
        return SGTE(p.number, p.section)

    @_('SLT LPAREN number COMMA section RPAREN')
    def op(self, p):
        return SLT(p.number, p.section)

    @_('SGT LPAREN number COMMA section RPAREN')
    def op(self, p):
        return SGT(p.number, p.section)

    @_('LTE LPAREN number COMMA item RPAREN')
    def op(self, p):
        return LTE(p.number, p.item)

    @_('GTE LPAREN number COMMA item RPAREN')
    def op(self, p):
        return GTE(p.number, p.item)

    @_('LT LPAREN number COMMA item RPAREN')
    def op(self, p):
        return LT(p.number, p.item)

    @_('GT LPAREN number COMMA item RPAREN')
    def op(self, p):
        return GT(p.number, p.item)

    @_('EQ LPAREN number COMMA item RPAREN')
    def op(self, p):
        return EQ(p.number, p.item)

    @_('IN LPAREN number COMMA section RPAREN')
    def op(self, p):
        return IN(p.number, p.section)

    @_('op END')
    def op(self, p):
        return p.op

    # GENERIC OPERATIONS AND COMMA AGGRUPATOR
    @_('op COMMA n_ops')
    def n_ops(self, p):
        res = [p.op]
        res.extend(p.n_ops)
        return res

    @_('op')
    def n_ops(self, p):
        return [p.op]

    # BASE ELEMS
    @_('ITEM')
    def item(self, p):
        return ItemIndexable(p.ITEM)

    @_('SECTION')
    def section(self, p):
        return SectionIndexable(p.SECTION)

    @_('NUMBER')
    def number(self, p):
        res = int(p.NUMBER)
        return res


class CisaLogicParser:
    """
    Just import this and use the parse method
    """

    def __init__(self):
        self.lexer = LogicLexer()
        self.parser = LogicParser()

    def parse(self, expr) -> CisaLogic:
        tokenized_lx = self.lexer.tokenize(expr)
        res = self.parser.parse(tokenized_lx)
        return res


class CisaLogicEvaluator():
    def __init__(self, ref_dict: dict[str, int], section_responses: list[list[int]]):
        self.ref_dict = ref_dict
        self.section_responses = section_responses
        self.item_responses = [item for row in self.section_responses for item in row]

    def _get_responses_roi_for_section(self, t: int | CisaIndexable) -> list[int]:
        index = self.ref_dict[t.ref] if isinstance(t, CisaIndexable) else t
        return self.section_responses[index]

    def _get_response_for_item(self, t: int | CisaIndexable) -> int:
        index = self.ref_dict[t.ref] if isinstance(t, CisaIndexable) else t
        return self.item_responses[index]

    def _eval_in(self, logic: IN) -> bool:
        """
        Evaluate IN operator
        """
        responses_roi = self._get_responses_roi_for_section(logic.t)
        return logic.x in responses_roi

    def _eval_slt(self, logic: SLT) -> bool:
        """
        Evaluate SLT operator
        """
        responses_roi = self._get_responses_roi_for_section(logic.t)
        return any([x < logic.x for x in responses_roi])

    def _eval_slte(self, logic: SLTE) -> bool:
        """
        Evaluate SLTE operator
        """
        responses_roi = self._get_responses_roi_for_section(logic.t)
        return any([x <= logic.x for x in responses_roi])

    def _eval_sgt(self, logic: SGT) -> bool:
        """
        Evaluate SGT operator
        """
        responses_roi = self._get_responses_roi_for_section(logic.t)
        return any([x > logic.x for x in responses_roi])

    def _eval_sgte(self, logic: SGTE) -> bool:
        """
        Evaluate SGTE operator
        """
        responses_roi = self._get_responses_roi_for_section(logic.t)
        return any([x >= logic.x for x in responses_roi])

    def _eval_eq(self, logic: EQ) -> bool:
        """
        Evaluate EQ operator
        """
        response_roi = self._get_response_for_item(logic.t)
        return response_roi == logic.x

    def _eval_lt(self, logic: LT) -> bool:
        """
        Evaluate LT operator
        """
        response_roi = self._get_response_for_item(logic.t)
        return response_roi < logic.x

    def _eval_lte(self, logic: LTE) -> bool:
        """
        Evaluate LTE operator
        """
        response_roi = self._get_response_for_item(logic.t)
        return response_roi <= logic.x

    def _eval_gt(self, logic: GT) -> bool:
        """
        Evaluate GT operator
        """
        response_roi = self._get_response_for_item(logic.t)
        return response_roi > logic.x

    def _eval_gte(self, logic: GTE) -> bool:
        """
        Evaluate GTE operator
        """
        response_roi = self._get_response_for_item(logic.t)
        return response_roi >= logic.x

    def _eval_not(self, logic: NOT) -> bool:
        """
        Evaluate NOT operator
        """
        return not self.eval(logic.x)

    def eval(self, logic: CisaLogic) -> bool:
        if isinstance(logic, CisaRecursiveOperator):
            if isinstance(logic, ANY):
                return any([self.eval(x) for x in logic.v])
            if isinstance(logic, ALL):
                return all([self.eval(x) for x in logic.v])
        if isinstance(logic, CisaSectionOperator):
            if isinstance(logic, IN):
                return self._eval_in(logic)
            if isinstance(logic, SLT):
                return self._eval_slt(logic)
            if isinstance(logic, SLTE):
                return self._eval_slte(logic)
            if isinstance(logic, SGT):
                return self._eval_sgt(logic)
            if isinstance(logic, SGTE):
                return self._eval_sgte(logic)
        if isinstance(logic, CisaItemOperator):
            if isinstance(logic, EQ):
                return self._eval_eq(logic)
            if isinstance(logic, LT):
                return self._eval_lt(logic)
            if isinstance(logic, LTE):
                return self._eval_lte(logic)
            if isinstance(logic, GT):
                return self._eval_gt(logic)
            if isinstance(logic, GTE):
                return self._eval_gte(logic)
        if isinstance(logic, CisaElemUnaryOperator):
            if isinstance(logic, NOT):
                return self._eval_not(logic)
        else:
            return False
