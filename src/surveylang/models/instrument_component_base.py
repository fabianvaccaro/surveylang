import uuid
from surveylang.common.enumerators import ComponentType
from typing import Generic, TypeVar, Mapping, Iterator
from surveylang.logicelements.logicparser import CisaLogicParser


class InstrumentComponentBase:
    """
    InstrumentComponentBase is the base class that allows a survey component to be traceable.
    The class is used to generate a unique identifier for each survey component.
    """

    def __init__(self):
        self._uid: str = str(uuid.uuid4())
        self._position: int = 0
        self._component_type: ComponentType = ComponentType.BASE
        self._ref: str | None = None  # Bibliographic reference of the component
        self._shortname: str | None = None  # Short name of the component
        self._alias: str | None = None  # Alias of the component

    def get_uid(self) -> str:
        return self._uid

    def get_shortname(self) -> str:
        return self._shortname

    def set_shortname(self, shortname: str):
        self._shortname = shortname

    def get_alias(self) -> str:
        return self._alias

    def set_alias(self, alias: str):
        self._alias = alias

    def get_type(self) -> ComponentType:
        return self._component_type

    def set_type(self, component_type: ComponentType):
        self._component_type = component_type

    def get_ref(self) -> str:
        return self._ref

    def set_ref(self, ref: str):
        self._ref = ref

    def get_position(self) -> int:
        return self._position

    def set_position(self, position: int):
        self._position = position

    def build(self):
        return self

    def verify(self) -> bool:
        raise NotImplementedError()

    def __str__(self):
        return f"{self.__class__.__name__}({self._component_type})({self._uid})"

    def __repr__(self):
        return self.__str__()


class InstrumentLogicExpression():
    def __init__(self, expr: str, target: str):
        self._expr = expr
        self.target = target
        parser = CisaLogicParser()
        self._parsed_expr = parser.parse(expr)

    def get_expr(self) -> str:
        return self._expr

    def get_target(self) -> str:
        return self.target

    def get_cisa_logic(self):
        return self._parsed_expr

    def __str__(self):
        return f'{self._expr} | {self.target}'


class InstrumentLogicBlock():
    def __init__(self, expressions: list[InstrumentLogicExpression] | None = None, target: str = '@NEXT'):
        if expressions is None:
            expressions = []
        self._expressions: list[InstrumentLogicExpression] = expressions
        self._target = target

    def get_target(self) -> str:
        return self._target

    def get_expressions(self) -> list[InstrumentLogicExpression]:
        return self._expressions

    def add_expression(self, expression: InstrumentLogicExpression):
        self._expressions.append(expression)

    def remove_expression(self, expression: InstrumentLogicExpression):
        self._expressions.remove(expression)

    def clear_expressions(self):
        self._expressions.clear()

    def insert_expression_at(self, position: int, expression: InstrumentLogicExpression):
        self._expressions.insert(position, expression)

    def move_expression(self, position: int, expression: InstrumentLogicExpression):
        self._expressions.remove(expression)
        self.insert_expression_at(position, expression)

    def move_expression_to_end(self, expression: InstrumentLogicExpression):
        self._expressions.remove(expression)
        self.add_expression(expression)

    def move_expression_to_start(self, expression: InstrumentLogicExpression):
        self._expressions.remove(expression)
        self.insert_expression_at(0, expression)

    def move_expression_up(self, expression: InstrumentLogicExpression):
        position = self._expressions.index(expression)
        if position == 0:
            raise ValueError("Cannot move expression up")
        self.move_expression(position - 1, expression)

    def move_expression_down(self, expression: InstrumentLogicExpression):
        position = self._expressions.index(expression)
        if position == len(self._expressions) - 1:
            raise ValueError("Cannot move expression down")
        self.move_expression(position + 1, expression)

    def __str__(self):
        return f'{self._expressions}'


T = TypeVar('T', bound=InstrumentComponentBase)


class InstrumentComponentBaseWithChildren(Generic[T], InstrumentComponentBase):
    """
    InstrumentComponentBaseWithChildren is the base class that allows a survey component to have children.
    The class is used to generate a unique identifier for each survey component.
    """

    def __init__(self):
        super().__init__()
        self._children: list[T] = []

    def get_children(self) -> list[T]:
        return self._children

    def add_child(self, child: T):
        self.insert_child_at(len(self._children), child)

    def remove_child(self, child: T):
        self._children.remove(child)
        child.set_position(-1)

    def clear_children(self):
        self._children.clear()

    def get_child_by_uid(self, uid: str) -> T:
        for child in self._children:
            if child.get_uid() == uid:
                return child
        raise ValueError(f"Child with id {uid} not found")

    def insert_child_at(self, position: int, child: T):
        self._children.insert(position, child)
        child.set_position(position)

    def move_child(self, position: int, child: T):
        self._children.remove(child)
        self.insert_child_at(position, child)

    def move_child_to_end(self, child: T):
        self._children.remove(child)
        self.add_child(child)

    def move_child_to_start(self, child: T):
        self._children.remove(child)
        self.insert_child_at(0, child)

    def move_child_up(self, child: T):
        position = self._children.index(child)
        if position == 0:
            raise ValueError("Cannot move child up")
        self.move_child(position - 1, child)
        child.set_position(position - 1)

    def move_child_down(self, child: T):
        position = self._children.index(child)
        if position == len(self._children) - 1:
            raise ValueError("Cannot move child down")
        self.move_child(position + 1, child)
        child.set_position(position + 1)

    def build(self):
        for i in range(len(self._children)):
            self._children[i].set_position(i)
            self._children[i].build()
        return self

    def verify(self) -> bool:
        return self.verify_children()

    def verify_children(self) -> bool:
        for i in range(len(self._children)):
            if not self._children[i].get_position() == i:
                return False
            if isinstance(self._children[i], InstrumentComponentBaseWithChildren):
                if not self._children[i].verify_children():
                    return False
        return True

    def __iter__(self) -> Iterator[T]:
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def __getitem__(self, index: int) -> T:
        return self._children[index]

    def __setitem__(self, index: int, value: T):
        self._children[index] = value

    def __delitem__(self, index: int):
        del self._children[index]

    def __contains__(self, item: T) -> bool:
        return item in self._children

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._children)


class InstrumentComponentBaseWithLogic(Generic[T], InstrumentComponentBaseWithChildren[T]):
    def __init__(self):
        super().__init__()
        self._entry_logic: InstrumentLogicBlock | None = None
        self._exit_logic: InstrumentLogicBlock | None = None
        self._title: str | None = None  # Title of the segment
        self._subtitle: str | None = None  # Subtitle of the segment
        self._qnid: str | None = None  # Question Number Identifier of the segment

    def get_entry_logic(self) -> InstrumentLogicBlock:
        return self._entry_logic

    def set_entry_logic(self, entry_logic: InstrumentLogicBlock):
        self._entry_logic = entry_logic

    def get_exit_logic(self) -> InstrumentLogicBlock:
        return self._exit_logic

    def set_exit_logic(self, exit_logic: InstrumentLogicBlock):
        self._exit_logic = exit_logic

    def get_title(self) -> str:
        return self._title

    def set_title(self, title: str):
        self._title = title

    def get_subtitle(self) -> str:
        return self._subtitle

    def set_subtitle(self, subtitle: str):
        self._subtitle = subtitle

    def get_qnid(self) -> str:
        return self._qnid

    def set_qnid(self, qnid: str):
        self._qnid = qnid
