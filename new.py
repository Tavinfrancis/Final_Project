import pickle

storyline = {
	"start": "You awaken in a mysterious dungeon with no memory of how you got there. To escape, you must find a way to unlock the large door.",
	"objectives": [
		"Find the hidden treasure.",
		"Discover the secret behind the ancient statues.",
		"Unlock the large door.",
		"Escape the dungeon."
	],
}

def print_storyline(storyline):
	print(storyline["start"])
	print("\nObjectives:")
	for objective in storyline["objectives"]:
		print(f"- {objective}")

def solve_riddle(player):
	riddle = "What has a heart that doesn’t beat? (Answer in one word)"
	answer = input("The Guardian asks: " + riddle + " ").lower()
	if answer == "artichoke":
		print("Correct! The Guardian hands you a scroll.")
		player.inventory.append("scroll")
	else:
		print("Incorrect! The Guardian remains silent.")

def check_win_condition(player):
	if ("key" in player.inventory and
		"treasure" in player.inventory and
		"statue" in player.inventory and
		player.room.description == "You are in a room with a large, ominous-looking door. It appears to be locked. There is a door to the west."):
		print("Congratulations! You have unlocked the door and escaped the dungeon!")
		print("Thanks for playing!")
		exit(0)


class Room:
	def __init__(self, description, items=None):
		self.description = description
		self.items = items if items is not None else []
		self.connections = {}

	def add_item(self, item):
		self.items.append(item)

	def remove_item(self, item):
		self.items.remove(item)

	def connect(self, direction, room):
		self.connections[direction] = room

class Player:
	def __init__(self, room):
		self.inventory = []
		self.room = room
		self.solved_riddles = []

	def pick_up(self, item):
		self.inventory.append(item)
		self.room.remove_item(item)

	def use_item(self, item):
		self.inventory.remove(item)

	def move(self, direction):
		if direction in self.room.connections:
			self.room = self.room.connections[direction]
			return True
		return False

def describe_room(room):
	print(room.description)
	if room.items:
		print("Items in the room:", ", ".join(room.items))

def save_game(player, filename="game_save.pickle"):
	with open(filename, "wb") as f:
		pickle.dump(player, f)

def load_game(player, filename="game_save.pickle"):
	try:
		with open(filename, "rb") as f:
			return pickle.load(f)
	except (FileNotFoundError, EOFError):
		print("Error: Could not load the game.")
		return player

class NPC:
	def __init__(self, name, items):
		self.name = name
		self.items = items

	def trade(self, player, player_item, npc_item):
		if npc_item in self.items and player_item in player.inventory:
			self.items.remove(npc_item)
			self.items.append(player_item)
			player.inventory.remove(player_item)
			player.inventory.append(npc_item)
			return True
		return False

def describe_npc(room):
	if hasattr(room, 'npc'):
		print(f"{room.npc.name} is in the room.")
		print(f"{room.npc.name} has the following items for trade:", ", ".join(room.npc.items))

def handle_hint(player, usable_items):
	hints = {
		"key": "The key unlocks a door.",
		"book": "There's something hidden inside the book.",
		"map": "The map reveals the location of a secret door.",
		"candle": "The candle can light up a dark room.",
		"painting": "The painting hides a secret.",
		"hammer": "The hammer can break something.",
		"lever": "The lever opens a hidden door.",
		"gem": "The gem is valuable and can be traded.",
		"hidden_key": "The hidden key unlocks a chest.",
		"statue": "The statue is needed to escape the dungeon."
	}

	# Check if the player is close to winning
	if "key" in player.inventory and "treasure" in player.inventory and "statue" in player.inventory:
		print("You have collected all the items you need to escape the dungeon! Get to the room with the large door to escape.")
		return

	print("Hints:")
	for item in hints:
		# Check if the item is in the player's inventory
		if item in player.inventory:
			continue
		
		# Check if the item is needed to win the game
		if item in ["key", "treasure", "statue"]:
			print(hints[item])
			continue
		
		# Check if the item is usable in the current room
		if item in usable_items and player.room == usable_items[item]["room"]:
			print(hints[item])
		
	# Check if the player is missing any of the items needed to win the game
	if "key" not in player.inventory:
		print("You need the key to unlock the large door.")
	if "treasure" not in player.inventory:
		print("You need to find the hidden treasure.")
	if "statue" not in player.inventory:
		print("You need to find the ancient statue to escape the dungeon.")
	print()

	item = input("Which item do you need a hint for? ").lower()
	if item in hints:
		print(hints[item])
		if item in usable_items and player.room == usable_items[item]["room"]:
			print(usable_items[item]["message"])
	else:
		print("No hints available for that item.")
		
