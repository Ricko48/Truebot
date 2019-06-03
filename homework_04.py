"""

Autor: Richard Ondrejka, 485630

Prohlašuji, že celý zdrojový kód jsem zpracoval zcela samostatně.
Jsem si vědom, že  nepravdivost tohoto tvrzení může být důvodem
k hodnocení F v předmětu IB111 a k disciplinárnímu řízení.


"""

from collections import deque

from random import random, randint

import sys

"""

!!!Samotna hra sa spusta fukciou 'game()'!!!

"""

"""

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


class Player:
    def __init__(self, name, equipped_weapon, skills, hp=500, ep=100):
        self.name = name
        self.hp = hp
        self.ep = ep
        self.equipped_weapon = equipped_weapon
        self.skills = skills
        self.default_hp = hp  # parameter default_... sluzi na ulozenie pociatocnej hodnoty EP alebo HP
        self.default_ep = ep

    def __str__(self):
        return '{}  |  HP: {}/{}  |  EP: {}/{} \n' \
               'Your weapon:    {} \nYour skills: ' \
            .format(self.name, self.hp, self.default_hp, self.ep, self.default_ep, self.equipped_weapon)

    def hp_increase(self):  # funkcia sluzi na zvysenie HP hraca po prekonani miestnosti o 20
        if (self.hp + 20) > self.default_hp:
            self.hp = self.default_hp
        else:
            self.hp += 20

    def hp_decrease(self, damage):  # funkcia sluzi na znizenie HP o damage prislusneho skilu
        if (self.hp - damage) < 0:
            self.hp = 0
        else:
            self.hp -= damage

    def ep_increase(self, value):  # funkcia sluzi na zvysenie EP po skonceni kola a po prekonani miestnosti
        if (self.ep + value) > self.default_ep:
            self.ep = self.default_ep
        else:
            self.ep += value

    def ep_decrease(self, value):  # funkcia sluzi na znienie ep po pouziti prislusneho skilu
        if (self.ep - value) < 0:
            self.ep = 0
        else:
            self.ep -= value


"""

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


class Monster:
    def __init__(self, name, skills, hp, ep):
        self.name = name
        self.hp = hp
        self.ep = ep
        self.skills = skills
        self.default_hp = hp
        self.default_ep = ep

    def __str__(self):
        return '{}  |  HP: {}/{}  |  EP: {}/{} \n{} skills: ' \
            .format(self.name, self.hp, self.default_hp, self.ep, self.default_ep, self.name)

    def full_hp_increase(self):  # po zabiti prisery v room sa jej doplni full hp
        self.hp = self.default_hp

    def hp_decrease(self, damage):  # znizenie hp o damage
        if (self.hp - damage) < 0:
            self.hp = 0
        else:
            self.hp -= damage

    def ep_increase(self, value):  # zvysenie ep po skonceni kola a po umrti v miestnosti
        if (self.ep + value) > self.default_ep:
            self.ep = self.default_ep
        else:
            self.ep += value

    def ep_decrease(self, value):  # znizenie ep o prislusny energy cost skilu
        if (self.ep - value) < 0:
            self.ep = 0
        else:
            self.ep -= value


"""

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


class Skill:
    def __init__(self, name, damage, energy_cost, probability):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
        self.probability = probability

    def __str__(self):
        return '{} - Damage: {}  |  Energy cost: {}  |  Chance of hit: {}' \
            .format(self.name, self.damage, self.energy_cost, self.probability)


"""

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


class Weapon:
    def __init__(self, name, damage, probability):
        self.name = name
        self.probability = probability
        self.damage = damage

    def __str__(self):
        return '{}  |  Damage: {}  |  Chance of hit: {}'.format(self.name, self.damage, self.probability)


"""

Trieda Room obsahuje atributy 'number' - cislo poradia miestnosti vo fronte a 'monsters' - slovnik
s triedami priser ktore miestnost obsahuje, key v slovniku tvori cislo ako poradie priseri, a value ako triedu
danej prisery.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


class Room:
    def __init__(self, number, monsters):
        self.number = number
        self.monsters = monsters


"""

Funkcia sluzi na vyber mena na zaciatku hry.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


def choose_name():
    while 1:
        name = input("Choose your heroic name: ")
        if len(name) > 25:
            print("You cant type name longer than 25 symbols. Try type a new one.")
        elif len(name) < 1:
            print("You have to type something.")
        else:
            break
    return name


"""

Funkcia sluzi na vyber charakteru.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


def choose_character():
    while 1:
        character = input("Choose your character (mage / hunter): ")
        if character == "mage" or character == "hunter":
            return character
        else:
            print("You typed illegal character. Try type again.")


"""

funkcia sluzi na vyber z troch obtiaznosti na zaciatku hry.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


