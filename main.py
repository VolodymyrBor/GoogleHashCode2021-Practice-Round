from pathlib import Path
from typing import List, Type

from rich.text import Text
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint

import strategies
import input_data
import output_data
from common import measure
from score_cache import ScoreCache
from pizza_structures import Pizza, DataSet, Order

OUTPUT_MAPPING = {
    input_data.A_FILE: output_data.A_OUTPUT,
    input_data.B_FILE: output_data.B_OUTPUT,
    input_data.C_FILE: output_data.C_OUTPUT,
    input_data.D_FILE: output_data.D_OUTPUT,
    input_data.E_FILE: output_data.E_OUTPUT,
}

cache = ScoreCache(output_data.SCORES_FILE)


def load_dateset(src: Path) -> DataSet:
    pizzas = []

    with src.open() as file:
        pizzas_len, two_team, three_team, four_team = map(int, file.readline().split())
        for i, line in track(enumerate(file), description=f'[{src.name}]Loading file...', total=pizzas_len):
            _, *ingredients = line.split()
            pizzas.append(Pizza(i, ingredients))

    return DataSet(
        pizzas=pizzas,
        two_team=two_team,
        three_team=three_team,
        four_team=four_team,
    )


def generate_output(des: Path, orders: List[Order]):
    total_score = 0
    with des.open('w') as file:
        file.write(f'{len(orders)}\n')
        for order in track(orders, description=f'[{des.name}]Writing output...'):
            pizzas_indexes = ' '.join(str(pizza.pizza_id) for pizza in order)
            file.write(f'{order.team} {pizzas_indexes}\n')
            total_score += order.score

    cashed_score = cache.get(des.name)
    score_delta = total_score - cashed_score
    if score_delta >= 0:
        delta_color = 'green'
        delta_text = f'+{score_delta}'
    else:
        delta_color = 'red'
        delta_text = f'-{score_delta}'

    text = Text()
    text.append(f'[{des.name}] ', style='red')
    text.append(f'Total Score = ')
    text.append(f'{total_score} ', style='blue')
    text.append(f'[{delta_text}] ', style=f'bold {delta_color}')
    text.append('points')
    rprint(text)

    cache.set(des.name, total_score)

def main(strategy: Type[strategies.StrategyBase]):
    for src, dst in OUTPUT_MAPPING.items():
        rprint(Panel('Start Processing...', title=src.name, style='dark_cyan'))
        dataset = load_dateset(src)
        with measure('Creating orders'):
            orders = strategy.create_orders(dataset)
        generate_output(dst, orders)


if __name__ == '__main__':
    main(strategy=strategies.SortStrategy)
