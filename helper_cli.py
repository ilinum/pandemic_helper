import pickle

infection_deck: [[str]] = []
discard_pile: [str] = []
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

def print_decks():
    global infection_deck, discard_pile
    print('[')
    for x in infection_deck:
        print('\t', x)
    print(']')
    print(discard_pile)


def mainloop():
    global infection_deck, discard_pile, unique_cards
    user_option = ""
    while(user_option != 'q'):
        user_option = input("""\nquit, save, load, print, add_card, draw_card, shuffle, remove_card:\n""")
        if (user_option == 'quit' or user_option == 'q'):
            save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
            break
        elif (user_option == 'save' or user_option == 's'):
            save_state((infection_deck, discard_pile, unique_cards), "manual_save.pkl")
        elif (user_option.startswith('load') or user_option.startswith('l ')):
            l = user_option.split(" ")
            if (len(l) == 1):
                infection_deck, discard_pile, unique_cards = load_state("manual_save.pkl")
                print_decks()
            elif(len(l) == 2):
                if (l[1] == 'manual'):
                    infection_deck, discard_pile, unique_cards = load_state("manual_save.pkl")
                    print_decks()
                elif (l[1] == 'auto'):
                    infection_deck, discard_pile, unique_cards = load_state("auto_save.pkl")
                    print_decks()
                else:
                    print("usage: load|l [manual|auto]")
            else:
                print("usage: load|l manual|auto")
        elif (user_option == 'print' or user_option == 'p'):
            save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
            print_decks()
        elif (user_option.startswith('add_card') or user_option.startswith('ac')):
            l = user_option.split(" ")
            if (len(l) == 3):
                c = l[2].replace('_', ' ')
                c = c.strip()
                c = c.lower()
                if (l[1].isdecimal):
                    i = int(l[1])
                    if (len(infection_deck) > i):
                        unique_cards.add(c)
                        infection_deck[i].append(c)
                        infection_deck[i].sort()
                        save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
                        print_decks()
                    else:
                        print("that sub-deck doesn't exist")
                else:
                    print("NaN index")
            else:
                print("usage: add_card|ac \d+ card_name")
        elif (user_option.startswith('draw_card') or user_option.startswith('dc')):
            l = user_option.split(" ")
            if (len(l) >= 2):
                for c in l[1:]:
                    c = c.replace('_', ' ')
                    c = c.strip()
                    c = c.lower()
                    if (c in unique_cards):
                        if (c in infection_deck[0]):
                            infection_deck[0].remove(c)
                            if (not infection_deck[0]):
                                infection_deck.pop(0)
                            discard_pile.append(c)
                            discard_pile.sort()
                            save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
                            print_decks()
                        else:
                            print("card not in infection deck", c)
                    else:
                        print("card doesn't exist", c)
            else:
                print("usage: draw_card|dc card_name")
        elif(user_option.startswith('shuffle') or user_option.startswith('sh')):
            if (len(discard_pile) > 0):
                infection_deck.insert(0, discard_pile)
                discard_pile = []
                save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
                print_decks()
        elif (user_option.startswith('remove_card') or user_option.startswith('rc')):
            l = user_option.split(" ")
            if (len(l) == 3):
                c = l[2].replace('_', ' ')
                c = c.strip()
                c = c.lower()
                if (l[1].isdecimal):
                    i = int(l[1])
                    if (len(infection_deck) > i):
                        infection_deck[i].remove(c)
                        save_state((infection_deck, discard_pile, unique_cards), "auto_save.pkl")
                        print_decks()
                    else:
                        print("that sub-deck doesn't exist")
                else:
                    print("NaN index")
            else:
                print("usage: remove_card|rc \d+ card_name")

def main():
    start_deck = load_deck("infection_deck.txt")
    infection_deck.append(start_deck)
    unique_cards.update(infection_deck[-1])
    
    infection_deck[0].sort()
    print_decks()
    mainloop()


if __name__ == "__main__":
    main()