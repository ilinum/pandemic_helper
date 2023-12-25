import json

SAVE_FILE_NAME_AUTO = "auto_save.json"
SAVE_FILE_NAME_MANUAL = "manual_save.json"

class Decks:
    def __init__(self, infection: list[list[str]], discard: list[str]) -> None:
        self.infection_deck: list[list[str]] = infection
        self.discard_pile: list[str] = discard

    @staticmethod
    def load(file_name: str) -> "Decks":
        with open(file_name, "rb") as file:
            obj = json.load(file)
            infection = obj["infection"]
            discard = obj["discard"]
        return Decks(infection, discard)

    def save(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            json.dump(
                {"infection": self.infection_deck, "discard": self.discard_pile},
                file,
                indent=4,
            )

    def print(self) -> None:
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

    def remove_discard(self, card: str) -> None:
        if card in self.discard_pile:
            self.discard_pile.remove(card)


def load_deck(file_name):
    with open(file_name, "r") as deck_file:
        return [line.strip().lower() for line in deck_file.readlines()]


def mainloop(decks: Decks) -> None:
    user_option = ""
    while user_option != "q":
        user_option = input(
            """\nquit, save, load, print, draw_card, shuffle, remove_discard:\n"""
        )
        if user_option == "quit" or user_option == "q":
            decks.save(SAVE_FILE_NAME_AUTO)
            break
        elif user_option == "save" or user_option == "s":
            decks.save(SAVE_FILE_NAME_MANUAL)
        elif user_option.startswith("load") or user_option.startswith("l "):
            l = user_option.split(" ")
            if len(l) == 1:
                decks = Decks.load(SAVE_FILE_NAME_MANUAL)
                decks.print()
            elif len(l) == 2:
                if l[1] == "manual":
                    decks = Decks.load(SAVE_FILE_NAME_MANUAL)
                    decks.print()
                elif l[1] == "auto":
                    decks = Decks.load(SAVE_FILE_NAME_AUTO)
                    decks.print()
                else:
                    print("usage: load|l [manual|auto]")
            else:
                print("usage: load|l manual|auto")
        elif user_option == "print" or user_option == "p":
            decks.save(SAVE_FILE_NAME_AUTO)
            decks.print()
        elif user_option.startswith("draw_card") or user_option.startswith("dc"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.draw(c)
                    decks.save(SAVE_FILE_NAME_AUTO)
                    decks.print()
            else:
                print("usage: draw_card|dc card_name")
        elif user_option.startswith("shuffle") or user_option.startswith("sh"):
            if len(decks.discard_pile) > 0:
                decks.reshuffle_discard()
                decks.save(SAVE_FILE_NAME_AUTO)
            decks.print()
        elif user_option.startswith("remove_discard") or user_option.startswith("rd"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.remove_discard(c)
                    decks.save(SAVE_FILE_NAME_AUTO)
                    decks.print()
            else:
                print("usage: remove_discard|rd card_name")


def main() -> None:
    start_deck = sorted(load_deck("infection_deck.txt"))
    decks = Decks([start_deck], discard=[])
    decks.print()
    mainloop(decks)


if __name__ == "__main__":
    main()
