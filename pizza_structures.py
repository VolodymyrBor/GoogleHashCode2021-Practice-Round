from enum import Enum
from typing import NamedTuple, Tuple, Iterable, Set, List


class TeamType(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4


class Pizza(NamedTuple):
    pizza_id: int
    ingredients: Tuple[str, ...]

    def __repr__(self):
        return f'Pizza({self.pizza_id}, {self.ingredients})'


class Order:

    def __init__(self, team: TeamType, pizzas: Iterable[Pizza] = None):
        self._team = team
        self._pizzas = list(pizzas) if pizzas else []

    def add_pizza(self, pizza: Pizza):
        self._pizzas.append(pizza)

    @property
    def unique_ingredients(self) -> Set[str]:
        unique_ingredients = set()
        for pizza in self._pizzas:
            unique_ingredients.update(pizza.ingredients)
        return unique_ingredients

    @property
    def score(self) -> int:
        return len(self.unique_ingredients) ** 2

    def __repr__(self):
        return f'Order({self._team}, {self._pizzas})'


class DataSet(NamedTuple):
    pizzas: List[]