def choose_difficult():
    while 1:
        difficult_ = input("Tell me how difficult your journey should be? (e / m / h): ")
        print()
        if difficult_ == "m" or difficult_ == "e" or difficult_ == "h":
            return difficult_
        else:
            print("You typed illegal symbol. Try type again.")


"""

Funkcia sluzi na overenie zasahu podla pravdepodobnosti zasahu prislusnenj zbrane.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


def prob_hit(probability):
    number = random()
    if number > probability:
        return False
    else:
        return True


"""

Funkcia sluzi na kompletny vypis hraca a priser v miestnosti

zname nedostatky: myslim ze ok akurat by sa dalo vylepsit yvpisovanie skillov
styl: myslim ze ok

"""


def status(room, player):
    print("<><><YOUR CHARACTER><><>", "\n")
    print(player)
    for i in player.skills.values():
        print(i)
    print(2 * "\n" + "<><><MONSTERS><><>", "\n")
    for key, value in room.monsters.items():
        print(str(key) + ". ", value)
        for j in value.skills.values():
            print(j)
        print()


"""

Funkcia overi vysku ep pre nejaky z jeho skilov.

zname nedostatky: myslim ze ok
styl: myslim ze ok

"""


def enough_ep_for_any_skill(player):
    for i in player.skills.values():
        if i.energy_cost <= player.ep:
            return True
    return False


"""

Funkcia vytvori frontu s miestnostami a priserami pre podla prislusnej obtiaznosti

zname nedostatky: myslim ze trochu zbytocne zlozite
styl: myslim ze ok

