from enum import Enum

class SourceEntity(str, Enum):
    internal = "internal"
    external = "external"