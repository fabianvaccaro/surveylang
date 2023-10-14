from enum import Enum


class ComponentType(Enum):
    """
    ComponentType is an enumeration of the different types of survey components.
    """
    QUESTIONNAIRE = 0
    SECTION = 1
    QUESTION = 2
    BATTERY = 3
    SEGMENT = 4
    ITEM = 5
    OPTION = 6
    BASE = 99


class ItemType(Enum):
    """
    ItemTypes is an enumeration of the different types of items inside a segment.
    """
    TEXT = 0
    NUMERIC = 1
    DATE = 2
    CHECKBOX = 3
    LIST = 4
    LIKERT_N = 5
    COMPARE = 6
    RANK = 7
    RATING = 8

    UPLOAD_IMAGE = 11
    UPLOAD_FILE = 12

    INFO_TEXT = 21
    INFO_IMAGE = 22
    INFO_VIDEO = 23
    INFO_AUDIO = 24
    INFO_FILE = 25
    INFO_LINK = 26
    INFO_HTML = 27
    INFO_MAP = 28
    INFO_GEOLOCATION = 29
    INFO_SIGNATURE = 30
    INFO_BARCODE = 31
    INFO_QR_CODE = 32

    DOES_NOT_KNOW = 91
    DOES_NOT_APPLY = 92
    REFUSED_TO_ANSWER = 93
    BASE = 99
