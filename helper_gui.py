#pls no look, its ugly

import pickle
import tkinter

infection_deck = []
discard_pile = []
unique_cards: {str} = set()

def save_state(state, file_name):
    with open(file_name, 'wb') as pickle_file:
        pickle.dump(state, pickle_file)

def load_state(file_name):
    with open(file_name, 'rb') as pickle_file:
        res = pickle.load(pickle_file)
    return res


def load_deck(file_name):
    with open(file_name, 'r') as deck_file:
        lines = deck_file.readlines()
        lines = map(str.strip, lines)
        lines = map(str.lower, lines)
    return list(lines)
        
def autocomplete(options, value):
    pass

def autocomplete_matches(value: str):
    global unique_cards
    cv = value.strip().lower()
    if (not cv):
        return []

    matches = []
    for u in unique_cards:
        if (u.startswith(cv)):
            matches.append(u)
    
    matches.sort(key=lambda v: len(v))
    print(cv, matches)
    return matches



class AutocompleteText(tkinter.Text):
    valid_chars = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    exclude_codes = set([22])

    def __init__(self, *args, **kwargs):
        self.autocomplete_callback = kwargs.pop("autocomplete", None)
        self.text_done_callback = kwargs.pop("text_done", None)
        super().__init__(*args, **kwargs)
        self.bind("<Any-KeyRelease>", self._autocomplete)
        self.bind("<Tab>", self._handle_tab)
        self.bind("<Return>", self._handle_enter)

    def _handle_enter(self, event):
        val = self.get("1.0", "end")
        self.delete("1.0", "end")

        self.tag_remove("sel", "1.0", "end")
        self.tag_remove("autocomplete", "1.0", "end")
        self.mark_unset("insert")

        self.text_done_callback(val)
        self.event_generate("<<textbox_done>>", data=val)
        return "break"


    def _handle_tab(self, event):
        tag_ranges= self.tag_ranges("autocomplete")
        if tag_ranges:
            self.mark_set("insert", tag_ranges[1])
            self.tag_remove("sel", "1.0", "end")
            self.tag_remove("autocomplete", "1.0", "end")

        return "break"

    def _autocomplete(self, event: tkinter.Event):
        if (event.keysym and self.autocomplete_callback and not event.keycode in self.exclude_codes):
            
            word = self.get("1.0", "end")
            matches = self.autocomplete_callback(word)

            if (matches):
                remainder = matches[0][len(word)-1:]

                insert = self.index("insert")
                self.insert(insert, remainder, ("sel", "autocomplete"))
                self.mark_set("insert", insert)

def add_card_to_infection_deck(list, value):
    infection_deck[0].append(value)
    infection_deck[0].sort()
    list.delete(0, "end")
    list.insert("end", *(infection_deck[0]))

def add_card_to_discard_pile(list, value):
    if (value in infection_deck[0]):
        infection_deck[0].remove(value)
        discard_pile.append(value)
        discard_pile.sort()
        list.delete(0, "end")
        list.insert("end", *(discard_pile))

class DeckListbox(tkinter.Listbox):
    def __init__(self, *args, **kwargs):
        self.add_card = kwargs.pop("add_card", None)
        super().__init__(*args, **kwargs)

    def handle_text(self, value):
        value = value.strip()
        if (self.add_card):
            self.add_card(self, value)

def handle_event(event: tkinter.Event):
    print(event)
    for x, y in event.__dict__.items():
        print(x, y)

def main():
    start_deck = load_deck("infection_deck.txt")
    infection_deck.append(start_deck)
    unique_cards.update(infection_deck[-1])

    root = tkinter.Tk()

    left_frame = tkinter.Frame(root)
    decklist_label = tkinter.Label(left_frame, text="Cards in infection deck")
    decklist = DeckListbox(left_frame, add_card=add_card_to_infection_deck)
    add_card_label = tkinter.Label(left_frame, text="Add infection card")
    add_card = AutocompleteText(left_frame, height=1, autocomplete=autocomplete_matches, text_done=decklist.handle_text)

    right_frame = tkinter.Frame(root)
    draw_card_label =  tkinter.Label(right_frame, text="Draw infection card")
    discardlist = DeckListbox(right_frame, add_card=add_card_to_discard_pile)
    discardlist_label =  tkinter.Label(right_frame, text="Cards in discard pile")
    draw_card = AutocompleteText(right_frame, height=1, autocomplete=autocomplete_matches, text_done=discardlist.handle_text)

    add_card_label.pack()
    add_card.pack()
    decklist_label.pack()
    decklist.pack(fill='both', expand=True)

    draw_card_label.pack()
    draw_card.pack()
    discardlist_label.pack()
    discardlist.pack(fill='both', expand=True)

    left_frame.pack(side=tkinter.LEFT, fill='both', expand=True)
    right_frame.pack(side=tkinter.RIGHT, fill='both', expand=True)

    # root.event_add("<<textbox_done_event>>", "<<textbox_done>>")
    root.bind("<<textbox_done>>", handle_event)
    
    infection_deck[0].sort()
    decklist.insert("end", *(infection_deck[0]))
    root.mainloop()


if __name__ == "__main__":
    main()