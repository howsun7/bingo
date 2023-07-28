import random
from abc import ABC, abstractmethod
from typing import List, Union


class BingoCardGenerator(ABC):
    def __init__(self, card_size=5, include_free_space=False):
        self.card_size = card_size
        self.include_free_space = include_free_space

    @abstractmethod
    def generate_card(self) -> List[List[Union[int, str]]]:
        pass

    @abstractmethod
    def generate_many_cards(
        self, num_cards: int, unique: bool = True
    ) -> List[List[List[Union[int, str]]]]:
        if unique:
            unique_cards = set()

            while len(unique_cards) < num_cards:
                card = self.generate_card()
                unique_cards.add(tuple(map(tuple, card)))

            return [list(map(list, card)) for card in unique_cards]

        cards = []
        for _ in range(num_cards):
            cards.append(self.generate_card())
        return cards

    def _create_free_space(self, card: List[List[Union[int, str]]]) -> bool:
        created = False
        card_size = len(card)
        if card_size % 2 != 0:
            middle_row = middle_col = card_size // 2
            card[middle_row][middle_col] = "FREE"
            created = True
        return created


class ClassicCardGenerator(BingoCardGenerator):
    FIRST_NUM = 1

    def __init__(
        self, last_num: int = 75, card_size: int = 5, include_free_space: bool = False
    ) -> None:
        super().__init__(card_size, include_free_space)
        self.last_num = last_num

    def generate_card(self) -> List[List[Union[int, str]]]:
        """
        Generates a classic bingo card.

        The classic bingo game starts from number 1, and each column on the card contains a {card_size}
        amount of numbers ranging from ax + 1 to (a + 1) * x + 1, where x is the size of the range and a is
        the column index.

        Returns:
            List[List[Union[int, str]]]: A 2D list representing the generated bingo card with numbers
            or strings for the free space.
        """

        if self.last_num < (self.card_size**2):
            raise ValueError("not enough numbers to fill the card")

        if self.last_num % self.card_size != 0:
            raise ValueError(
                f"{self.last_num} cannot be even divied into equal size of {self.card_size} ranges"
            )

        num_per_col = int(self.last_num / self.card_size)
        num_rows = num_cols = self.card_size
        card = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
        cols_nums = [set() for _ in range(num_rows)]

        for col_idx in range(num_cols):
            col_nums = random.sample(
                range(
                    col_idx * num_per_col + self.FIRST_NUM,
                    col_idx * num_per_col + num_per_col + self.FIRST_NUM,
                ),
                self.card_size,
            )

            for row_idx in range(num_rows):
                card[row_idx][col_idx] = col_nums[row_idx]
                cols_nums[col_idx].add(col_nums[row_idx])

        if self.include_free_space:
            super()._create_free_space(card)

        return card


class ThemeCardGeneator(BingoCardGenerator):
    def __init__(
        self,
        items: List[Union[int, str]],
        card_size: int = 5,
        include_free_space: bool = False,
    ) -> None:
        super().__init__(card_size, include_free_space)
        self.items = items

    def generate_card(self) -> List[List[Union[int, str]]]:
        if len(self.items) < self.card_size * self.card_size:
            raise ValueError("not enough items to fill a card")

        items_to_use = random.sample(self.items, self.card_size * self.card_size)
        card = []
        row_items = []

        while items_to_use:
            item_to_use = items_to_use.pop()
            row_items.append(item_to_use)

            if len(row_items) == self.card_size:
                card.append(row_items)
                row_items = []

        if self.include_free_space:
            super()._create_free_space(card)

        return card
