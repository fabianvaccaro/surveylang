from surveylang.models.instrument_component_base import InstrumentComponentBase, InstrumentComponentBaseWithChildren, \
    InstrumentComponentBaseWithLogic
from surveylang.common.enumerators import ComponentType, ItemType
from typing import Generic, TypeVar, Mapping, Iterator


class Option(InstrumentComponentBase):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.OPTION
        self._raw_value: str | None = None  # Raw value of the option
        self._value: int | None = None  # Value of the option
        self._text: str | None = None  # Text of the option
        self._exclusive: bool = False  # Exclusive option

    def get_raw_value(self) -> str:
        return self._raw_value

    def set_raw_value(self, raw_value: str):
        self._raw_value = raw_value

    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int):
        self._value = value
        self._raw_value = str(value)

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str):
        self._text = text

    def get_exclusive(self) -> bool:
        return self._exclusive

    def set_exclusive(self, exclusive: bool):
        self._exclusive = exclusive

    def verify(self) -> bool:
        return True

    def __int__(self):
        return self._value

    def __str__(self):
        return self._raw_value


class Item(InstrumentComponentBaseWithChildren[Option]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.ITEM
        self._item_type: ItemType | None = ItemType.BASE  # Type of the item
        self._text: str | None = None  # Text of the item
        self._display_logic_string: str | None = None  # Display logic of the item
        self._deal_breaker: bool = False  # Specifies if the item is a deal-breaker

    def get_options(self) -> list[Option]:
        return self._children

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str):
        self._text = text

    def get_display_logic_string(self) -> str:
        return self._display_logic_string

    def set_display_logic_string(self, display_logic_string: str):
        self._display_logic_string = display_logic_string

    def is_deal_breaker(self) -> bool:
        return self._deal_breaker

    def set_deal_breaker(self, deal_breaker: bool):
        self._deal_breaker = deal_breaker

    def __str__(self):
        return self._text


ITM = TypeVar('ITM', bound=InstrumentComponentBase)


class ItemText(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.TEXT


class ItemNumeric(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.NUMERIC
        self._max_value: int | None = None  # Maximum value of the item
        self._min_value: int | None = None  # Minimum value of the item

    def get_max_value(self) -> int:
        return self._max_value

    def set_max_value(self, max_value: int):
        self._max_value = max_value

    def get_min_value(self) -> int:
        return self._min_value

    def set_min_value(self, min_value: int):
        self._min_value = min_value


class ItemDate(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.DATE
        self._max_date: str | None = None  # Maximum date of the item
        self._min_date: str | None = None  # Minimum date of the item

    def get_max_date(self) -> str:
        return self._max_date

    def set_max_date(self, max_date: str):
        self._max_date = max_date

    def get_min_date(self) -> str:
        return self._min_date

    def set_min_date(self, min_date: str):
        self._min_date = min_date


class ItemCheckbox(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.CHECKBOX


class ItemList(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.LIST


class ItemLikertN(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.LIKERT_N


class ItemInfoText(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.INFO_TEXT


class ItemDoesNotKnow(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.DOES_NOT_KNOW
        self._deal_breaker = True


class ItemDoesNotApply(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.DOES_NOT_APPLY
        self._deal_breaker = True


class ItemRefusedToAnswer(Item):
    def __init__(self):
        super().__init__()
        self._item_type = ItemType.REFUSED_TO_ANSWER
        self._deal_breaker = True


class Segment(InstrumentComponentBaseWithLogic[Item]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.SEGMENT

    def get_items(self) -> list[Item]:
        return self._children


class Battery(InstrumentComponentBaseWithLogic[Segment]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.BATTERY

    def get_segments(self) -> list[Segment]:
        return self._children


class Question(InstrumentComponentBaseWithLogic[Battery]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.QUESTION

    def get_batteries(self) -> list[Battery]:
        return self._children


class Section(InstrumentComponentBaseWithLogic[Question]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.SECTION

    def get_questions(self) -> list[Question]:
        return self._children


class Questionnaire(InstrumentComponentBaseWithLogic[Section]):
    def __init__(self):
        super().__init__()
        self._component_type = ComponentType.QUESTIONNAIRE

    def get_sections(self) -> list[Section]:
        return self._children
