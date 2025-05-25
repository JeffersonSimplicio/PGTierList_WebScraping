from typing import Protocol, TypeVar


T = TypeVar("T")


class Assembler(Protocol[T]):
    def assemble(any) -> T: ...
