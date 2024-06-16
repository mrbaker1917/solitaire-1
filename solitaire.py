from random import shuffle
import copy
from termcolor import colored


#######################################################################################################
# CARD SETUP


def assign_value(seed):
    if seed % 13 == 0:
        value = 1
    elif seed % 13 == 1:
        value = 2
    elif seed % 13 == 2:
        value = 3
    elif seed % 13 == 3:
        value = 4
    elif seed % 13 == 4:
        value = 5
    elif seed % 13 == 5:
        value = 6
    elif seed % 13 == 6:
        value = 7
    elif seed % 13 == 7:
        value = 8
    elif seed % 13 == 8:
        value = 9
    elif seed % 13 == 9:
        value = 10
    elif seed % 13 == 10:
        value = 11
    elif seed % 13 == 11:
        value = 12
    elif seed % 13 == 12:
        value = 13
    return value


def assign_rank(seed):
    if seed % 13 == 0:
        card = "Ace"
    elif seed % 13 == 1:
        card = "Two"
    elif seed % 13 == 2:
        card = "Three"
    elif seed % 13 == 3:
        card = "Four"
    elif seed % 13 == 4:
        card = "Five"
    elif seed % 13 == 5:
        card = "Six"
    elif seed % 13 == 6:
        card = "Seven"
    elif seed % 13 == 7:
        card = "Eight"
    elif seed % 13 == 8:
        card = "Nine"
    elif seed % 13 == 9:
        card = "Ten"
    elif seed % 13 == 10:
        card = "Jack"
    elif seed % 13 == 11:
        card = "Queen"
    elif seed % 13 == 12:
        card = "King"
    return card


def assign_suit(seed):
    if seed % 4 == 0:
        suit = "Clubs"
    elif seed % 4 == 1:
        suit = "Diamonds"
    elif seed % 4 == 2:
        suit = "Spades"
    elif seed % 4 == 3:
        suit = "Hearts"
    return suit


def assign_color(suit):
    if suit == "Clubs" or suit == "Spades":
        return "Black"
    else:
        return "Red"


def deal_cards(piles):
    for i in range(7):
        for j in range(i, 7):
            piles[j].face_down.append(Card())
        piles[i].face_up.append(piles[i].face_down[-1])
        piles[i].face_down.pop(-1)


########################################################################################################
# MOVES AND MAIN LOGIC


def flip_card(pile):
    pile.face_up.append(pile.face_down[-1])
    pile.face_down.pop()


def check_king(pile):
    if pile.face_up[0].rank != "King":
        raise PileError("Invalid move! (must be king)")


def move_pile(piles):
    while True:
        print("Which pile would you like to move from (number 1-7)?")
        print("Input 'r' to return.")
        in1 = input(":> ")
        if in1 == "r":
            break
        try:
            pile1 = copy.deepcopy(piles[int(in1) - 1])
        except ValueError:
            print("Invalid input. (must be digit)")
        except IndexError:
            print("Invalid input. (must be 1-7)")
        else:
            print(f"Selected pile {in1}.")
            break
    while True:
        print("Which pile would you like to move to? (number 1-7)")
        print("Input 'r' to return.")
        in2 = input(":> ")
        if in2 == "r":
            break
        try:
            pile2 = copy.deepcopy(piles[int(in2) - 1])
            if in1 == in2:
                raise PileError("Invalid input. (cannot move to the same pile)")
        except PileError as e:
            print(e)
        except ValueError:
            print("Invalid input. (must be digit)")
        except IndexError:
            print("Invalid input. (must be 1-7)")
        else:
            print(f"Selected pile {in2}.")
            break
    while True:
        pile1 = copy.deepcopy(piles[int(in1) - 1])
        pile2 = copy.deepcopy(piles[int(in2) - 1])
        print(
            "Input the card (or bottom card) you'd like to move from the first pile. (card value ex. 'Ace', 'Queen')"
        )
        print("Input 'r' to return.")
        in3 = input(":> ")
        if in3 == "r":
            break
        face_up_ranks = [card.rank for card in pile1.face_up]
        try:
            if len(pile2.face_up) == 0 and len(pile2.face_down) == 0 and in3 != "King":
                raise PileError("Invalid move. (must be a king)")
            pile2.face_up.extend(pile1.face_up[face_up_ranks.index(in3) :])
            pile1.face_up = pile1.face_up[: face_up_ranks.index(in3)]
            pile1.check_pile()
            pile2.check_pile()
        except PileError as e:
            print(e)
        except ValueError:
            print(f"Invalid input. (no card with value of {in3})")
        else:
            piles[int(in1) - 1] = pile1
            piles[int(in2) - 1] = pile2
            print(
                f"Moved the {in3} and all cards above it in pile {in1} to pile {in2}."
            )
            break


