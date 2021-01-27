from enum import Enum
from dataclasses import dataclass
from typing import NamedTuple, Tuple, Iterable, Set, List, Iterator


class TeamType(int, Enum):
    TWO = 2
    THREE = 3
    FOUR = 4


class Pizza(NamedTuple):
    pizza_id: int
    ingredients: Tuple[str, ...]

    def __repr__(self):
        return f'Pizza({self.pizza_id}, {self.ingredients})'

    def __hash__(self):
        return self.pizza_id


class Order:

    def __init__(self, team: TeamType, pizzas: Iterable[Pizza] = None):
        self._team = team
        self._pizzas = list(pizzas) if pizzas else []

    def add_pizza(self, pizza: Pizza):
        self._pizzas.append(pizza)

    @property
    def team(self) -> int:
        return self._team.value

    @property
    def unique_ingredients(self) -> Set[str]:
        unique_ingredients = set()
        for pizza in self._pizzas:
            unique_ingredients.update(pizza.ingredients)
        return unique_ingredients

    @property
    def score(self) -> int:
        return len(self.unique_ingredients) ** 2

    @property
    def is_full(self) -> bool:
        return len(self._pizzas) == self._team.value

    def __repr__(self):
        return f'Order({self._team}, {self._pizzas})'

    def __len__(self):
        return len(self._pizzas)

    def __iter__(self) -> Iterator[Pizza]:
        return iter(self._pizzas)


class TeamsOverError(Exception):
    pass


@dataclass
class DataSet:
    pizzas: List[Pizza]
    two_team: int
    three_team: int
    four_team: int

    def __post_init__(self):
        self.total_teams = self.two_team + self.three_team + self.four_team

    def create_order(self) -> Order:
        if self.two_team > 0:
            order = Order(team=TeamType.TWO)
            self.two_team -= 1
        elif self.three_team > 0:
            order = Order(team=TeamType.THREE)
            self.three_team -= 1
        elif self.four_team > 0:
            order = Order(team=TeamType.FOUR)
            self.four_team -= 1
        else:
            raise TeamsOverError('Teams are over')

        return order