def main():
	# Create rooms
	room1 = Room("You find yourself in a dimly lit room, with cold stone walls. A mysterious "
				"voice tells you that you must find the hidden treasure to escape. "
				"There is a door to the east.")
	room2 = Room("You are in a room filled with dusty books and cobwebs. An ancient library "
				"perhaps? There are doors to the west and east.")
	room3 = Room("You enter a grand hall with a massive chandelier hanging above. Shadows flicker "
				"on the walls. There are doors to the north, west, and east.")
	room4 = Room("You are in a small room with the remains of a feast on a long table. "
				"It looks like it has been abandoned for years. There is a door to the north.")
	room5 = Room("You are in a room filled with eerie paintings. Their eyes seem to follow you. "
				"There are doors to the north and west.")
	room6 = Room("You find yourself in a chamber with a large, cracked mirror on the wall. "
				"There are doors to the south, west, east, and north.")
	room7 = Room("You are in a room with a beautiful fountain, but the water is dark and murky. "
				"There are doors to the east, west, and north.")
	room8 = Room("You are in a room with walls covered in vines. Sunlight streams through a hole in the ceiling. There are doors to the east and south.")
	room9 = Room("You find yourself in a room filled with ancient statues. They look like guardians of something important. There is a door to the south.")
	room10 = Room("You enter a narrow corridor with walls covered in mysterious symbols. There are doors to the south and east.")
	room11 = Room("You are in a room with a large, ominous-looking door. It appears to be locked. There is a door to the west.")
	secret_room = Room("Congratulations! You found the secret room with the hidden treasure! "
					"A door to the south leads back to the fountain room.")
	dark_room = Room("You are in a pitch-black room. You can't see anything. There is a door to the south.")
	chest_room = Room("You are in a room with a locked chest in the center. There are doors to the west and east.")
	trading_room = Room("You are in a room with a mysterious figure standing in the corner, ready to trade items. There is a door to the east.")
	trader = NPC("Trader", ["torch", "mysterious_note"])
	guardian = NPC("Guardian", ["riddle_answer", "scroll"])
	trading_room.npc = trader
	room9.npc = guardian

	# Connect rooms
	room1.connect("east", room2)
	room2.connect("west", room1)
	room2.connect("east", room3)
	room3.connect("west", room2)
	room3.connect("south", room4)
	room3.connect("east", room5)
	room4.connect("north", room3)
	room5.connect("west", room3)
	room5.connect("north", room6)
	room6.connect("south", room5)
	room6.connect("east", room7)
	room6.connect("south", room8)
	room7.connect("north", secret_room)
	room7.connect("west", trading_room)
	room7.connect("east", room11)
	room8.connect("north", room6)
	room8.connect("east", room9)
	room9.connect("south", room10)
	room10.connect("south", room4)
	room10.connect("east", room11)
	room11.connect("west", room10)
	room11.connect("west", room7)
	secret_room.connect("south", room7)
	room3.connect("north", dark_room)
	dark_room.connect("south", room3)
	room6.connect("west", chest_room)
	chest_room.connect("east", room6)
	trading_room.connect("east", room7)

# Add items to rooms
	room1.add_item("key")
	room2.add_item("book")
	room3.add_item("map")
	room4.add_item("candle")
	room5.add_item("painting")
	room5.add_item("hammer")
	room6.add_item("lever")
	room7.add_item("gem")
	room8.add_item("vines")
	room9.add_item("statue")
	room10.add_item("mysterious_symbol")
	room11.add_item("large_door")
	secret_room.add_item("treasure")
	dark_room.add_item("hidden_door_map")
	chest_room.add_item("locked_chest")