def move_fnd(fnds, piles):
    while True:
        print("Input the pile you'd like to move the top card from. (number 1-7)")
        print("Input 'r' to return.")
        in1 = input(":> ")
        if in1 == "r":
            break
        try:
            pile = copy.deepcopy(piles[int(in1) - 1])
        except ValueError:
            print("Invalid input. (must be digit)")
        except IndexError:
            print("Invalid input. (must be a number 1-7)")
        else:
            break
    while True:
        pile = copy.deepcopy(piles[int(in1) - 1])
        print("Input the foundation pile you'd like to move your card to. (number 1-4)")
        print("Input 'r' to return.")
        in2 = input(":> ")
        if in2 == "r":
            break
        try:
            fnd = copy.deepcopy(fnds[int(in2) - 1])
            fnd.append(pile.face_up[-1])
            pile.face_up.pop(-1)
            pile.check_pile()
            check_fnd(fnd)
        except ValueError:
            print("Invalid input. (must be digit)")
        except IndexError:
            print("Invalid input. (must be a number 1-4)")
        except FndError as e:
            print(e)
        else:
            fnds[int(in2) - 1] = fnd
            piles[int(in1) - 1] = pile
            break


def flip_deck(deck):
    if len(deck[1]) == 0 and len(deck[0]) != 0:
        deck[1].extend(deck[0][::-1])
        deck[0] = []
    elif len(deck[1]) == 0 and len(deck[0]) == 0:
        print("Invalid move. (no cards left in deck!)")
    else:
        deck[0].append(deck[1][-1])
        deck[1].pop(-1)


def move_deck(deck, piles, fnds):  # make sure there is a face-up card in the deck
    while True:
        print("Input whether to move to a foundation or a pile. ('f' or 'p')")
        print("Input 'r' to return.")
        in1 = input(":> ")
        if in1 == "r":
            break
        if in1 != "f" and in1 != "p":
            print("Invalid input. (must be 'f' or 'p')")
        else:
            break
    if in1 == "f":
        while True:
            print("Input the foundation pile you want to move to. (number 1-4)")
            print("Input 'r' to return.")
            in2 = input(":> ")
            if in2 == "r":
                break
            try:
                fnd = copy.deepcopy(fnds[int(in2) - 1])
                fnd.append(deck[0][-1])
                deck[0].pop(-1)
                check_fnd(fnd)
            except ValueError:
                print("Invalid input. (must be digit)")
            except IndexError:
                print("Invalid input. (must be a number 1-4)")
            except FndError as e:
                print(e)
            else:
                fnds[int(in2) - 1] = fnd
                break

    else:
        while True:
            print("Input the pile you want to move to. (number 1-7)")
            print("Input 'r' to return.")
            in2 = input(":> ")
            if in2 == "r":
                break
            try:
                pile = copy.deepcopy(piles[int(in2) - 1])
                pile.face_up.append(deck[0][-1])
                deck[0].pop(-1)
                pile.check_pile()
            except ValueError:
                print("Invalid input. (must be a number)")
            except IndexError:
                print("Invalid input. (must be a number 1-7)")
            except PileError as e:
                print(e)
            else:
                piles[int(in2) - 1] = pile
                break


def move_rev(fnds, piles):
    while True:
        print("Input the foundation pile you want to move from. (number 1-4)")
        print("Input 'r' to return.")
        in1 = input(":> ")
        if in1 == "r":
            break
        try:
            fnd = copy.deepcopy(fnds[int(in1) - 1])
        except ValueError:
            print("Invalid input. (must be a number)")
        except IndexError:
            print("Invalid input. (must be a number 1-4)")
        else:
            break
    while True:
        print("Input the pile you want to move to. (number  1-7)")
        print("Input 'r' to return.")
        in2 = input(":> ")
        if in2 == "r":
            break
        try:
            pile = copy.deepcopy(piles[int(in2) - 1])
            pile.face_up.append(fnd[-1])
            fnd.pop(-1)
            pile.check_pile()
        except ValueError:
            print("Invalid input. (must be a number)")
        except IndexError:
            print("Invalid input. (must be a number 1-7)")
        except PileError as e:
            print(e)
        else:
            fnds[int(in1) - 1] = fnd
            piles[int(in2) - 1] = pile
            break


def check_fnd(fnd):
    if len(fnd) == 1:
        if fnd[0].rank != "Ace":
            raise FndError("Invalid move. (must be ace)")
    elif len(fnd) > 1:
        if fnd[-1].suit != fnd[-2].suit:
            raise FndError("Invalid move. (must be same suit)")
        elif fnd[-1].value - 1 != fnd[-2].value:
            raise FndError("Invalid move. (bad value sort)")


