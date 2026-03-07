from __future__ import annotations

from abc import ABC, abstractmethod

from scripts.lib.models.item import FrontierItem


class Collector(ABC):
    source_type: str

    @abstractmethod
    def collect(self) -> list[FrontierItem]:
        raise NotImplementedError
