from random import randint


def calculate(number_of_attacks, ac, to_hit, damage_per_hit=None, advantage=False, disadvantage=False, dmg_mode=False):
    """ Simulates attacks to figure out how many hit and, if damage per hit is given, what damage was dealt.
        If in DMG mode, the table provided in the Dungeon Master's Guide is used instead.

    :param number_of_attacks: The number of single attacks
    :param ac: The armor class of the defending creature
    :param to_hit: The to hit bonus of the attacking creatures
    :param damage_per_hit: The average damage per hitting attack
    :param advantage: Do the attacks occur with advantage?
    :param disadvantage: Do the attacks occur with disadvantage?
    :param dmg_mode: Use the table in the Dungeon Master's Guide instead of simulating each attack?
    :return: If no damage was provided: The number of attacks hitting the defending creature.
    Otherwise: A pair of the number of attacks hitting the defending creature and total damage dealt by those attacks.
    """
    hits = number_of_hits(ac, advantage, disadvantage, dmg_mode, number_of_attacks, to_hit)

    if damage_per_hit is not None:
        return hits, damage_per_hit * hits
    else:
        return hits


def number_of_hits(number_of_attacks, ac, to_hit, advantage=False, disadvantage=False, dmg_mode=False):
    """ Simulates attacks to figure out how many hit. Also returns the number of critical hits, if not in DMG mode.
    If in DMG mode, the table provided in the Dungeon Master's Guide is used instead.

    :param number_of_attacks: The number of single attacks
    :param ac: The armor class of the defending creature
    :param to_hit: The to hit bonus of the attacking creatures
    :param advantage: Do the attacks occur with advantage?
    :param disadvantage: Do the attacks occur with disadvantage?
    :param dmg_mode: Use the table in the Dungeon Master's Guide instead of simulating each attack?
    :return: The number of attacks hitting the defending creature and the number of critical ones, if not in DMG mode.
    """
    hits = 0
    critical_hits = 0
    if dmg_mode:
        attackers_needed_for_one_hit = dmg_mob_attack(ac - to_hit)
        hits = number_of_attacks // attackers_needed_for_one_hit
    else:
        for _ in range(number_of_attacks):
            roll = randint(1, 20)
            if advantage:
                roll = max(roll, randint(1, 20))
            elif disadvantage:
                roll = min(roll, randint(1, 20))
            if roll == 20:
                hits += 1
                critical_hits += 1
            elif roll != 1 and roll + to_hit >= ac:
                hits += 1

    return hits, critical_hits


def dmg_mob_attack(d20_roll_needed):
    """ Table from the Dungeon Master's Guide to lookup the number of attackers needed for one hit based on the d20 roll
    needed to hit the defending creature. This disregards advantage, disadvantage, critical hits, and critical failures.

    :param d20_roll_needed: The d20 roll needed for an attack to hit
    :return: The number of attackers needed for one hit
    """
    if 1 <= d20_roll_needed <= 5:
        return 1
    if 6 <= d20_roll_needed <= 12:
        return 2
    if 13 <= d20_roll_needed <= 14:
        return 3
    if 15 <= d20_roll_needed <= 16:
        return 4
    if 17 <= d20_roll_needed <= 18:
        return 5
    if d20_roll_needed == 19:
        return 10
    if d20_roll_needed <= 20:
        return 20
