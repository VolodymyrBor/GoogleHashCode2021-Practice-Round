from contextlib import contextmanager
from typing import Iterable, Generator
from timeit import default_timer as timer

from rich.text import Text
from rich import print as rprint


@contextmanager
def measure(text: str):
    start = timer()
    try:
        yield
    finally:
        delta = timer() - start
        text = Text(f'Time spent on {text}: ')
        text.append(f'{delta:f}s', style='blue')
        rprint(text)


def flatten_chain(iterable: Iterable[Iterable]) -> Generator:
    for item in iterable:
        yield from item
