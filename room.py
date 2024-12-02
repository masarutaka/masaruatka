from dataclasses import dataclass
from building import Building

@dataclass
class Room:
    building: Building
    floor: str
    rent: str
    management_fee: str
    deposit: str
    gratuity: str
    layout: str
    size: str
    url: str