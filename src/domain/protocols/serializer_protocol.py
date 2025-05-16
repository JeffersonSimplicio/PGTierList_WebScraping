from typing import Protocol, TypeVar, Dict

T = TypeVar("T")
D = TypeVar("D")


class SerializerProtocol(Protocol[T, D]):
    def serialize(obj: T) -> Dict[str, D]: ...
