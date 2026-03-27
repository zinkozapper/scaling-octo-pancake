#Author: Daniel Walker, Colby Seeley, Adam Halliday
#Program conducts a pokemon battle!

class Pokemon():
    def __init__(self, name: str, element_type: str, hit_points: int):
        self.name = name
        self.element_type = element_type
        self.hit_points = hit_points

    #Returns info on a pokemon
    def get_info(self):
        pass
        print(f"{self.name} - Type: {self.element_type} - Hit Points: {self.hit_points}")

    def heal(self):
        self.hit_points += 15
        print(f"{self.name} has been healed to {self.hit_points} hit points.")


#Initalizes each pokemon
oPokemonBulbasuar = Pokemon("Bulbasuar", "Grass", 60)
oPokemonCharmander = Pokemon("Charmander", "Fire", 55)
oPokemonSquirtle = Pokemon("Squirtle", "Water", 65)

#Gets all the pokemon info
oPokemonBulbasuar.get_info()
oPokemonCharmander.get_info()
oPokemonSquirtle.get_info()

#Heals each pokemon. This is mostly for example. Move or delete.
oPokemonBulbasuar.heal()
oPokemonCharmander.heal()
oPokemonSquirtle.heal()
