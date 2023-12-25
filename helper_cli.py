import pickle


class Decks:
    def __init__(self, infection, discard):
        self.infection_deck: list[list[str]] = infection
        self.discard_pile: list[str] = discard

    @staticmethod
    def load(file_name):
        with open(file_name, "rb") as pickle_file:
            (infection, discard) = pickle.load(pickle_file)
        return Decks(infection, discard)

    def save(self, file_name):
        with open(file_name, "wb") as pickle_file:
            pickle.dump((self.infection_deck, self.discard_pile), pickle_file)

    def print(self):
        print("[")
        for x in self.infection_deck:
            print("\t", x)
        print("]")
        print(self.discard_pile)

    def draw(self, card: str) -> None:
        if card in self.infection_deck[0]:
            self.infection_deck[0].remove(card)
            if not self.infection_deck[0]:
                self.infection_deck.pop(0)
        self.discard_pile.append(card)
        self.discard_pile.sort()

    def reshuffle_discard(self) -> None:
        if len(self.discard_pile) > 0:
            self.infection_deck.insert(0, list(self.discard_pile))
            self.discard_pile = []


def load_deck(file_name):
    with open(file_name, "r") as deck_file:
        return [line.strip().lower() for line in deck_file.readlines()]


def mainloop(decks: Decks) -> None:
    user_option = ""
    while user_option != "q":
        user_option = input(
            """\nquit, save, load, print, draw_card, shuffle, remove_card:\n"""
        )
        if user_option == "quit" or user_option == "q":
            decks.save("auto_save.pkl")
            break
        elif user_option == "save" or user_option == "s":
            decks.save("manual_save.pkl")
        elif user_option.startswith("load") or user_option.startswith("l "):
            l = user_option.split(" ")
            if len(l) == 1:
                decks = Decks.load("manual_save.pkl")
                decks.print()
            elif len(l) == 2:
                if l[1] == "manual":
                    decks = Decks.load("manual_save.pkl")
                    decks.print()
                elif l[1] == "auto":
                    decks = Decks.load("auto_save.pkl")
                    decks.print()
                else:
                    print("usage: load|l [manual|auto]")
            else:
                print("usage: load|l manual|auto")
        elif user_option == "print" or user_option == "p":
            decks.save("auto_save.pkl")
            decks.print()
        elif user_option.startswith("draw_card") or user_option.startswith("dc"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.draw(c)
                    decks.save("auto_save.pkl")
                    decks.print()
            else:
                print("usage: draw_card|dc card_name")
        elif user_option.startswith("shuffle") or user_option.startswith("sh"):
            if len(decks.discard_pile) > 0:
                decks.reshuffle_discard()
                decks.save("auto_save.pkl")
            decks.print()
        elif user_option.startswith("remove_card") or user_option.startswith("rc"):
            l = user_option.split(" ")
            if len(l) == 3:
                c = l[2].replace("_", " ").strip().lower()
                if l[1].isdecimal:
                    i = int(l[1])
                    if len(decks.infection_deck) > i:
                        decks.infection_deck[i].remove(c)
                        decks.save("auto_save.pkl")
                        decks.print()
                    else:
                        print("that sub-deck doesn't exist")
                else:
                    print("NaN index")
            else:
                print("usage: remove_card|rc \d+ card_name")


def main() -> None:
    start_deck = sorted(load_deck("infection_deck.txt"))
    decks = Decks([start_deck], discard=[])
    decks.print()
    mainloop(decks)


if __name__ == "__main__":
    main()
