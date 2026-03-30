# Author: Daniel Walker, Colby Seeley, Adam Halliday
# Program conducts a pokemon battle!
import random


# Move class with various move attributes and attack value and formatted string return methods
class Move:
    def __init__(
        self, move_name, elemental_type, low_attack_points, high_attack_points
    ):
        self.move_name = move_name
        self.elemental_type = elemental_type
        self.low_attack_points = low_attack_points
        self.high_attack_points = high_attack_points

    # Method to return all associated information with the move class/object
    def get_info(self):
        return f"{self.move_name} (Type: {self.elemental_type}): {self.low_attack_points} to {self.high_attack_points} Attack Points"

    # Method to to randomly generate an attack points value that is subsequently returned
    def generate_attack_value(self):
        return random.randint(self.low_attack_points, self.high_attack_points)


class Pokemon:
    def __init__(self, name: str, element_type: str, hit_points: int):
        self.name = name
        self.element_type = element_type
        self.hit_points = hit_points

    # Returns info on a pokemon
    def get_info(self):
        pass
        print(
            f"{self.name} - Type: {self.element_type} - Hit Points: {self.hit_points}"
        )

    def heal(self):
        self.hit_points += 15
        print(f"{self.name} has been healed to {self.hit_points} hit points.")


# Main program
# List to create/store the 9 move objects
moves = [
    Move("Tackle", "Normal", 5, 20),
    Move("Quick Attack", "Normal", 6, 25),
    Move("Slash", "Normal", 10, 30),
    Move("Flamethrower", "Fire", 5, 30),
    Move("Ember", "Fire", 10, 20),
    Move("Water Gun", "Water", 5, 15),
    Move("Hydro Pump", "Water", 20, 25),
    Move("Vine Whip", "Grass", 10, 25),
    Move("Solar Beam", "Grass", 18, 27),
]

# Loop that runs 3 times that randomly selects an object, obtains its info, and generates an attack value
for iCount in range(0, 3):
    random_key = random.randint(0, len(moves)-1)
    move = moves[random_key]
    print(move.get_info())
    print(f"Generated attack value: {move.generate_attack_value()}")
    moves.pop(random_key)

# Adds pause in the program through the use of an input function and a while loop
while True:
    user_continue = input("Press enter to continue...")
    if user_continue == "":
        break


# Initalizes each pokemon and stores objects to list
oPokemonBulbasuar = Pokemon("Bulbasuar", "Grass", 60)
oPokemonCharmander = Pokemon("Charmander", "Fire", 55)
oPokemonSquirtle = Pokemon("Squirtle", "Water", 65)

list_pokemon = [
    oPokemonBulbasuar,
    oPokemonCharmander,
    oPokemonSquirtle
]

# Print charmander's info and heal
oPokemonCharmander.get_info()
oPokemonCharmander.heal()

# Prints get_info for each pokemon
for pokemon in list_pokemon:
    pokemon.get_info()