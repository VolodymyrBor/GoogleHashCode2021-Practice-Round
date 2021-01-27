from typing import List
from abc import ABC, abstractmethod

from rich.progress import track

from pizza_structures import DataSet, Order, TeamType, TeamsOverError


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
                try:
                    order = dataset.create_order()
                except TeamsOverError:
                    break
            order.add_pizza(pizza)
            if order.is_full:
                orders.append(order)
                order = None

        return orders[:-1]


class GridStrategy(StrategyBase):

    @staticmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        orders = [dataset.create_order() for _ in range(dataset.total_teams)]

        for order in track(orders, description='Order processing...'):

            if not dataset.pizzas:
                break

            for _ in range(order.team):

                if not dataset.pizzas:
                    break

                best_pizza_index = 0
                best_pizza_score = 0
                for i, pizza in enumerate(dataset.pizzas):
                    order_ingredients = order.unique_ingredients
                    score = len(order_ingredients | set(pizza.ingredients)) ** 2
                    if score > best_pizza_score:
                        best_pizza_index = i
                        best_pizza_score = score

                best_pizza = dataset.pizzas.pop(best_pizza_index)
                order.add_pizza(best_pizza)

        return [order for order in orders if order.is_full]
