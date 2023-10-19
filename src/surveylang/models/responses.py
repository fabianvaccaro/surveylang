from typing import Generic, TypeVar, Mapping, Iterator


class ResponseInstance(object):
    def __init__(self, val: int, raw: str, section_idx: int, question_idx: int, battery_idx: int, segment_idx: int,
                 item_idx: int, option_idx: int):
        self.val = val
        self.raw = raw
        self.section_idx = section_idx
        self.question_idx = question_idx
        self.battery_idx = battery_idx
        self.segment_idx = segment_idx
        self.item_idx = item_idx
        self.option_idx = option_idx

    def __str__(self):
        return self.raw

    def __int__(self):
        return self.val


T = TypeVar('T')


class IterableResponseBase(Generic[T]):
    def __init__(self, elements: list[T]):
        self._elements = elements

    def __iter__(self):
        self.i = 0
        return iter(self._elements)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, idx):
        return self._elements[idx]

    def __next__(self):
        if self.i >= len(self._elements):
            raise StopIteration
        x = self._elements[self.i]
        self.i += 1
        return x

    def append(self, response: ResponseInstance):
        self._elements.append(response)

    def extend(self, responses: list[ResponseInstance]):
        self._elements.extend(responses)

    def insert(self, index: int, response: ResponseInstance):
        self._elements.insert(index, response)

    def remove(self, response: ResponseInstance):
        self._elements.remove(response)

    def get_iterator(self) -> Iterator[T]:
        return iter(self._elements)


class ResponseGroup(IterableResponseBase[ResponseInstance]):
    def __init__(self, responses: list[ResponseInstance]):
        super().__init__(responses)


class ResponseMatrix(IterableResponseBase[ResponseGroup]):
    def __init__(self, response_groups: list[ResponseGroup]):
        super().__init__(response_groups)

    def get_response_matrix(self):
        matrix = [[ri.val for ri in rg.get_iterator()] for rg in self.get_iterator()]
        return matrix
