import json
from pathlib import Path
from typing import Dict

Scores = Dict[str, int]

class ScoreCache:

    def __init__(self, src: Path):
        self.src = src
        if not src.exists():
            self.clear()

    def set(self, key: str,  score: int):
        scores = self._load_scores()
        scores[key] = max(score, scores.get(key, 0))
        self._save_scores(scores)

    def get(self, key: str) -> int:
        scores = self._load_scores()
        return int(scores.get(key, 0))

    def clear(self):
        self._save_scores(dict())

    def _load_scores(self) -> Scores:
        with self.src.open() as file:
            return json.load(file)

    def _save_scores(self, scores: Scores):
        with self.src.open('w') as file:
            json.dump(scores, file, indent=4)