"""


def make_deque(difficult, monster_dict):
    list_rooms = []
    list_count_monsters = []
    for i in range(len(list(monster_dict))):  # vytvorenie zoznamu s cislami zodpovedajucimi poctu priser
        list_count_monsters.append(i)

    room_ = "room_"
    queue = deque([])
    if difficult == "e":
        count_rooms = 4
        output = False

    elif difficult == "m":
        number_1 = 1
        number_2 = 2
        count_rooms = 6
        output = True

    elif difficult == "h":
        number_1 = 2
        number_2 = 3
        count_rooms = 8
        output = True

    for i in range(count_rooms):
        list_rooms.append(room_ + str(i))
        list_rooms[i] = Room(i, {})
        if output:
            count_monsters = randint(number_1, number_2)  # podla obtiaznosti sa vygeneruje pocet priser v miestnosti
            for j in range(count_monsters):
                output = True
                while output:
                    output = False
                    number = list_count_monsters[randint(0, len(list_count_monsters) - 1)]
                    for k in list_rooms[i].monsters.values():
                        if k == monster_dict[number]:
                            output = True
                            list_count_monsters.remove(number)
                            break

                list_rooms[i].monsters[j] = monster_dict[number]
            queue.append(list_rooms[i])

        else:  # ak je obtiaznost easy tak je pocet priser pevne stanoveny na jednu v kazdej miestnosti
            number = randint(0, len(list(monster_dict)) - 1)
            list_rooms[i].monsters[0] = monster_dict[number]
            queue.append(list_rooms[i])

    return queue


'''

Funkcia sluzi na boj hraca s priserou a pre boj priser s hracom.

zname nedostatky: myslim ze ok
styl: myslim ze ok

'''


def fight(player, monster, who_attacks, weapon_option, used_skill_or_weapon):
    if who_attacks == 0:  # ak utoci hrac
        if weapon_option == 0:  # ak hrac utoci skilom
            if prob_hit(player.skills[used_skill_or_weapon].probability):  # overenie zasahu
                monster.hp_decrease(player.skills[used_skill_or_weapon].damage)  # znizenie HP prisery
                print(">>>> You dealt", player.skills[used_skill_or_weapon].damage, "damage to", monster.name, "<<<<")
            else:
                print(">>>> You missed <<<<")
        else:  # ak hrac utoci zbranou
            if prob_hit(player.equipped_weapon.probability):  # overenie zasahu
                monster.hp_decrease(player.equipped_weapon.damage)  # znizenie HP prisery
                print(">>>> You dealt", player.equipped_weapon.damage, "damage to", monster.name, "<<<<")

            else:
                print(">>>> You missed <<<<")

    else:  # ak utoci prisera
        if prob_hit(used_skill_or_weapon.probability):  # overenie zasahu
            player.hp_decrease(used_skill_or_weapon.damage)  # znizenie HP hraca
            print(">>>>", monster.name, "used", used_skill_or_weapon.name, "and dealt",
                  used_skill_or_weapon.damage, "damage to you <<<<")

        else:
            print(">>>>", monster.name, "used", used_skill_or_weapon.name, "and missed <<<<")
        print()


'''

Funkcia sluzi na priebeh deja v miesnotiach pocas hry. Funkcia skonci pokial zomrie hrac alebo
vsetky prisery v miestnosti. Funkcia taktie overuje ci hrac vyhral celu hru.

zname nedostatky: myslim ze overovanie datovych vstupov by sa dalo nejako zjednodusit
styl: trochu copy-past

'''


def room_rounds(room, player, queue):
    while 1:
        status(room, player)  # vypis postav
        output = False
        while output is False:
            output = True
            try:
                target = int(input("Please select target (number): "))  # vyber ciela
            except ValueError:
                print("You must type a number. Please try again.")
                output = False
            if output:
                if target not in room.monsters:
                    print("You typed a wrong number. Please try again.")
                    output = False

        '''
        Ak hrac nema dostatok EP pre nejaky skil, hrac v boji automaticky pouzije zbran.
        '''

        if enough_ep_for_any_skill(player) is False:
            print("You don't have enough EP to use any skill, so you will fight with your equipped weapon.")
            used_weapon = 0

        else:
            while output:
                output = False
                try:  # vyber zbrane alebo skilu
                    used_weapon = int(input("Press 0 if you want attack with your weapon or"
                                            " press 1 if you want attack with your skill: "))

                except ValueError:
                    print("\n" + "You must press a number. Please try again.")
                    output = True

                if output is False:
                    if used_weapon != 1 and used_weapon != 0:
                        print("\n" + "You must press a number 0 or number 1. Please try again.")
                        output = True

        print()
        monster = room.monsters[target]  # z priser sa vyberie zadany ciel a priradi sa premennej 'monster'

        if used_weapon == 1:  # ak si hrac zvolil skil
            for key, value in player.skills.items():  # vypis skilov
                print(str(key) + ". ", value)

            while output is False:
                output = True

                try:
                    used_skill = int(input("Please select skill (number): "))  # vyber skilu

                except ValueError:
                    print("You must press a number. Please try again.")
                    output = False

                if output:
                    if used_skill > (len(list(player.skills)) - 1) or used_skill < 0:
                        print("You must press one of the numbers on the screen. Please try again.")
                        output = False
                if output:
                    if player.ep < player.skills[used_skill].energy_cost:  # ak hrac nema dostatok EP pre vybrany skil
                        print("\n" + "You don't have enough EP to use this skill. Please try another skill.")
                        output = False

            print()
            player.ep_decrease(player.skills[used_skill].energy_cost)  # znizenie hracovho EP o energy_cost skilu

            fight(player, monster, 0, 0, used_skill)  # funkcia pre boj hraca s priserou so skilom

        elif used_weapon == 0:
            fight(player, monster, 0, 1, player.equipped_weapon)  # funkcia pre boj hraca s priserou so zbranou

        if monster.hp <= 0:  # ak ma prisera EP <= 0 tak sa odstrani z miestnosti
            del room.monsters[target]
            monster.full_hp_increase()
            monster.ep_increase(monster.ep)
            print("\n" + "You killed", monster.name, "\n")

        if room.monsters == {}:  # ak je slovnik priser prazdny funkcia sa ukonci
            print("You killed all monsters in the room ", str(room.number + 1) + ".", "\n")
            if queue:  # ak fronta obsahuje miestnosti funkcia skonci
                return  # [room, player, queue]
            else:  # ak fronta neobsahuje dalsie miestnosti, hrac vyhral a cely program sa vypne
                print("This was a last room!", 2 * "\n" + "======YOU WON======")
                sys.exit()

        for opponent in room.monsters.values():  # vytvori sa zoznam s cislami, ktore oznacuju pocet skilov prisery
            list_skills_numbers = []
            for i in range(len(list(opponent.skills))):
                list_skills_numbers.append(i)

            output = True
            while output:  # nahodny vyber schopnosti pre priseru v boji
                number = list_skills_numbers[randint(0, (len(list_skills_numbers) - 1))]
                if opponent.ep >= opponent.skills[number].energy_cost:
                    output = False

                else:  # ak prisera nema dostatok ep vyberie sa iny skil
                    list_skills_numbers.remove(number)
                    if list_skills_numbers is False:
                        number = -1
                        output = False

            if number != -1:
                opponent.ep_decrease(opponent.skills[number].energy_cost)  # znizenie EP prisery
                fight(player, opponent, 1, 1, opponent.skills[number])  # boj prisery s hracom

                if player.hp <= 0:  # ak hracove HP <= 0 tak hrac prehral s cela hra sa vypne
                    print("\n" + ">>>>" + opponent.name, "killed you.", 3 * "\n" + "======YOU LOST======")
                    sys.exit()

            else:  # ak prisera nema dostatok EP pre nejaky skil nebude utocit
                print(">>>>", opponent.name, "don't have enough EP to attack <<<<")

            opponent.ep_increase(10)  # na konci kola sa kazdej prisere zvysi EP o 10
        player.ep_increase(10)  # na konci kola sa hracovi zvysi EP o 10
        print("\n" + "+10 EP for you and all monsters", 2 * "\n")
        print("======NEXT ROUND======", 2 * "\n")


"""

