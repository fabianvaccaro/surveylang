import uuid
from surveylang.common.enumerators import ComponentType
from typing import Generic, TypeVar, Mapping, Iterator


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
        self._entry_logic_string: str | None = None
        self._exit_logic_string: str | None = None
        self._title: str | None = None  # Title of the segment
        self._subtitle: str | None = None  # Subtitle of the segment
        self._qnid: str | None = None  # Question Number Identifier of the segment

    def get_entry_logic_string(self) -> str:
        return self._entry_logic_string

    def set_entry_logic_string(self, entry_logic_string: str):
        self._entry_logic_string = entry_logic_string

    def get_exit_logic_string(self) -> str:
        return self._exit_logic_string

    def set_exit_logic_string(self, exit_logic_string: str):
        self._exit_logic_string = exit_logic_string

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
