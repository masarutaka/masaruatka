from dataclasses import dataclass
from typing import List

@dataclass
class Building:
    name: str
    address: str
    stations: List[str]
    age: str
    floors: str