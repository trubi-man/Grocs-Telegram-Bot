from dataclasses import dataclass
from enum import Enum

@dataclass
class SubscriptionData:
    type_sub: str
    price: int
    daily_limit: int

class Subscription(Enum):
    STANDARD = SubscriptionData("standard", 1, 130)
    PRO = SubscriptionData("pro", 2, 400)
    PREMIUM = SubscriptionData("premium", 3, 1000)