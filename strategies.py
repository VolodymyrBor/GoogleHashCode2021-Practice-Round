from typing import List
from abc import ABC, abstractmethod

from rich.progress import track

from pizza_structures import DataSet, Order, TeamType


class StrategyBase(ABC):

    @staticmethod
    @abstractmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        pass


class SortStrategy(StrategyBase):

    @staticmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        orders = []
        pizzas = sorted(dataset.pizzas, key=lambda p: len(p.ingredients), reverse=True)

        order = None
        for pizza in track(pizzas, description='Creating Orders...'):
            if not order:
                if dataset.two_team:
                    order = Order(team=TeamType.TWO)
                    dataset.two_team -= 1
                elif dataset.three_team:
                    order = Order(team=TeamType.THREE)
                    dataset.three_team -= 1
                elif dataset.four_team:
                    order = Order(team=TeamType.FOUR)
                    dataset.four_team -= 1
                else:
                    break
            order.add_pizza(pizza)
            if order.is_full:
                orders.append(order)
                order = None

        return orders
