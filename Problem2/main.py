input_file = 'inputPS11Q2.txt'
output_file = 'outputPS11Q2.txt'
# Weapons : 6
# MaxWeight : 118
# Weapon Name / Weight / Damage
# A1 / 10 / 20
# A2 / 30 / 40

MAX_WEAPONS: int = 0
MAX_WEIGHT: int = 118


class Items:
    def __init__(self, name: str, weight: int, damage: int):
        self.name = name
        self.weight = weight
        self.damage = damage
        self.power = damage / weight


def read_inputs():
    all_inputs = []
    f = None
    f = open(input_file, "r")
    for line in f.readlines():
        temp = process_inputs(line)
        if len(temp) > 0:
            all_inputs.append(temp)
    return all_inputs


def process_inputs(input_str):
    global MAX_WEAPONS
    global MAX_WEIGHT
    current_inputs = []
    x = None
    if 'Weapons' in input_str:
        x = input_str.split(':')
        MAX_WEAPONS = int(x[1].strip())
    elif 'MaxWeight' in input_str:
        x = input_str.split(':')
        MAX_WEIGHT = int(x[1].strip())
    elif '/' in input_str:
        input_str = input_str.strip()
        x = input_str.split('/')
        if len(x) == 3:
            current_inputs.append(x[0].strip())
            current_inputs.append(x[1].strip())
            current_inputs.append(x[2].strip())

        else:
            print('Invalid input string.')
    return current_inputs


def print_to_file(std_str):
    f = None
    try:
        # print('Writing {}'.format(std_str))
        f = open(output_file, 'a')
        print(std_str, file=f)

    except IOError as e:
        print('Could not write to output file')
    finally:
        if f is not None:
            f.close()


def do_greedy_distribution(all_weapons, fill_small_power_first=False):
    used_capacity = 0
    total_power = 0
    used_weapon = 0
    global MAX_WEIGHT
    global MAX_WEAPONS
    # sort the weapons based on power
    if fill_small_power_first:
        all_weapons.sort(key=lambda x: x.power, reverse=False)
    else:
        all_weapons.sort(key=lambda x: x.power, reverse=True)
    for weapon in all_weapons:
        current_capacity = used_capacity + weapon.weight
        if current_capacity <= MAX_WEIGHT and used_weapon <= MAX_WEAPONS:
            print(
                'Fully using [{}] with power [{}], weight [{}] and damage [{}]'.format(weapon.name, weapon.power,
                                                                                       weapon.weight, weapon.damage))
            print_to_file('{} > 1'.format(weapon.name))
            used_capacity = used_capacity + weapon.weight
            used_weapon = used_weapon + 1
            total_power = total_power + weapon.damage
        else:

            unused = MAX_WEIGHT - used_capacity
            percent_used = (unused / weapon.weight)
            value = weapon.power * unused
            print(
                'Partially [{}] using [{}] with power [{}], weight [{}] and damage [{}]'.format(percent_used,
                                                                                                weapon.name,
                                                                                                weapon.power,
                                                                                                weapon.weight,
                                                                                                weapon.damage))
            print_to_file('{} > {}'.format(weapon.name, percent_used))
            used_capacity = used_capacity + unused
            total_power = total_power + value

        if used_capacity == MAX_WEIGHT:
            break
    print_to_file("Total Damage: " + str(total_power))


def clear_output_file():
    import os
    try:
        os.remove(output_file)
    except IOError as e:
        print('Could not delete the output file')


def entry():
    clear_output_file()
    input_weapons = read_inputs()
    all_weapons = []
    # add weapons and calculate the power (damage/weight)
    for weapon in input_weapons:
        # print('Inserting [{}] with damage [{}]'.format(weapon[1], weapon[2]))
        item = Items(weapon[0], int(weapon[1]), int(weapon[2]))
        all_weapons.append(item)
    do_greedy_distribution(all_weapons)


entry()
