import os
import json
import random

#json target
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "effect.json"), "r", encoding="utf-8") as f:
    effect_pool = json.load(f)

with open(os.path.join(BASE_DIR, "parameter.json"), "r", encoding="utf-8") as f:
    parameter_pool = json.load(f)

#card color(type) as number
color_number = {"1": "Red",
                "2": "Blue",
                "3": "Green",
                "4": "Purple",
                "5": "Black",
                "6": "Grey"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#take effect(The effects and passives are still in Indonesian, but you can change them).
def take_effect(color,level):
    
    effect = effect_pool.get(color)
    if not effect:
        return("None", "None", "No Prefix", "No Suffix")
    lvl = effect.get(level)
    if not lvl:
        return("None", "None", "No Prefix", "No Suffix")
    
    prefix = random.choice(lvl["prefix"])
    suffix = random.choice(lvl["suffix"])
    passive = random.choice(lvl["passive"])
    support = random.choice(lvl["support"])
    if passive == "none":
        passive = None
    if support == "none":
        support = None
    return passive, support, prefix, suffix

#generate card parameter (you can change the value according to your want)
def card_parameter(color,level):
    try:
        color_data = parameter_pool.get(color)
        if not color_data:
            return f"color '{color}' not found"
        level_data = color_data.get(level)
        if not level_data:
            return f"Level '{level}' nor found for color '{color}'."
        hp = random.randrange(level_data["HP"][0], level_data["HP"][1]+1, 10)
        attack = random.randrange(level_data["ATK"][0], level_data["ATK"][1]+1, 10)
        defense = random.randrange(level_data["DEF"][0], level_data["DEF"][1]+1, 10)
        passive, support, prefix, suffix = take_effect(color,level)
        name = prefix + " " + suffix
        parameter = [

            {"Name": name},
            {"Color": color},
            {"Level": int(level)},
            {"HP": hp},
            {"ATK": attack},
            {"DEF": defense},
            {"Passive Effect": passive},
            {"Support Effect": support},
        ]
        return name, parameter
    except Exception as e:
        return f"Error: '{str(e)}"
    
#get id for cards
def get_next_id(color, level, filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                cards = json.load(f)
            except:
                cards = []
    else:
        cards = []

    max_num = 0
    color_abbreviation = {
        "Red": "RD", "Blue": "BL", "Green": "GN",
        "Purple": "PL", "Black": "BK", "Grey": "GY"
    }

    color_str = color_abbreviation.get(color, color)

    for card in cards:
        card_id = card.get("ID", "")
        if card_id.startswith(f"1-{color_str}-{level}-"):
            try:
                num = int(card_id.split("-")[-1])
                if num > max_num:
                    max_num = num
            except:
                continue

    return f"1-{color_str}-{level}-{max_num+1:03}"


#export to json
def export_to_json(card_data, filename= "generated_cards.json"):
    card_id = get_next_id(card_data["Color"], card_data["Level"], filename)
    card_data["ID"] = card_id

    if not os.path.isabs(filename):
        filename = os.path.join(BASE_DIR,filename)

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open (filename, "r", encoding="utf-8") as f:
            try:
                existing_cards = json.load(f)
            except json.JSONDecodeError:
                existing_cards = []
    else:
        existing_cards = []

    existing_cards.append(card_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_cards, f, ensure_ascii=False,indent=2)
        f.flush()
        os.fsync(f.fileno())
    print(f"Card succesfully saved to {filename}!")
    print(f"Saving to: {filename}")

def main():

    while True:

        print("\n=== Generator Random Cards ===")
        print("Choose Color Card:")
        print("1. Red (High Attack)")
        print("2. Blue (High Defense)")
        print("3. Green (Balance)")
        print("4. Purple (Tricky)")
        print("5. Black (High Risk)")
        print("6. Grey (Late Game)")
        print("0. Exit")
        
        your_color = input("Input Color (0-6): ")

        color = color_number.get(your_color)

        if your_color == "0":
            print("Thank you for using the card generator!")
            break

        if your_color not in color_number:
            print("Invalid selection. Please enter a number. 0-6.")
            continue
        
        print("\nChoose level card (1-4):")
        level = input("Input card level: ")
        
        if level not in ["1", "2", "3", "4"]:
            print("Level must be between 1-4. Please try again..")
            continue

        results = card_parameter(color,level)
        name = results[0]
        parameter = results[1]

        if results is None:
            print("Terjadi masalah.")
            continue

        if isinstance(results, str):
            print(results)
            continue

        # Card result
        print("\n=== Kartu yang Dihasilkan ===")
        #print (f"{name}, {parameter}")
        print(name)
        for item in parameter:
            for k, v in item.items():
                print(f"{k} : {v}")

        save = input("Do you want to save this card to a JSON file? (y/n): ")
        if save.lower() == "y":
            filename = input("Name JSON file(ex: my_card.json): ")
            if not filename.endswith(".json"):
                filename += ".json"
            print(f"Full fil path: {os.path.abspath(filename)}")
            # Combine card attributes into 1 dict (more suitable for JSON)
            card_dict = {}
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir,filename)
            for item in results:
                card_dict.update(item)
            export_to_json(card_dict,filename)
            print("Saving to:",os.path.abspath(filename))

if __name__ == "__main__":
    main()

    

    

