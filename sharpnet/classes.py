from dataclasses import dataclass, field


@dataclass
class Container():
    """
    Container class for all objects in the sharpnet package.
    """
    name: str


@dataclass
class CacheData():
    """
    CacheData class for all objects in the sharpnet package.
    """

    mercy: bool = field(default=True)
    servers: list[str] = field(default_factory=list)
