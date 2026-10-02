class Pet:
    def __init__(self, name):
        self.name = name
        self._fullness = 50
        self._happiness = 50
        self.sleep_count = 0 
    @property
    def fullness(self):
        return self._fullness

    @fullness.setter
    def fullness(self, value):
        if value > 100:
            self._fullness = 100
        elif value < 0:
            self._fullness = 0
        else:
            self._fullness = value
    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        if value > 100:
            self._happiness = 100
        elif value < 0:
            self._happiness = 0
        else:
            self._happiness = value
    @property
    def is_alive(self):
        return self.fullness > 0
    @property
    def mood(self):
        if not self.is_alive:
            return "Dead"
        elif self.fullness < 30:
            return "Hungry"
        elif self.happiness < 30:
            return "Bored"
        elif self.fullness >= 70 and self.happiness >= 70:
            return "Happy"
        else:
            return "Normal"
    def feed(self):
        self.fullness += 20
        print(f"{self.name} enjoyed the delicious food!")

    def play(self):
        self.happiness += 25
        self.fullness -= 15
        print(f"{self.name} is playing and having fun!")
    def pass_time(self):
        self.fullness -= 10
        self.happiness -= 10

    def show(self):
        print(f"{self.name} | Fullness: {self.fullness} | Happiness: {self.happiness} | Mood: {self.mood}")
def main():
    print("Welcome to Virtual Pet!")
    pet_name = input("Name your pet: ")
    my_pet = Pet(pet_name)
    
    turn = 1
    max_turns = 10

    while turn <= max_turns and my_pet.is_alive:
        print(f"\n--- Turn {turn} ---")
        my_pet.show()
        print("1. Feed  2. Play  3. Skip  4. Sleep")
        choice = input("Choose: ").strip()
        if choice == '1':
            my_pet.feed()
        elif choice == '2':
            my_pet.play()
        elif choice == '3':
            print(f"{self.name if 'self' in locals() else my_pet.name} rests this turn.")
        elif choice == '4':

            if not my_pet.sleep():
                continue
        else:
            print("Invalid input! Please choose 1, 2, 3, or 4.")
            continue
        

        my_pet.pass_time()
        turn += 1
    print("\n====================")
    if my_pet.is_alive:
        print(f"Congratulations! Your pet {my_pet.name} survived all 10 turns!")
        my_pet.show()
        print(f"Game Over. Sadly, your pet {my_pet.name} has died.")
    print("====================")

if __name__ == "__main__":
    main()