Hlavna funkcia hry.
Nakolko v zadani neboli definovane urcite veci, hru som spravil tak, ze na zaciatku sa hracovi prideli
zbran nahodne. Po najdeni vsetkych zbrani uz hrac nema moznost ziskat novu zbran.

zname nedostatky: myslim ze by sa to urcite dalo spravit jednoduchsie
styl: trosku copy-past

"""


def game():
    with open("skills.csv", "r") as input_file:  # ulozenie skilov do slovnika
        file = input_file.readlines()
    skill_dict = {}
    for line in file:
        line = line.split(",")
        skill_dict[line[0]] = Skill(line[0], int(line[1]), int(line[2]), float(line[3]))

    with open("monsters.csv", "r") as input_file:  # ulozenie priser do slovnika
        file = input_file.readlines()
    monster_dict = {}
    count = -1
    for line in file:
        line = line.split(",")
        line[3] = line[3].split(";")
        dict = {}
        count += 1
        count_2 = 0

        for i in line[3]:
            dict[count_2] = skill_dict[i]
            count_2 += 1
        monster_dict[count] = Monster(line[0], dict, int(line[1]), int(line[2]))

    with open("weapons.csv", "r") as input_file:  # nahranie zbrani do slovnika
        file = input_file.readlines()

    weapon_dict = {}

    for line in file:
        line = line.split(",")
        weapon_dict[line[0]] = Weapon(line[0], int(line[1]), float(line[2]))

    print("Welcome to the Dungeons and Pythons")
    print(35 * "-")
    name = (choose_name())  # vyber mena
    character = choose_character()  # vyber charakteru
    difficult = choose_difficult()  # vyber obtiaznosti
    skills = {}
    count = -1
    if character == "mage":  # podla vybraneho charakteru sa nahraju skili do slovnika skills
        with open("mage_skills.csv", "r") as input_file:
            file = input_file.readlines()

        for line in file:
            line = line.split(",")
            count += 1
            skills[count] = Skill(line[0], int(line[1]), int(line[2]), float(line[3]))

    elif character == "hunter":  # podla vybraneho charakteru sa nahraju skili do slovnika skills
        with open("hunter_skills.csv", "r") as input_file:
            file = input_file.readlines()

        for line in file:
            line = line.split(",")
            count += 1
            skills[count] = Skill(line[0], int(line[1]), int(line[2]), float(line[3]))

    queue = make_deque(difficult, monster_dict)  # vytvorenie fronty

    number = randint(0, len(list(weapon_dict)) - 1)  # vygenerovanie nahodnej zbrane pre hraca na zaciatku hry
    count = 0
    for key, value in weapon_dict.items():
        if count == number:
            default_weapon = value
            del weapon_dict[key]
            break
        count += 1

    player = Player(name, default_weapon, skills)  # vytvorenie hracovej postavy

    print("You have to cross " + str(len(queue)) + " rooms.", "\n")
    print("GOOD LUCK!", 2 * "\n")

    while 1:  # cyklus hry
        room = queue.popleft()  # z fronty sa 'popne' miestnost
        print("======YOU ENTERED ROOM " + str(room.number + 1) + ".======", 2 * "\n")
        room_rounds(room, player, queue)  # zavola sa funkcia pre priebeh hry v miestnosti

        if weapon_dict:  # ak este ostala nejaka zbran tak sa jedna vyberie a ponukne sa hracovi
            count = 0
            number = randint(0, (len(list(weapon_dict)) - 1))
            for key, value in weapon_dict.items():
                if count == number:
                    found_weapon = value
                    del weapon_dict[key]
                    break

                count += 1

            print("You found:  ", found_weapon)
            output = True
            while output:
                output = False
                agree = input("Do you want to equip it? (y / n): ")
                if agree != "y" and agree != "n":
                    print("You must type y or n. Please try again.")
                    output = True

            if agree == "y":  # ak hrac suhlasi, prideli sa mu nova zbran
                player.equipped_weapon = found_weapon

        else:  # ak hrac uz nasiel vsetky zbrane, ziadna mu nebude ponuknuta
            print("You have already found all weapons. There's no more to get.")

        print("\n" + "======YOU LEFT ROOM " + str(room.number + 1) + ".======", 2 * "\n")
        player.hp_increase()  # zvysenie hracovho HP o 20 po prekonani miestnosti
        player.ep_increase(100)  # doplnenie hracovho EP do plna po prekonani miestnosti
        print("You got +20 HP and full EP", 2 * "\n")
