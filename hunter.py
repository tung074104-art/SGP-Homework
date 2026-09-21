from random import randint

class Hero():
    # constructor
    def __init__(self, name,potion,weapon,mana,armour,dmg,hero_rank,hero_type):
        self.name = name
        self.potion = potion
        self.mana = mana
        self.armor = armour
        self.dmg = dmg
        self.weapon = weapon
        self.hero_type = hero_type
        self.hero_rank = hero_rank
    # method print info
    def introduce(self):
        print(f"====> Hero: {self.name} <====")
        print(f"- Hero type: {self.hero_type}")
        print(f"- Health: {self.hp}")
        print(f"- Stamina: {self.mana}")
        print(f"- Armor: {self.armor}")
        print(f"- Ability: {self.skill}")
        print(f"- Damage: {self.dmg}")
        print(f"- Potion: {self.potion}")
        print(f"- Weapon: {self.weapon}")
        print(f"- Hero rank: {self.hero_rank}")
        print("======================")

    def strike(self, enemy):
        rateMin = 0.2
        rateMax = 0.2
        if (self.hero_type == "Tanker"):
            rateMin = 0.1
            rateMax = 0.1
        elif (self.hero_type == "Archer"):
            rateMin = 0.2
            rateMax = 0.6
        elif (self.hero_type == "Mage"):
            rateMin = 0.3
            rateMax = 0.5
        elif (self.hero_type == "Striker"):
            rateMin = 0.2
            rateMax = 0.6
                    
        actualDmg = randint(self.dmg - self.dmg * rateMin, self.dmg + self.dmg * rateMax)
        print(f'🔥 STRIKE! {self.name} attacked {enemy.name} - 🥊 DMG:{actualDmg}')
        

hero1 = Hero("Salt","tanker",5000,4500,"no armor",
hero2 = Hero()
hero1.introduce()