# Create player and set initial values
	player = Player(room1)
	hidden_door_found = False

	# Print storyline and start game loop
	print_storyline(storyline)

	usable_items = {
		"key": {
			"room": room11,
			"message": "You can use the key to unlock the large door in the room with the large door."
		},
		"statue": {
			"room": room11,
			"message": "You can use the statue to escape the dungeon!"
		},
		"treasure": {
			"room": room11,
			"message": "You can use the treasure to escape the dungeon and win the game!"
		},
		"hidden_key": {
			"room": chest_room,
			"message": "You can use the hidden key to unlock the chest in the chest room."
		},
		"map": {
			"room": room3,
			"message": "You can use the map to reveal the location of a secret door in the grand hall."
		},
		"candle": {
			"room": dark_room,
			"message": "You can use the candle to light up the dark room."
		},
		"painting": {
			"room": room5,
			"message": "You can use the painting to reveal a hidden compartment in the room with eerie paintings."
		},
		"hammer": {
			"room": room6,
			"message": "You can use the hammer to break the cracked mirror in the room with the cracked mirror."
		},
		"lever": {
			"room": room6,
			"message": "You can use the lever to open the hidden door in the room with the lever."
		},
		"gem": {
			"room": trading_room,
			"message": "You can use the gem to trade with the mysterious figure in the trading room."
		}
	}

	while True:
		describe_room(player.room)
		describe_npc(player.room)
		check_win_condition(player)

		print("Usable items in the room: ", end="")
		for item in usable_items:
			if player.room == usable_items[item]["room"]:
				print(item, end=", ")
		print()

		action = input("What would you like to do? ").lower().split()
		if action[0] in ["pick", "pickup", "take"]:
			item = action[1]
			if item in player.room.items:
				player.pick_up(item)
				print(f"You picked up {item}.")
			else:
				print("That item is not in the room.")
		elif action[0] in ["use", "drop"]:
			if len(action) < 2:
				print("Please specify an item to use or drop.")
			else:
				item = action[1]
				if item in player.inventory:
					if item == "lever" and player.room == room6 and not hidden_door_found:
						room6.connect("north", secret_room)
						secret_room.connect("south", room6)
						print("You used the lever and discovered a hidden door to the north!")
						hidden_door_found = True
					elif item == "book" and player.room == room2:
						print("You open the book and find a hidden key inside!")
						player.use_item(item)
						player.pick_up("hidden_key")
					else:
						player.use_item(item)
						player.room.add_item(item)
						print(f"You dropped {item}.")
				else:
					print("That item is not in your inventory.")
		elif action[0] == "move":
			direction = action[1]
			if player.move(direction):
				print(f"You moved {direction}.")
			else:
				print("You cannot move in that direction.")
		elif action[0] == "save":
			save_game(player)
			print("Game saved.")
		elif action[0] == "load":
			player = load_game(player)
			print("Game loaded.")
		elif action[0] == "quit":
			break
		elif action[0] == "hint":
			handle_hint(player, usable_items)
		elif action[0] == "trade":
			if hasattr(player.room, 'npc'):
				trade_item = input(f"What item do you want to trade with {player.room.npc.name}? ").lower()
				if trade_item in player.inventory:
					for npc_item in player.room.npc.items:
						print(f"Offering {trade_item} for {npc_item}.")
						if player.room.npc.trade(player, trade_item, npc_item):
							print(f"Successfully traded {trade_item} for {npc_item}.")
							break
					else:
						print("The NPC doesn't want any of your items.")
				else:
					print("You don't have that item in your inventory.")
			else:
				print("There is no one to trade with in this room.")
		elif action[0] == "talk":
			if hasattr(player.room, 'npc'):
				npc = player.room.npc
				if npc.name == "Guardian":
					if "riddle_answer" in npc.items:
						solve_riddle(player)
					else:
						print("The Guardian has nothing more to say.")
				else:
					print(f"{npc.name} has nothing to say.")
			else:
				print("There is no one to talk to in this room.")
		else:
			print("Invalid command.")

if __name__ == "__main__":
	main()
