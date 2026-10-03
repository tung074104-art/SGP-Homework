from random import randint
import time
class Hero():
    # constructor
    def __init__(self, name,hp,weapon,mana, armor, dmg,hero_type):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.armor = armor
        self.dmg = dmg
        self.weapon = weapon
        self.hero_type = hero_type
    # method print info
    def introduce(self):
        print(f"====> Hero: {self.name} <====")
        print(f"- Hero type: {self.hero_type}")
        print(f"- Health: {self.hp}")
        print(f"- stamina: {self.mana}")
        print(f"- Armor: {self.armor}")
        print(f"- Weapon: {self.weapon}")
        print(f"- Damage: {self.dmg}")
        print("======================")

    def strike(self, enemy):
        rateMin = 0.2
        rateMax = 0.2
        if (self.hero_type == "tanker"):
            rateMin = 0.1
            rateMax = 0.1
        if (self.hero_type == "swordman"):
            rateMin = 0.2
            rateMax = 0.6
        if (self.hero_type == "spearman"):
                rateMin = 0.3
                rateMax = 0.2
        
        actualDmg = randint(round(self.dmg - self.dmg * rateMin), round(self.dmg + self.dmg * rateMax))
        print(f'🔥 STRIKE! {self.name} attacked {enemy.name} - 🥊 DMG:{actualDmg}')
        enemy.armor -= actualDmg
        if enemy.armor < 0:
            enemy.hp += enemy.armor
            enemy.armor = 0
        if enemy.hp <= 0:
            enemy.hp = 0
        print("=========================================")
        print(f'STRIKE! Hero🦸{enemy.name} has been hit!')
        print(f'Armor🪖: {enemy.armor} ')
        print(f'Hp❤️‍🩹: {enemy.hp}')

    def fight(self,enemy):
        while self.hp > 0 and enemy.hp > 0:
            self.strike(enemy)
            if enemy.hp <= 0:
                print(f'Hero {enemy.name} has fallen!☠️')
                break
            time.sleep(2)
            enemy.strike(self)
            if self.hp <= 0:
                print(f'Hero {enemy.name} has fallen!☠️')
                break
            time.sleep(2)
Arthur = Hero("Arthur", 1500,'Sword and shield⚔️🛡️', 3000, 4500, 800, 'tanker')
Charles = Hero("Charles", 1500,'Bow🏹', 5000, 900, 2000, "archer")
Richard = Hero("Richard", 1500,'Spear🗡️', 4000, 1000, 2500, "spearman")
print("Welcome to the Arena of Valor")
print('Please select the type of mission: ')
mission = int(input("0 - Exit the game \n1 -Introduce your self \n2 - Attack enemy \n: " ))
while mission != 0:
    if mission == 1:
        Arthur.introduce()
    if mission == 2:
        print("What boss do you want to fight?")
        type = int(input("1 - Charles \n2 - Richard: \n:"))
        if type == 1:
            print("Enemy info:")
            Charles.introduce()
            time.sleep(3)
            Arthur.fight(Charles)            
        if type == 2:
            Richard.introduce()
            time.sleep(3)
            Arthur.fight(Richard)

        if Arthur.hp > 0:
            print("You win! 🏆")
            Arthur.hp += round(Arthur.hp * 0.2)
            Arthur.dmg += round(Arthur.dmg * 0.1)
        else:
            print("You lose!!!")
    mission = int(input("0 - Exit \n1 - Introduce your self \n2 - Attack enemy\n"))
