import json
from termcolor import colored

SAVE_FILE_NAME_AUTO = "auto_save.json"
SAVE_FILE_NAME_MANUAL = "manual_save.json"


class Decks:
    def __init__(
        self,
        infection: list[list[str]],
        discard: list[str],
        city_to_color: dict[str, str],
    ) -> None:
        self.infection_deck: list[list[str]] = infection
        self.discard_pile: list[str] = discard
        self.city_to_color: dict[str, str] = city_to_color

    @staticmethod
    def load(file_name: str) -> "Decks":
        with open(file_name, "rb") as file:
            obj = json.load(file)

        return Decks(
            obj.get("infection", []),
            obj.get("discard", []),
            obj.get("city_to_color", {}),
        )

    def save(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            json.dump(
                {
                    "infection": self.infection_deck,
                    "discard": self.discard_pile,
                    "city_to_color": self.city_to_color,
                },
                file,
                indent=4,
            )

    def print(self) -> None:
        print("infection decks (topmost first):\n[")
        for infections in self.infection_deck:
            reprs = []
            for city in infections:
                reprs.append(self._format_city(city))
            print(f"\t[{', '.join(reprs)}]")
        print("]\n")
        discards = [self._format_city(city) for city in self.discard_pile]
        print(f"discard: [{', '.join(discards)}]")

    def _format_city(self, city: str) -> str:
        if city in self.city_to_color:
            return colored(city, self.city_to_color[city])
        return city

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

    def mark_city(self, city: str, color: str) -> None:
        self.city_to_color[city] = color

    def unmark_city(self, city: str) -> None:
        del self.city_to_color[city]


def load_deck(file_name):
    with open(file_name, "r") as deck_file:
        return [line.strip().lower() for line in deck_file.readlines()]


def mainloop(decks: Decks) -> None:
    user_option = ""
    while user_option != "q":
        user_option = input(
            """\nquit, save, load, print, draw_card, shuffle, remove_discard, mark_red, mark_yellow, unmark:\n"""
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
        elif user_option.startswith("mark_red") or user_option.startswith("mr"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.mark_city(c, "red")
                    decks.save(SAVE_FILE_NAME_AUTO)
                decks.print()
            else:
                print("usage: mark_red|mr card_name")
        elif user_option.startswith("mark_yellow") or user_option.startswith("my"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.mark_city(c, "yellow")
                    decks.save(SAVE_FILE_NAME_AUTO)
                decks.print()
            else:
                print("usage: mark_yellow|my card_name")
        elif user_option.startswith("unmark") or user_option.startswith("um"):
            l = user_option.split(" ")
            if len(l) >= 2:
                for c in l[1:]:
                    c = c.replace("_", " ").strip().lower()
                    decks.unmark_city(c)
                    decks.save(SAVE_FILE_NAME_AUTO)
                decks.print()
            else:
                print("usage: unmark|um card_name")


def main() -> None:
    start_deck = sorted(load_deck("infection_deck.txt"))
    decks = Decks([start_deck], discard=[], city_to_color={})
    decks.print()
    mainloop(decks)


if __name__ == "__main__":
    main()
