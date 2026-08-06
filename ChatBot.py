# =====================================================================
#  CBEMC-5 X40
#  Final Project - ArcherEats Chatbot
#  Members:
    # CHUNG, Josh Matthew A.
    # NOMOTO, Shintaroh
    # RICALDE, Jhobert Alfonso V.
    # VASCO, Victor Gerald N.
# =====================================================================


# shin is in night shift mode frr

import random
import nltk
from nltk.chat.util import Chat, reflections

# stolen i mean collected from the UH CAFEtEriA

FOOD_DATABASE = [
    {
        "name": "STEAMED RICE",
        "description": "",
        "price": 15,
        "kcal": 205,
        "allergens": [],
        "isAvailable": False, # also ginawa ko false toh coz lets assume bibili sila ng meal and gawin nalang parang add on yung rice 
        "isVegetarian": True
    },
    {
        "name": "ROAST PORK",
        "description": "Oven-roasted pork with savory drippings",
        "price": 95,
        "kcal": 217,
        "allergens": ["gluten", "celery", "mustard", "soybean", "sulphite"],
        "keywords": ["pork", "meat", "lunch", "roasted", "heavy"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "BREADED FISH FILLET",
        "description": "Crispy breaded fish fillet",
        "price": 90,
        "kcal": 235,
        "allergens": ["seafood", "egg", "gluten"],
        "keywords": ["fish", "lunch", "light"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "DAING NA BANGUS",
        "description": "Marinated milkfish fried to golden perfection",
        "price": 85,
        "kcal": 131,
        "allergens": ["soybean", "fish", "gluten", "seafood"],
        "keywords": ["fish", "lunch", "fried"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "BRAISED BEEF",
        "description": "Slow-braised beef in rich sauce",
        "price": 105,
        "kcal": 218,
        "allergens": ["soybean", "gluten", "sesame", "celery", "sulphite", "milk", "mustard"],
        "keywords": ["beef", "meat", "lunch", "heavy"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "FRIED EGG",
        "description": "",
        "price": 17,
        "kcal": 131,
        "allergens": ["egg"],
        "keywords": ["fried", "breakfast", "lunch", "light", "protein"],
        "isAvailable": True,
        "isVegetarian": True
    },
    {
        "name": "FRIED HUNGARIAN SAUSAGE",
        "description": "",
        "price": 75,
        "kcal": 100,
        "allergens": ["gluten", "soybean"],
        "keywords": ["fried", "breakfast"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "FRIED HOTDOG",
        "description": "",
        "price": 45,
        "kcal": 89,
        "allergens": ["soybean", "milk", "mustard", "gluten", "sulphite"],
        "keywords": ["fried", "breakfast"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "PORK BBQ",
        "description": "",
        "price": 100,
        "kcal": 195,
        "allergens": ["soybean", "mustard", "gluten", "sulphite"],
        "keywords": ["pork", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "PORK MENUDO",
        "description": "",
        "price": 85,
        "kcal": 209,
        "allergens": ["soybean", "milk", "crustaceans", "celery", "sulphite"],
        "keywords": ["pork", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "SINIGANG NA SALMON",
        "description": "",
        "price": 140,
        "kcal": 165,
        "allergens": ["gluten", "fish", "soybean", "crustacean", "celery", "egg", "milk", "seafood"],
        "keywords": ["fish", "soup", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "TOFU SISIG",
        "description": "",
        "price": 85,
        "kcal": 76,
        "allergens": ["soybean", "gluten", "milk", "celery"],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True
    },
    {
        "name": "FRIED CHICKEN",
        "description": "",
        "price": 95,
        "kcal": 256,
        "allergens": ["chicken", "egg", "gluten", "soybean"],
        "keywords": ["chicken", "meat", "fried", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "MONGGO WITH AMPALAYA LEAVES",
        "description": "",
        "price": 60,
        "kcal": 98,
        "allergens": ["gluten", "soybean", "milk", "crustaceans", "celery", "sulphite"],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True
    },
    {
        "name": "BEEF MONGOLIAN",
        "description": "",
        "price": 100,
        "kcal": 255,
        "allergens": ["chicken", "soybean"],
        "keywords": ["beef", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "CHICKEN NUGGETS",
        "description": "",
        "price": 75,
        "kcal": 240,
        "allergens": ["milk", "soybean", "wheat", "sulphite", "egg", "crustacean", "celery", "mustard"],
        "keywords": ["chicken", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "AMPALAYA W/ EGG",
        "description": "",
        "price": 60,
        "kcal": 104,
        "allergens": ["egg"],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True
    },
    {
        "name": "FRIED RICE",
        "description": "",
        "price": 25,
        "kcal": 202,
        "allergens": ["chicken", "milk", "soybean", "celery"],
        "keywords": ["breakfast"],
        "isAvailable": True,
        "isVegetarian": False
    },
    {
        "name": "CHAMPORADO",
        "description": "",
        "price": 50,
        "kcal": 280,
        "allergens": ["gluten", "nut"],
        "keywords": ["breakfast"],
        "isAvailable": True,
        "isVegetarian": True
    }
]

last_discussed_food = None
last_discussed_allergen = None
user_allergies = []
USER_ID_NUMBER = 12345678


# dummy dummy lang toh para pag nag order si user di naman sya una diba diba and para lang if madaming ginawang order si user nadagdag tlga para cool 

orders_queue = [
    {
        "id_number": 12411234,
        "food_name": "ROAST PORK",
        "count": 1,
        "with_rice": True,
        "order_number": 1,
    },
    {
        "id_number": 12422094,
        "food_name": "FRIED CHICKEN",
        "count": 2,
        "with_rice": False,
        "order_number": 2,
    },
    {
        "id_number": 11900000,
        "food_name": "TOFU SISIG",
        "count": 1,
        "with_rice": True,
        "order_number": 3,
    },
]

# function to make things maayos yung allergies

def normalize_allergen(allergen_str):
    allergen_map = {
        "eggs": "egg",
        "soy": "soybean",
        "dairy": "milk",
        "nuts": "nut",
        "seafoods": "seafood",
        "crustaceans": "crustacean",
    }
    cleaned = allergen_str.lower().strip()
    return allergen_map.get(cleaned, cleaned)

# we adding sa list of allergy ni user kasi we care we remember 

def register_user_allergy(allergen_type):
    global user_allergies, last_discussed_allergen
    target = normalize_allergen(allergen_type)
    if target not in user_allergies:
        user_allergies.append(target)
    last_discussed_allergen = target

    if len(user_allergies) == 1:
        allergies_str = user_allergies[0]
    else:
        allergies_str = (", ".join(user_allergies[:-1]) + " and " + user_allergies[-1])

    return f"Gotcha! You're allergic to {allergies_str}."

# this is the asking and the checking for allergies

def add_allergies(allergen_type=None):
    if allergen_type:
        return register_user_allergy(allergen_type)

    print("What are you allergic to? [give only 1|none if none]")
    user_input = input("> ").strip()

    if not user_input or user_input.lower() in [
        "none"
    ]:
        return "No problem! Let me know if you need any menu recommendations."

    parsed_intent = chatbot.respond(user_input)
    if parsed_intent and parsed_intent.strip().startswith("REGISTER_ALLERGY_"):
        allergen = parsed_intent.strip().replace("REGISTER_ALLERGY_", "")
    else:
        allergen = user_input.lower().strip()

    return register_user_allergy(allergen)

# show menu all available

def get_available_menu():
    available_items = [
        f"• {item['name']}"
        for item in FOOD_DATABASE
        if item.get("isAvailable")
    ]

    if not available_items:
        return "Sorry, no items are currently available on the menu."

    return (
        "Today's available menu:\n"
        + "\n".join(available_items)
        + "\nA cup of plain rice for an additional ₱15 [205 kcal]"
    )

# we checkin the keywords now

def get_meal_type_menu(meal_type):
    meal_type = meal_type.lower().strip()

    matched_items = [
        f"• {item['name']} (₱{item['price']})"
        for item in FOOD_DATABASE
        if item.get("isAvailable")
        and meal_type in [k.lower() for k in item.get("keywords", [])]
    ]

    if not matched_items:
        return f"Sorry, no available options found for {meal_type} right now."

    return (
        f"Here are today's available {meal_type.title()} options:\n"
        + "\n".join(matched_items)
    )

# yeahhh categories

def get_category_menu(category):
    category = category.lower().strip()
    matched_items = []

    for item in FOOD_DATABASE:
        if not item.get("isAvailable"):
            continue

        keywords = [k.lower() for k in item.get("keywords", [])]
        allergens = [a.lower() for a in item.get("allergens", [])]
        name = item["name"].lower()

        if category in ["pork"]:
            if "pork" in keywords or "pork" in name:
                matched_items.append(f"• {item['name']} (₱{item['price']})")

        elif category in ["beef"]:
            if "beef" in keywords or "beef" in name:
                matched_items.append(f"• {item['name']} (₱{item['price']})")

        elif category in ["chicken"]:
            if "chicken" in keywords or "chicken" in name:
                matched_items.append(f"• {item['name']} (₱{item['price']})")

        elif category in ["meat", "meats"]:
            if "meat" in keywords or any(
                m in name or m in keywords
                for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
            ):
                matched_items.append(f"• {item['name']} (₱{item['price']})")

        elif category in ["fish", "seafood"]:
            if (
                "fish" in keywords
                or "fish" in allergens
                or "seafood" in allergens
                or any(f in name for f in ["fish", "bangus", "salmon"])
            ):
                matched_items.append(f"• {item['name']} (₱{item['price']})")

        elif category in ["vegetable", "vegetables", "veggie", "veggies"]:
            if any(
                v in name for v in ["ampalaya", "monggo", "tofu"]
            ) or item.get("isVegetarian"):
                matched_items.append(f"• {item['name']} (₱{item['price']})")

    if not matched_items:
        return f"Sorry, no available options found for '{category}'."

    return f"Here are today's available {category} options:\n" + "\n".join(
        matched_items
    )

# this is when they say NO *keyword, basically opposite nung nauna

def get_category_removed_menu(category):
    category = category.lower().strip()
    matched_items = []

    for item in FOOD_DATABASE:
        if not item.get("isAvailable"):
            continue

        keywords = [k.lower() for k in item.get("keywords", [])]
        allergens = [a.lower() for a in item.get("allergens", [])]
        name = item["name"].lower()

        is_excluded = False

        if category in ["pork"]:
            if "pork" in keywords or "pork" in name:
                is_excluded = True

        elif category in ["beef"]:
            if "beef" in keywords or "beef" in name:
                is_excluded = True

        elif category in ["chicken"]:
            if "chicken" in keywords or "chicken" in name:
                is_excluded = True

        elif category in ["meat", "meats"]:
            if "meat" in keywords or any(
                m in name or m in keywords
                for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
            ):
                is_excluded = True

        elif category in ["fish", "seafood"]:
            if (
                "fish" in keywords
                or "fish" in allergens
                or "seafood" in allergens
                or any(f in name for f in ["fish", "bangus", "salmon"])
            ):
                is_excluded = True

        elif category in ["vegetable", "vegetables", "veggie", "veggies"]:
            if any(
                v in name for v in ["ampalaya", "monggo", "tofu"]
            ) or item.get("isVegetarian"):
                is_excluded = True

        if not is_excluded:
            matched_items.append(f"• {item['name']} (₱{item['price']})")

    if not matched_items:
        return f"Sorry, no available options found after excluding '{category}'."

    return (
        f"Here are today's available options without {category}:\n"
        + "\n".join(matched_items)
    )

# with allergen

def get_food_with_allergen(allergen_type):
    target = normalize_allergen(allergen_type)
    matched_items = []

    for item in FOOD_DATABASE:
        if not item.get("isAvailable"):
            continue
        
        item_allergens = [a.lower() for a in item.get("allergens", [])]
        
        # Check if the target allergen is in the item's allergen list
        if target in item_allergens:
            matched_items.append(f"• {item['name']} (₱{item['price']})")

    if not matched_items:
        return f"Sorry, we don't have any available menu items containing '{allergen_type}'."

    return f"Here are the available menu items containing {allergen_type}:\n" + "\n".join(matched_items)

# from all the evil that surrounds me defend me

def get_allergen_safe_menu(allergen_type=None):
    global user_allergies

    if allergen_type:
        target = normalize_allergen(allergen_type)
        if target not in user_allergies:
            user_allergies.append(target)

    if not user_allergies:
        return get_available_menu()

    safe_items = []
    for item in FOOD_DATABASE:
        if not item.get("isAvailable"):
            continue

        item_allergens = [a.lower() for a in item["allergens"]]
        is_safe = not any(
            user_allergy in item_allergens for user_allergy in user_allergies
        )

        if is_safe:
            safe_items.append(f"• {item['name']}")

    allergies_label = ", ".join(user_allergies)
    if not safe_items:
        return f"Sorry, we don't have any available items free from '{allergies_label}' today."

    return (
        f"Here are today's available items safe for {allergies_label} allergy:\n"
        + "\n".join(safe_items)
    )

# this could just be category pero nauna na toh iimplement so lets just keep this instead of changing the whole database

def get_vegetarian_menu():
    veg_items = [
        f"• {item['name']} (₱{item['price']})"
        for item in FOOD_DATABASE
        if item.get("isAvailable") and item.get("isVegetarian", False)
    ]

    if not veg_items:
        return "Sorry, we don't have any vegetarian options currently available on the menu."

    return "Here are today's available vegetarian-friendly options:\n" + "\n".join(
        veg_items
    )

# suggestion ! ! ! ! coolest part imo

def get_food_suggestion(criteria_type, value=None):
    available = [
        item for item in FOOD_DATABASE if item.get("isAvailable")
    ]

    if not available:
        return "Sorry, there are no items currently available on the menu."

    filtered = []

    if criteria_type == "budget" and value:
        limit = float(value)
        filtered = [item for item in available if item["price"] <= limit]
        if not filtered:
            return f"Sorry, we don't have any available items within a ₱{int(limit)} budget."

    elif criteria_type == "high_cal":
        filtered = [item for item in available if item["kcal"] >= 200]
        if not filtered:
            return "Sorry, no high-calorie options are available right now."

    elif criteria_type == "low_cal":
        filtered = [item for item in available if item["kcal"] < 200]
        if not filtered:
            return "Sorry, no low-calorie options are available right now."

    elif criteria_type == "cheapest":
        chosen = min(available, key=lambda x: x["price"])
        return (
        f"I recommend {chosen['name']}. "
        f"It's our cheapest available meal at ₱{chosen['price']}. "
        f"It has {chosen['kcal']} kcal."
    )

    elif criteria_type == "lowest_cal":
        chosen = min(available, key=lambda x: x["kcal"])
        return (
        f"I recommend {chosen['name']}. "
        f"It has only {chosen['kcal']} kcal."
    )

    elif criteria_type == "filling":
        chosen = max(available, key=lambda x: x["kcal"])
        return (
        f"If you're really hungry, try {chosen['name']}. "
        f"It has {chosen['kcal']} kcal."
    )
    
    elif criteria_type == "vegetarian":
        filtered = [
        item for item in available
        if item["isVegetarian"]
    ]

        if not filtered:
            return "Sorry, no vegetarian meals are available."

        chosen = random.choice(filtered)

        return (
            f"I recommend {chosen['name']}. "
            f"It costs ₱{chosen['price']} and has {chosen['kcal']} kcal."
    )

    elif criteria_type == "category" and value:
        target_cat = value.lower().strip()
        for item in available:
            keywords = [k.lower() for k in item.get("keywords", [])]
            name = item["name"].lower()
            allergens = [a.lower() for a in item.get("allergens", [])]

            if target_cat in ["pork"] and ("pork" in keywords or "pork" in name):
                filtered.append(item)
            elif target_cat in ["beef"] and ("beef" in keywords or "beef" in name):
                filtered.append(item)
            elif target_cat in ["chicken"] and ("chicken" in keywords or "chicken" in name):
                filtered.append(item)
            elif target_cat in ["meat", "meats"] and ("meat" in keywords or any(m in name or m in keywords for m in ["pork", "beef", "chicken", "sausage", "hotdog"])):
                filtered.append(item)
            elif target_cat in ["fish", "seafood"] and ("fish" in keywords or "fish" in allergens or "seafood" in allergens or any(f in name for f in ["fish", "bangus", "salmon"])):
                filtered.append(item)
            elif target_cat in ["vegetable", "veggie"] and (any(v in name for v in ["ampalaya", "monggo", "tofu"]) or item.get("isVegetarian")):
                filtered.append(item)

    elif criteria_type == "allergen" and value:
        allergen_type = value.lower().strip()
        allergen_map = {"eggs": "egg", "soy": "soybean", "dairy": "milk"}
        target_allergen = allergen_map.get(allergen_type, allergen_type)

        filtered = [
            item
            for item in available
            if target_allergen not in [a.lower() for a in item["allergens"]]
        ]
        if not filtered:
            return f"Sorry, no available options are safe for a '{target_allergen}' allergy."

    else:
        filtered = available

    chosen = random.choice(filtered)
    return f"How about {chosen['name']}? It costs ₱{chosen['price']} and contains {chosen['kcal']} kcal."

# basically more info on da food

def get_food_description(food_name):
    global last_discussed_food
    if food_name.lower().strip() in ["it"]:
        if not last_discussed_food:
            return "What food are you referring to?"
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()

    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            last_discussed_food = item["name"]
            desc = item.get("description")
            if desc:
                return f"{item['name']} - {desc}"
            else:
                return f"{item['name']} is on our menu, but has no detailed description."

    return f"Sorry, I couldn't find '{food_name.title()}' on our menu."

# get price 

def get_food_price(food_name):
    global last_discussed_food
    if food_name.lower().strip() in ["it"]:
        if not last_discussed_food:
            return "Which dish are you asking the price for?"
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()

    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            last_discussed_food = item["name"]
            return f"{item['name']} costs ₱{item['price']} alone and ₱{item['price']+15} with white rice."

    return f"Sorry, I couldn't find '{food_name.title()}' on our menu."

# get calories kcalories kcal

def get_food_calories(food_name):
    global last_discussed_food

    if food_name.lower().strip() in ["it"]:
        if not last_discussed_food:
            return "Which dish are you asking the calorie count for?"
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()

    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            last_discussed_food = item["name"]
            return f"{item['name']} has {item['kcal']} kcal."

    return f"Sorry, I couldn't find '{food_name.title()}' on our menu."

# if user asking if certain menu item has this allergen

def check_item_allergen(food_name, allergen_type):
    global last_discussed_food, last_discussed_allergen

    if food_name.lower().strip() in ["it"]:
        if not last_discussed_food:
            return "Which food item are you referring to?"
        food_name = last_discussed_food

    if allergen_type.lower().strip() in ["it", "that"]:
        if not last_discussed_allergen:
            return "Which allergen are you asking about?"
        allergen_type = last_discussed_allergen

    food_name_clean = food_name.strip().upper()
    allergen_type_clean = allergen_type.lower().strip()

    allergen_map = {
        "eggs": "egg",
        "soy": "soybean",
        "dairy": "milk",
        "nuts": "nut",
    }
    target_allergen = allergen_map.get(
        allergen_type_clean, allergen_type_clean
    )

    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            last_discussed_food = item["name"]
            last_discussed_allergen = target_allergen

            item_allergens = [a.lower() for a in item["allergens"]]

            if target_allergen in item_allergens:
                return f"Yes, {item['name']} contains **{target_allergen}**. (Listed allergens: {', '.join(item['allergens'])})"
            else:
                if item["allergens"]:
                    return f"No, {item['name']} does NOT contain {target_allergen}. (Listed allergens: {', '.join(item['allergens'])})"
                else:
                    return f"No, {item['name']} has no declared allergens."

    return f"Sorry, I couldn't find '{food_name.title()}' on our menu."

# making order 

def process_order_creation(count_str, food_query):
    global orders_queue, last_discussed_food

    try:
        count = int(count_str)
        if count <= 0:
            return "Order quantity must be at least 1."
    except ValueError:
        return "Invalid order quantity."

    food_query_clean = food_query.strip().upper()
    selected_item = None

    for item in FOOD_DATABASE:
        if food_query_clean in item["name"].upper():
            selected_item = item
            break

    if not selected_item:
        return f"Sorry, we couldn't find '{food_query.title()}' on our menu."

    if not selected_item.get("isAvailable"):
        return (
            f"Sorry, {selected_item['name']} is currently not available."
        )

    last_discussed_food = selected_item["name"]

    print(
        f"Would you like to add rice to your {count}x {selected_item['name']} for an additional ₱15 per item? [y/n]"
    )

    with_rice = False
    while True:
        rice_choice = input("> ").strip().lower()
        if rice_choice in ["y", "yes"]:
            with_rice = True
            break
        elif rice_choice in ["n", "no"]:
            with_rice = False
            break
        else:
            print("Please answer with 'y' or 'n'.")

    unit_price = selected_item["price"] + (15 if with_rice else 0)
    total_price = unit_price * count
    # we can change the format of this para mas bagay sa chatbot but thats basically what we need
    rice_str = "with rice" if with_rice else "without rice"
    print("\n--- ORDER SUMMARY ---")
    print(f"ID Number : {USER_ID_NUMBER}")
    print(f"Item      : {count}x {selected_item['name']} ({rice_str})")
    print(f"Unit Price: ₱{unit_price}")
    print(f"Total     : ₱{total_price}")
    print("---------------------")
    print("Type CONFIRM to place your order or CANCEL to abort.")

    while True:
        action = input("> ").strip().upper()
        if action == "CONFIRM":
            order_num = len(orders_queue) + 1
            new_order = {
                "id_number": USER_ID_NUMBER,
                "food_name": selected_item["name"],
                "count": count,
                "with_rice": with_rice,
                "order_number": order_num,
            }
            orders_queue.append(new_order)
            return (
                f"Order confirmed! Your order number is #{order_num}. "
                f"You are number {order_num} in queue."
            )
        elif action == "CANCEL":
            return "Order process canceled."
        else:
            print("Please type CONFIRM or CANCEL.")

# regex

pairs = [
    # eto dapat sa taas para di magconflict sa iba

    # dis is creating order na ilalagay sa napakacool na dummy queue YIPEE

    [
        r"^\s*(\d+)\s*,\s*(.+)\s*$",
        ["CREATE_ORDER_%1|%2"],
    ],
    [
        r"^\s*(\d+)\s+(.+)\s*$",
        ["CREATE_ORDER_%1|%2"],
    ],

    # recommendation tong mga sunod

    [
    r".*\b(suggest|recommend|pick|want)\b.*\b(pork|beef|chicken|meat|meats|fish|seafood|veggie|vegetable)\b.*",
    ["SUGGEST_CATEGORY_%2"],
],

    # recommend for brokies

    [
        r".*\b(suggest|recommend|what can i get|food|lunch|dinner|breakfast)\b.*\b(\d+)\b\s*(peso|pesos|php|p|budget|).*",
        ["SUGGEST_BUDGET_%2"],
    ],

    # high cal 

    [
        r".*\b(suggest|recommend|what can i get|want|food)\b.*\b(high cal|high calorie|heavy|bulk|cheat meal)\b.*",
        ["SUGGEST_HIGHCAL"],
    ],

    # low cal

    [
        r".*\b(suggest|recommend|what can i get|want|food)\b.*\b(low cal|low calorie|light|diet|healthy)\b.*",
        ["SUGGEST_LOWCAL"],
    ],

    # just indecisive

    [
        r".*\b(suggest|recommend|what should i eat|pick for me)\b.*",
        ["SUGGEST_GENERAL"],
    ],

    # may allergy

    [
        r".*\b(suggest|recommend|what can i eat|what should i eat|food|lunch|dinner)\b.*\b(allergic to|allergy|allergies|no|without|free from)\s+(to\s+|)\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nuts)\b.*",
        ["SUGGEST_ALLERGEN_%4"],
    ],
    [
        r".*\b(suggest|recommend|what can i eat|what should i eat|food|lunch|dinner)\b.*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nuts)\s+(free|allergy|allergies)\b.*",
        ["SUGGEST_ALLERGEN_%2"],
    ],

    # herbivore 

    [
        r".*\b(vegetarian|veggie|meatless|no meat|plant based|vegetables)\b.*",
        ["FETCH_VEGETARIAN"],
    ],

    # Suggestion Cheapest

    [
    r".*\b(cheapest|lowest price|least expensive|budget meal|cheapest meal)\b.*",
    ["SUGGEST_CHEAPEST"],
    ],

    # Suggestion Lowest Calories

    [
    r".*\b(lowest calories|lowest calorie|healthiest|lightest|lowest kcal)\b.*",
    ["SUGGEST_LOWESTCAL"],
    ],

    #Suggestion Most Filling

    [
    r".*\b(most filling|heaviest|largest meal|full meal|very hungry)\b.*",
    ["SUGGEST_FILLING"],
    ],

    #Suggestion Vegetarian
    [
    r".*\b(recommend|suggest|pick)\b.*\b(vegetarian|veggie|vegetarian meal)\b.*",
    ["SUGGEST_VEGETARIAN"],
    ],

     # without meats

    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero)\b.*\b(pork)\b.*", 
        ["WITHOUT_pork"]
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero)\b.*\b(beef)\b.*",
        ["WITHOUT_beef"]
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero)\b.*\b(chicken)\b.*",
        ["WITHOUT_chicken"],
    ],

    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero)\b.*\b(fish|seafood|seafoods)\b.*",
        ["WITHOUT_fish"],
    ],

    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero)\b.*\b(meat|meats)\b.*",
        ["WITHOUT_meat"]
    ],

    # without allergens

    [
        r".*\b(allergic to|allergy|allergies|no|without|free from|exclude|minus|skip|remove)\s+(to\s+|)\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|wheat|chicken)\b.*",
        ["ALLERGEN_%3"],
    ],
    [
        r".*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|wheat|chicken)\s+(free|allergy|allergies|intolerant)\b.*",
        ["ALLERGEN_%1"],
    ],

    # Catches general requests like "food with egg" or "dish with shrimp"
    [
        r".*\b(food|dish|meal|what)\b.*\b(with|contains|has)\b.*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*",
        ["FOOD_WITH_ALLERGEN_%3"],
    ],
    # Catches direct questions like "show me food with dairy"
    [
        r".*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*\b(food|dish|meal)\b.*",
        ["FOOD_WITH_ALLERGEN_%1"],
    ],

    # with meat

    [
        r".*\b(pork)\b.*",
        ["CATEGORY_pork"]
    ],
    [
        r".*\b(beef)\b.*",
        ["CATEGORY_beef"]
    ],
    [
        r".*\b(chicken)\b.*",
        ["CATEGORY_chicken"]
    ],
    [
        r".*\b(meat|meats)\b.*",
        ["CATEGORY_meat"]
    ],
    [
        r".*\b(fish|seafood|seafoods)\b.*",
        ["CATEGORY_fish"]
    ],
    [
        r".*\b(vegetable|vegetables|veggie|veggies)\b.*",
        ["CATEGORY_vegetable"]
    ],

    # honestly why not nasa activity ko naman toh -shin
    
    [
        r".*\b(breakfast)\b.*",
        ["MEAL_breakfast"]
    ],
    [
        r".*\b(lunch)\b.*",
        ["MEAL_lunch"]
    ],

    # this saying hab allergy so the chatbot is like oh no what ur allergy tapos the chatbot will remember kasi hes nice and sweet
    
    [
        r".*(allerg).*",
        ["IDENTIFY_ALLERGY"]
    ],

    # just regular menu

    [
        r"(.*\b|)(menu|available|food|dishes|whats on|what is on)\b.*",
        ["FETCH_MENU"],
    ],

    # asking for stuff about certain food
    
    [
        r".*\b(what is|what\'s|tell me about|describe|info on|details for)\s+(.+)\b\s*$",
        ["INFO_%2"],
    ],

    # specific allergen question 

    [
        r".*\b(does|is|has)\s+(.+)\b\s+(contain|have|has|got|with)\s+(any\s+|)(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*",
        ["CHECK_ALLERGEN_%2|%5"],
    ],

    [
        r".*\b(is there|are there)\s+(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\s+(in|inside|on)\s+(.+)\b.*",
        ["CHECK_ALLERGEN_%4|%2"],
    ],

    # price checker

    [
        r".*\b(how much is|price of|how much for|cost of|how much)\s+(.+)\b.*",
        ["PRICE_%2"],
    ],
    [
        r".*\b(how much is it|how much does it cost|what is the price|price|how much)\b.*",
        ["PRICE_it"],
    ],

    # calorie checker

    [
        r".*\b(how many calories|calorie count|kcal|calories)\s+(are\s+|)(in|of|for)\s+(.+)\b.*",
        ["CALORIES_%4"],
    ],
    [
        r".*\b(how many calories does it have|how many calories in it|how many calories is it|calories in it|kcal count|how many calories|calories)\b.*",
        ["CALORIES_it"],
    ],

    # oh cool

    [
        r".*\b(combo|combos|rice meal|with rice|extra rice|add rice|rice combo)\b.*",
        [
            "All main dishes can be ordered ala carte or made into a meal by adding white rice for an extra ₱15 (205 kcal)!"
        ],
    ],

    # ordering, claiming, or not claiming kung gusto mong mapunta sdfo
    
    [
        r"(.*)(order)(.*)",
        [
            "To order, please head to the lower left corner and select your meal from there! I could also order for you! Just say what you want to order and I'll do it for you (e.g., '1, Roast Pork')"
        ],
    ],

    [
        r"(.*)(where)(.*)\b(claim|receive|take|get|grab)\b(.*)",
        [
            "You can claim your food in the UH Cafeteria once it has been prepared. You will receive a notification once your meal is ready."
        ],
    ],

    [
        r"(.*)\b(forgot|didnt|did not|not|no|didn\'t|cant|can\'t|would not|wont|won\'t)\b(.*)\b(claim)\b(.*)",
        [
            "Every order is tied to your ID number. If you did not take your food, repeating offence will result in disciplinary action."
        ],
    ],

    [
        r"(.*)(claim)(.*)",
        [
            "To claim your food, your order number will be called, and a notification will be sent to your device! Just head to the claiming area to receive your meal."
        ],
    ],

    # assistance - victor's activity 4 basically

    [
        r"(hi|hello|hey|good (morning|afternoon|evening))",
        [
            "Hello! Welcome to ArcherEats support. How can I help you today?",
            "Hi there! Need help with anything?",
        ],
    ],

    [
        r"(.*)(create|register|sign up|open|make)(.*)(account|profile)(.*)",
        [
            "Hit the sign up button and enter your ID number and make a password!"
        ],
    ],

    [
        r"(.*)(cannot|can\'t|unable to)(.*)(login|log in|sign in)(.*)",
        [
            "Please double-check your ID number and password. If the issue persists, try resetting your password."
        ],
    ],

    [
        r"(.*)(forgot|reset)(.*)(password)(.*)",
        [
            'You can reset your ArcherEats password by clicking "Forgot Password" on the login screen.'
        ],
    ],

    [
        r"(.*)(update|change|edit)(.*)(account|profile|details)(.*)",
        [
            "You can update your ArcherEats profile in the Account Settings section of the app."
        ],
    ],

    [
        r"(.*)(payment methods|how do i pay|payment options|pay)(.*)",
        ["ArcherEats accepts cash and GCash once you have ordered."],
    ],

    [
        r"(.*)(payment failed|failed payment|transaction failed|error payment)(.*)",
        [
            "Your payment may have failed due to insufficient funds or network issues. Please try again or use another method."
        ],
    ],

    [
        r"(.*)(refund|money back|return payment)(.*)",
        [
            "Refund requests in ArcherEats are processed within 3–5 business days after approval."
        ],
    ],

    [
        r"(.*)(not|didn\'t)(.*)(receive|get)(.*)(confirmation|receipt)(.*)",
        [
            "Please check your email or order history. If missing, contact support with your order ID."
        ],
    ],

    [
        r"(.*)(error|bug|issue|problem)(.*)(app|system|website|ArcherEats)(.*)",
        [
            "We’re sorry for the inconvenience. Please restart the app or try again later."
        ],
    ],

    [
        r"(.*)(app|system|website)(.*)(not working|down|crashed|slow)(.*)",
        [
            "Try restarting ArcherEats or checking your internet connection. If it continues, contact support."
        ],
    ],

    [
        r"(.*)(charged|double charge|overcharged)(.*)",
        [
            "If you were overcharged, please report the issue with your receipt so we can investigate."
        ],
    ],

    [
        r"(help|support|assist|customer service)",
        [
            "I can help you with ArcherEats accounts, payments, refunds, and system issues."
        ],
    ],

    [
        r".*\b(hours|open|close|operating hours|schedule|where are you|location|where to pick up|pick up location|where)\b.*",
        [
            "UH Cafeteria operates Monday to Saturday from 7:00 AM to 6:00 PM at the UH Dining Area."
        ],
    ],

    [
        r"(bye|goodbye|exit|quit)",
        [
            "Thank you for using ArcherEats support. Have a great day!",
            "Goodbye! Your ArcherEats support assistant is always here to help.",
        ],
    ],
    [r"(.*)(thank|thanks)(.*)", ["You're welcome! Enjoy your meal!"]],
]

chatbot = Chat(pairs, reflections)

'''
print("Hi, I'm ArcherEats. How can I help you?")

while True:
    try:
        user_input = input("> ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Thank you for using ArcherEats Chatbot!")
            break

        if not user_input:
            continue

        response = chatbot.respond(user_input)

        if response:
            clean_response = response.strip()

            if clean_response == "FETCH_MENU":
                print(get_available_menu())

            elif clean_response == "FETCH_VEGETARIAN":
                print(get_vegetarian_menu())

            elif clean_response.startswith("CATEGORY_"):
                category = clean_response.replace("CATEGORY_", "")
                print(get_category_menu(category))

            elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
                allergen = clean_response.replace("FOOD_WITH_ALLERGEN_", "")
                print(get_food_with_allergen(allergen))

            elif clean_response.startswith("WITHOUT_"):
                category = clean_response.replace("WITHOUT_", "")
                print(get_category_removed_menu(category))

            elif clean_response.startswith("SUGGEST_CATEGORY_"):
                category = clean_response.replace("SUGGEST_CATEGORY_", "")
                print(get_food_suggestion("category", category))

            elif clean_response.startswith("ALLERGEN_"):
                allergen = clean_response.replace("ALLERGEN_", "")
                print(get_allergen_safe_menu(allergen))

            elif clean_response.startswith("SUGGEST_BUDGET_"):
                amount = clean_response.replace("SUGGEST_BUDGET_", "")
                print(get_food_suggestion("budget", amount))

            elif clean_response == "SUGGEST_HIGHCAL":
                print(get_food_suggestion("high_cal"))

            elif clean_response == "SUGGEST_LOWCAL":
                print(get_food_suggestion("low_cal"))

            elif clean_response == "SUGGEST_GENERAL":
                print(get_food_suggestion("general"))

            elif clean_response.startswith("SUGGEST_ALLERGEN_"):
                allergen = clean_response.replace("SUGGEST_ALLERGEN_", "")
                print(get_food_suggestion("allergen", allergen))

            elif clean_response == "SUGGEST_CHEAPEST":
                print(get_food_suggestion("cheapest"))

            elif clean_response == "SUGGEST_LOWESTCAL":
                print(get_food_suggestion("lowest_cal"))

            elif clean_response == "SUGGEST_FILLING":
                print(get_food_suggestion("filling"))

            elif clean_response == "SUGGEST_VEGETARIAN":
                print(get_food_suggestion("vegetarian"))

            elif clean_response.startswith("INFO_"):
                food = clean_response.replace("INFO_", "")
                print(get_food_description(food))

            elif clean_response.startswith("PRICE_"):
                food = clean_response.replace("PRICE_", "")
                print(get_food_price(food))

            elif clean_response.startswith("CALORIES_"):
                food = clean_response.replace("CALORIES_", "")
                print(get_food_calories(food))

            elif clean_response.startswith("CHECK_ALLERGEN_"):
                payload = clean_response.replace("CHECK_ALLERGEN_", "")
                if "|" in payload:
                    food_item, allergen = payload.split("|", 1)
                    print(check_item_allergen(food_item, allergen))
                else:
                    print("Could not process allergen check query.")

            elif clean_response.startswith("MEAL_"):
                meal = clean_response.replace("MEAL_", "")
                print(get_meal_type_menu(meal))

            elif clean_response.startswith("CREATE_ORDER_"):
                payload = clean_response.replace("CREATE_ORDER_", "")
                if "|" in payload:
                    count_str, food_query = payload.split("|", 1)
                    print(process_order_creation(count_str, food_query))

            elif clean_response == "IDENTIFY_ALLERGY":
                response_msg = add_allergies()
                print(response_msg)

                if "Gotcha!" in response_msg:
                    print(get_allergen_safe_menu())
            else:
                print(response)
        else:
            print(
                "I understand the general topic, but could you please rephrase your request?"
            )

    except (KeyboardInterrupt, EOFError, SystemExit):
        break '''