def print_game(piles, fnds, deck):
    print("\nPILES:")
    for pile in piles:
        print(str(piles.index(pile) + 1) + ")")
        pile.print_pile()
    print("\nFOUNDATION PILES:")
    for fnd in fnds:
        if len(fnd) != 0:
            print(fnd[-1])
        else:
            print("No cards.")
    print("\nDECK:")
    if deck[0] == [] and deck[1] == []:
        print("No cards in the deck.")
    else:
        if len(deck[0]) >= 3:
            print(deck[0][-1])
            print(deck[0][-2])
            print(deck[0][-3])
        elif len(deck[0]) == 2:
            print(deck[0][-1])
            print(deck[0][-2])
        elif len(deck[0]) == 1:
            print(deck[0][-1])
        else:
            print("No cards face up.")
        if len(deck[1]) > 1:
            print(f"{len(deck[1])} cards face-down.")
        elif len(deck[1]) == 1:
            print(f"1 card face down.")
        else:
            print("No cards face down.")


def check_win(fnds):
    wins = 0
    for fnd in fnds:
        if len(fnd) == 13:
            wins += 1
    if wins == 4:
        return True
    else:
        return False


class PileError(Exception):
    pass


class FndError(Exception):
    pass


class Card:
    def __init__(self):
        seed = seeds[0]
        seeds.pop(0)
        self.value = assign_value(seed)
        self.rank = assign_rank(seed)
        self.suit = assign_suit(seed)
        self.color = assign_color(self.suit)
        self.output = f"{self.rank} of {self.suit}"

    def __str__(self):
        return self.output


class Pile:
    def __init__(self):
        self.face_down = []
        self.face_up = []

    def print_pile(self):
        for card in self.face_up:
            if card.color == "Red":
                print(f'  {colored(card, "red")}')
            else:
                print(f'  {colored(card, "blue")}')
        print(f"  {len(self.face_down)} cards face-down.")

    def check_pile(self):
        if len(self.face_up) == 0:
            if len(self.face_down) != 0:
                flip_card(self)

        elif len(self.face_up) > 1:
            if self.face_up[-1].value + 1 != self.face_up[-2].value:
                raise PileError("Invalid move. (bad value sort)")
            elif self.face_up[-1].color == self.face_up[-2].color:
                raise PileError("Invalid move. (same color)")


#########################################################################################################
# MENU AND UI


print("\nWelcome to solitaire!")
while True:
    print("Start a game, print the rules or quit. ('s', 'r', 'q')")
    start = input(":> ")
    if start == "q":
        break

    elif start == "s":
        seeds = []
        for i in range(
            1, 53
        ):  # it is very important this stays at range(1,53) for seed generation reasons
            seeds.append(i)

        shuffle(seeds)

        piles = [Pile() for i in range(7)]

        deal_cards(piles)

        fnds = [[] for i in range(4)]

        deck = [[], [Card() for i in range(len(seeds))]]

        while True:
            print_game(piles, fnds, deck)

            print(
                """\nPICK A MOVE:
'p': move a card or stack of cards between piles
'l': flip a card in the deck over. (if no cards are face down, the deck will be turned face-down.)
'f': move a card from a pile to a foundation pile.
'd': move a card from the deck to any pile.
'r': move a card from a foundation pile to a pile.
'q': quit the game."""
            )
            pick_move = input(":> ")

            if pick_move == "q":
                break

            elif pick_move == "p":
                move_pile(piles)

            elif pick_move == "l":
                flip_deck(deck)

            elif pick_move == "f":
                move_fnd(fnds, piles)

            elif pick_move == "d":
                if len(deck[0]) != 0:
                    move_deck(deck, piles, fnds)
                else:
                    print("There are no face-up cards in the deck.")

            elif pick_move == "r":
                move_rev(fnds, piles)

            else:
                print("Invalid input. (must be one of the inputs listed above)")

            win = check_win(fnds)
            if win:
                print("You won!")
                break
            else:
                continue

    elif start == "r":
        print(
            """Rules of solitaire:
 - In solitaire, the goal is to sort each of the four foundation piles.
 - The foundation piles must be sorted from lowest to highest.
 - Aces are low and Kings are high, so the piles must start with Aces and end with Kings.
 - The foundation piles are organised by suit.
 - At the start of a round of Solitaire, you are dealt 7 piles of cards with increasing numbers of cards in each pile.
 - Each pile must have at least one face-up card.
 - Face-up cards can be moved to form piles with other cards.
 - These piles must be organised from highest to lowest, and must alternate color.
 - In order to start a new pile, there must be an empty space and the bottom card must be a King.
 - The remaining cards in the deck are set face down.
 - Drawn cards from this deck are added to a new deck, with only the top card (most recently drawn) being accessible.
 - After the entire deck has been drawn, the deck can be flipped over and sorted through again.
 - It's order must be kept.
 - Cards can be moved to and from the four foundation piles, between piles, and from the deck to .
              """
        )

    else:
        print("Invalid input.")
