from collections.abc import Iterable

class WatchlistManager:
    def __init__(self):
        self._symbols: set[str] = set()

    def update(self, symbols: Iterable[str]) -> None:
        self._symbols = set(symbols)

    @property
    def symbols(self) -> list[str]:
        return sorted(self._symbols)