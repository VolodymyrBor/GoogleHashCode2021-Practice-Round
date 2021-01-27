from typing import List
from abc import ABC, abstractmethod
from collections import deque, Counter

from rich.progress import track

from common import flatten_chain
from pizza_structures import DataSet, Order, TeamsOverError


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

        return orders


class GridStrategy(StrategyBase):

    @staticmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        orders = [dataset.create_order() for _ in range(dataset.total_teams)]

        for order in track(orders, description='Order processing...'):
            for _ in range(order.team):

                if not dataset.pizzas:
                    break

                best_pizza_index = 0
                best_pizza_score = 0
                for i, pizza in enumerate(dataset.pizzas):
                    score = len(order.unique_ingredients | set(pizza.ingredients)) ** 2
                    if score > best_pizza_score:
                        best_pizza_index = i
                        best_pizza_score = score

                best_pizza = dataset.pizzas.pop(best_pizza_index)
                order.add_pizza(best_pizza)

        return [order for order in orders if order.is_full]


class MaxPLusMinStrategy(StrategyBase):

    @staticmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        pizzas = sorted(dataset.pizzas, key=lambda p: len(p.ingredients), reverse=True)
        orders = [dataset.create_order() for _ in range(dataset.total_teams)]

        pizzas = deque(pizzas)

        for order in track(orders, description='Processing orders'):

            if len(pizzas) < order.team:
                break

            order.add_pizza(pizzas.popleft())
            for _ in range(order.team - 1):
                order.add_pizza(pizzas.pop())

        return [order for order in orders if order.is_full]


class IngredientsFrequencyStrategy(StrategyBase):

    @staticmethod
    def create_orders(dataset: DataSet) -> List[Order]:
        all_ingredients = flatten_chain(pizza.ingredients for pizza in dataset.pizzas)
        ingredients_frequency = Counter(all_ingredients)

        pizza_scores = {
            pizza: sum(ingredients_frequency[item] for item in pizza.ingredients)
            for pizza in dataset.pizzas
        }

        orders = []
        pizzas = sorted(dataset.pizzas, key=lambda p: pizza_scores[p], reverse=True)

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

        return orders
