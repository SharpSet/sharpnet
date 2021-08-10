from dataclasses import dataclass, field

@dataclass
class Container():
    name: str

@dataclass
class CacheData():
    mercy: bool = field(default=True)
    servers: list[str] = field(default_factory=list)

