from operator import itemgetter
from random import randint

initiative_sorted = []
drop_counter = 15
first_round = 1
first_turn = 0


def info_gather(round_count, turn_count):
    """
    function to initialize the initiative tracker, ask for combatant info,
    and build a list of dictionaries with initiative counts in order
    """
    global initiative_sorted
    # Prompts user for input of a list of combatants and their initiatives
    temp_name_holder = input("Please enter a combatants name, or enter done:")
    if temp_name_holder != "done":
        temp_initiative_holder = input(f"What is {temp_name_holder}'s initiative?")
        # Checks that the input for initiative and dex mod  are integers, prompting the user for another input if not
        # Also, appends the combatant name, initiative, and dex mod to a list of dictionaries (combatant_list)
        try:
            temp_initiative_holder = int(temp_initiative_holder) * 100
            temp_dexmod_holder = input(f"What is {temp_name_holder}'s dex mod?")
            try:
                temp_dexmod_holder = int(temp_dexmod_holder)
                # Creates a temporary dictionary holding combatant name, initiative, and dex mod
                temp_dict = {'Name': temp_name_holder, 'Initiative': temp_initiative_holder,
                             'Dex Mod': temp_dexmod_holder}
                # Appends the temp dictionary into the combatant list
                initiative_sorted.append(dict.copy(temp_dict))
                info_gather(round_count, turn_count)
            except ValueError:
                print("Dex Mod has to be an integer , lets try entering that info again...")
                info_gather(round_count, turn_count)
        except ValueError:
            print("Initiative has to be an integer , lets try entering that info again...")
            info_gather(round_count, turn_count)
    else:
        initiative_sorted = sorted(initiative_sorted, key=itemgetter('Initiative', 'Dex Mod'), reverse=True)
        combat_turn(round_count, turn_count)


def combat_turn(round_count, turn_count):
    global initiative_sorted
    global drop_counter
    if turn_count == 0:
        print("The initiative order is:\n")
        for i in initiative_sorted:
            print(f"{i['Name']}")
        print(f"\nIt's round {round_count}")
    if turn_count + 1 < len(initiative_sorted):
        print(f"\n{initiative_sorted[turn_count]['Name']} You're up!")
        print(f"{initiative_sorted[turn_count + 1]['Name']} You're on deck\n")
    else:
        print(f"\n{initiative_sorted[turn_count]['Name']} You're up!")
        print(f"{initiative_sorted[0]['Name']} You're on deck\n")
    action = input("Enter an action(next, info, order, add, drop, dead, combat over):")
    if action == "info":
        print("info will print out a list of commands and what they do\n"
              "order will print out the initiative order\n"
              "add will add prompt you to add another combatant into initiative\n"
              "drop will prompt you for the position the active player wants to drop to, and re-sort them there\n"
              "dead will kill the active player and remove them from initiative\n"
              "combat over will end the initiative sequence\n")
        combat_turn(round_count, turn_count)
    elif action == "order":
        print("The initiative order is:\n")
        for i in initiative_sorted:
            print(f"{i['Name']}")
        print(f"\nIt's round {round_count}")
        combat_turn(round_count, turn_count)
    elif action == "add":
        info_gather(round_count, turn_count)
    elif action == "drop":
        drop_to = input("\nWho would you like to drop after?")
        new_init = next(item for item in initiative_sorted if item["Name"] == drop_to)["Initiative"]
        initiative_sorted[turn_count]['Initiative'] = new_init - drop_counter
        drop_counter -= 1

        combat_turn(round_count, turn_count)
    elif action == "dead":
        message_num = randint(1, 100)
        if message_num < 20:
            print(f"\nThey should not have stood against a greater foe, {initiative_sorted[turn_count]['Name']} has "
                  f"perished!")
        elif message_num < 40:
            print(f"\nOuch! Did you see {initiative_sorted[turn_count]['Name']} die?")
        elif message_num < 60:
            print(f"\nAnother has fallen, just as prophesized. {initiative_sorted[turn_count]['Name']} is slain.")
        elif message_num < 80:
            print(f"\nDeath is a cruel mistress... {initiative_sorted[turn_count]['Name']} stands before her now.")
        elif message_num < 95:
            print(f"\nThe weave is threadbare. Was {initiative_sorted[turn_count]['Name']} supposed to fall?")
        else:
            print(f"\n{initiative_sorted[turn_count]['Name']} died. Fucking nerd.")
        initiative_sorted.pop(turn_count)
        combat_turn(round_count, turn_count)
    elif action == "combat over":
        print("\nPhew, fights over. Hope nobody important died.")
        exit()
    else:
        turn_count += 1
        if turn_count >= len(initiative_sorted):
            turn_count = 0
            round_count += 1
        combat_turn(round_count, turn_count)


info_gather(first_round, first_turn)