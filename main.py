import pickle

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []

class Player:
    def __init__(self):
        self.inventory = []

def save_game(player, current_room):
    with open("saved_game.bin", "wb") as f:
        pickle.dump((player, current_room), f)

def load_game():
    try:
        with open("saved_game.bin", "rb") as f:
            player, current_room = pickle.load(f)
            return player, current_room
    except FileNotFoundError:
        print("No saved game found.")
        return None, None

def get_input(choices):
    choice = ""
    while choice not in choices:
        choice = input("Enter your choice: ")
    return choice

def print_room(current_room):
    print("\n" + current_room.name)
    print(current_room.description)
    if current_room.items:
        print("Items in the room:")
        for item in current_room.items:
            print("- " + item.name)

def print_inventory(player):
    print("Inventory:")
    if player.inventory:
        for item in player.inventory:
            print("- " + item.name)
    else:
        print("You don't have any items in your inventory.")

def get_item(item_name, item_list):
    for item in item_list:
        if item.name == item_name:
            return item
    return None

def main():
    player = Player()
    current_room = Room("Starting Room", "You are in a dimly lit room. There is a door to the north.")
    save_game(player, current_room)

    while True:
        print_room(current_room)
        print_inventory(player)

        # Prompt the user for their choice
        choices = ["n", "s", "e", "w", "u", "d", "i", "q"]
        choice = get_input(choices)

        # Handle the user's choice
        if choice == "n":
            current_room = SecondRoom()
            save_game(player, current_room)
        elif choice == "s":
            current_room = Room("Starting Room", "You are in a dimly lit room. There is a door to the north.")
            save_game(player, current_room)
        elif choice == "e":
            if isinstance(current_room, SecondRoom):
                current_room = current_room.use_key(player)
                save_game(player, current_room)
            elif isinstance(current_room, FourthRoom):
                current_room = current_room.go_up(player)
                save_game(player, current_room)
            else:
                print("You cannot go east.")
        elif choice == "w":
            if isinstance(current_room, ThirdRoom):
                print("You have already been in this room.")
            else:
                current_room = ThirdRoom()
                save_game(player, current_room)
        elif choice == "u":
            if isinstance(current_room, FourthRoom):
                current_room = current_room.go_up(player)
                save_game(player, current_room)
            else:
                print("There is no way to go up here.")
        elif choice == "d":
            if isinstance(current_room, FifthRoom):
                current_room = current_room.go_down()
                save_game(player, current_room)
            else:
                print("There is no way to go down here.")
        elif choice == "use flashlight":
            if isinstance(current_room, ThirdRoom):
                current_room = current_room.use_flashlight(player)
                save_game(player, current_room)
            else:
                print("There's nothing to see here.")
        elif choice == "i":
            print_inventory(player)
            item_choice = input("Enter the name of the item you want to use (or type 'cancel' to cancel): ")
            if item_choice.lower() == "cancel":
                continue
            item = get_item(item_choice, player.inventory)
            if item:
                player.inventory.remove(item)
                print("You used the " + item.name + ".")
            else:
                print("You don't have an item named " + item_choice + ".")
        elif choice == "q":
            break

#All rooms are added here.---------------------------------------------------------------------------------------------------------------

class SecondRoom:
    def __init__(self):
        self.name = "Second Room"
        self.description = "You are in a spacious room with a high ceiling. There are two doors, one to the east and one to the south."
        self.items = [Item("key", "A small rusty key")]

    def use_key(self, player):
        key = get_item("key", player.inventory)
        if key:
            print("You used the key to unlock the door.")
            player.inventory.remove(key)
            return ThirdRoom()
        else:
            print("You don't have the key.")
            return self

class ThirdRoom:
    def __init__(self):
        self.name = "Third Room"
        self.description = "You are in a dark room with a faint light shining in from a small window. There is a door to the west."
        self.items = [Item("flashlight", "A small flashlight")]

    def use_flashlight(self, player):
        flashlight = get_item("flashlight", player.inventory)
        if flashlight:
            print("You turn on the flashlight and illuminate the room.")
            self.description = "You are in a dark room with a faint light shining in from a small window. There is a door to the west. You can see a safe in the corner of the room."
            return self
        else:
            print("You can't see anything in the dark.")
            return self

class FourthRoom:
    def __init__(self):
        self.name = "Fourth Room"
        self.description = "You are in a brightly lit room with a large window overlooking the city. There is a door to the east and a stairway going up."
        self.items = [Item("book", "A leather-bound book")]

    def go_up(self, player):
        print("You climb the stairs to the next floor.")
        return FifthRoom()

class FifthRoom:
    def __init__(self):
        self.name = "Fifth Room"
        self.description = "You are in a dusty attic filled with cobwebs. There is a door to the south and a ladder going down."
        self.items = [Item("key", "A shiny brass key")]

    def go_down(self):
        print("You climb down the ladder to the floor below.")
        return FourthRoom()


#End of rooms.-------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    player, current_room = load_game()
    if player is None or current_room is None:
        main()
    else:
        print("Saved game found.")
        while True:
            new_or_continue = input("Do you want to start a new game or continue your save?")
			if new_or_continue.lower() == "n" or "new":
                main()
                break
            elif new_or_continue.lower() == "c" or "continue":
                break
            else:
                print("Invalid input. Please try again.")

