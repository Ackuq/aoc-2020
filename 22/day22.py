import re
from typing import List, Tuple
from copy import deepcopy


file_name = "input"
input = open("./{}.txt".format(file_name)).read()


class Player:
    id: int
    deck: List[int]

    def __init__(self, id: int, deck: List[int]) -> None:
        self.id = id
        self.deck = deck

    def draw_card(self) -> int:
        return self.deck.pop(0)

    def insert_card(self, card: int):
        self.deck.append(card)

    def has_lost(self) -> bool:
        return len(self.deck) == 0


def map_input(player_string: str):
    rows = player_string.split("\n")
    id = int(re.match(r"Player\s(\d):", rows[0]).group(1))
    cards = list(map(int, rows[1:]))
    return Player(id, cards)


players = list(map(map_input, input.split("\n\n")))


def part1(player1: Player, player2: Player):
    while not player1.has_lost() and not player2.has_lost():
        card1 = player1.draw_card()
        card2 = player2.draw_card()

        highest = max(card1, card2)
        lowest = min(card1, card2)

        if highest == card1:
            player1.insert_card(highest)
            player1.insert_card(lowest)
        else:
            player2.insert_card(highest)
            player2.insert_card(lowest)

    winner = player1 if player2.has_lost() else player2

    return sum(card * (i + 1) for i, card in enumerate(reversed(winner.deck)))


def part2(player1: Player, player2: Player):
    def play(game: int, round: int) -> Player:
        # print("== Game {} ==".format(game))
        recursion_found = False
        previous: List[Tuple[List[int], List[int]]] = []

        while not player1.has_lost() and not player2.has_lost():
            # print("-- Round {} (Game {}) --".format(round, game))
            # print(
            #     "Player {} deck: {}".format(
            #         player1.id, ", ".join(map(str, player1.deck))
            #     )
            # )
            # print(
            #     "Player {} deck: {}".format(
            #         player2.id, ", ".join(map(str, player2.deck))
            #     )
            # )

            if any(p[0] == player1.deck or p[1] == player2.deck for p in previous):
                recursion_found = True
                break

            previous.append((player1.deck.copy(), player2.deck.copy()))

            card1 = player1.draw_card()
            card2 = player2.draw_card()

            # print("Player {} plays: {}".format(player1.id, card1))
            # print("Player {} plays: {}".format(player2.id, card2))

            winner = None
            played_cards: Tuple[int, int]

            if card1 <= len(player1.deck) and card2 <= len(player2.deck):
                # print("Playing sub-game to determine winner...\n")
                temp1 = player1.deck.copy()
                temp2 = player2.deck.copy()
                player1.deck = temp1[:card1]
                player2.deck = temp2[:card2]
                winner = play(game + 1, 1)
                # print("...anyway, back to game {}.".format(game))
                player1.deck = temp1
                player2.deck = temp2
            else:
                highest = max(card1, card2)

                if highest == card1:
                    winner = player1
                else:
                    winner = player2
            # print("Player {} wins round {} of game {}\n".format(winner.id, round, game))
            if winner.id == player1.id:
                played_cards = (card1, card2)
            else:
                played_cards = (card2, card1)

            winner.insert_card(played_cards[0])
            winner.insert_card(played_cards[1])
            round += 1

        winner = None
        if recursion_found:
            winner = player1
        else:
            winner = player1 if player2.has_lost() else player2

        return winner

    winner = play(1, 1)

    return sum(card * (i + 1) for i, card in enumerate(reversed(winner.deck)))


if __name__ == "__main__":
    print("Part 1:", part1(deepcopy(players[0]), deepcopy(players[1])))
    print("Part 2:", part2(deepcopy(players[0]), deepcopy(players[1])))
