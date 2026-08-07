# =====================================================================
#  CBEMC-5 X40
#  Final Project - ArcherEats Chatbot
#  Members:
#    - CHUNG, Josh Matthew A.
#    - NOMOTO, Shintaroh
#    - RICALDE, Jhobert Alfonso V.
#    - VASCO, Victor Gerald N.
# =====================================================================

import random
import nltk
from nltk.chat.util import Chat, reflections

FOOD_DATABASE = [
    {
        "name": "STEAMED RICE",
        "description": "Steamed white rice, cooked fluffy and soft.",
        "price": 15,
        "kcal": 205,
        "allergens": [],
        "keywords": ["rice", "carbs", "side", "staple"],
        "isAvailable": False,
        "isVegetarian": True,
    },
    {
        "name": "ROAST PORK",
        "description": "Oven-roasted pork with savory drippings.",
        "price": 95,
        "kcal": 217,
        "allergens": ["gluten", "celery", "mustard", "soybean", "sulphite"],
        "keywords": ["pork", "meat", "lunch", "roasted", "heavy"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "BREADED FISH FILLET",
        "description": "Crispy breaded fish fillet.",
        "price": 90,
        "kcal": 235,
        "allergens": ["seafood", "egg", "gluten"],
        "keywords": ["fish", "lunch", "light"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "DAING NA BANGUS",
        "description": "Marinated milkfish fried to golden perfection.",
        "price": 85,
        "kcal": 131,
        "allergens": ["soybean", "fish", "gluten", "seafood"],
        "keywords": ["fish", "lunch", "fried"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "BRAISED BEEF",
        "description": "Slow-braised beef in rich sauce.",
        "price": 105,
        "kcal": 218,
        "allergens": [
            "soybean",
            "gluten",
            "sesame",
            "celery",
            "sulphite",
            "milk",
            "mustard",
        ],
        "keywords": ["beef", "meat", "lunch", "heavy"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "FRIED EGG",
        "description": "Freshly fried egg with a cooked yolk.",
        "price": 17,
        "kcal": 131,
        "allergens": ["egg"],
        "keywords": ["fried", "breakfast", "lunch", "light", "protein"],
        "isAvailable": True,
        "isVegetarian": True,
    },
    {
        "name": "FRIED HUNGARIAN SAUSAGE",
        "description": "Pan-fried Hungarian sausage.",
        "price": 75,
        "kcal": 100,
        "allergens": ["gluten", "soybean"],
        "keywords": ["fried", "breakfast"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "FRIED HOTDOG",
        "description": "Pan-fried hotdog.",
        "price": 45,
        "kcal": 89,
        "allergens": ["soybean", "milk", "mustard", "gluten", "sulphite"],
        "keywords": ["fried", "breakfast"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "PORK BBQ",
        "description": "Grilled pork on a stick with a barbecue glaze.",
        "price": 100,
        "kcal": 195,
        "allergens": ["soybean", "mustard", "gluten", "sulphite"],
        "keywords": ["pork", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "PORK MENUDO",
        "description": "Pork cooked in tomato sauce with potatoes and carrots.",
        "price": 85,
        "kcal": 209,
        "allergens": ["soybean", "milk", "crustaceans", "celery", "sulphite"],
        "keywords": ["pork", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "SINIGANG NA SALMON",
        "description": "Salmon in a sour tamarind soup with vegetables.",
        "price": 140,
        "kcal": 165,
        "allergens": [
            "gluten",
            "fish",
            "soybean",
            "crustacean",
            "celery",
            "egg",
            "milk",
            "seafood",
        ],
        "keywords": ["fish", "soup", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "TOFU SISIG",
        "description": "Fried tofu mixed with onions and sisig seasoning.",
        "price": 85,
        "kcal": 76,
        "allergens": ["soybean", "gluten", "milk", "celery"],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True,
    },
    {
        "name": "FRIED CHICKEN",
        "description": "Crispy fried chicken.",
        "price": 95,
        "kcal": 256,
        "allergens": ["chicken", "egg", "gluten", "soybean"],
        "keywords": ["chicken", "meat", "fried", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "MONGGO WITH AMPALAYA LEAVES",
        "description": "Monggo bean stew with ampalaya leaves.",
        "price": 60,
        "kcal": 98,
        "allergens": [
            "gluten",
            "soybean",
            "milk",
            "crustaceans",
            "celery",
            "sulphite",
        ],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True,
    },
    {
        "name": "BEEF MONGOLIAN",
        "description": "Beef strips cooked in a savory soy-based sauce.",
        "price": 100,
        "kcal": 255,
        "allergens": ["chicken", "soybean"],
        "keywords": ["beef", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "CHICKEN NUGGETS",
        "description": "Crispy chicken nuggets.",
        "price": 75,
        "kcal": 240,
        "allergens": [
            "milk",
            "soybean",
            "wheat",
            "sulphite",
            "egg",
            "crustacean",
            "celery",
            "mustard",
        ],
        "keywords": ["chicken", "meat", "lunch"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "AMPALAYA W/ EGG",
        "description": "Sauteed ampalaya with scrambled egg.",
        "price": 60,
        "kcal": 104,
        "allergens": ["egg"],
        "keywords": ["lunch"],
        "isAvailable": True,
        "isVegetarian": True,
    },
    {
        "name": "FRIED RICE",
        "description": "Fried rice with garlic.",
        "price": 25,
        "kcal": 202,
        "allergens": ["chicken", "milk", "soybean", "celery"],
        "keywords": ["breakfast"],
        "isAvailable": True,
        "isVegetarian": False,
    },
    {
        "name": "CHAMPORADO",
        "description": "Sweet chocolate rice porridge.",
        "price": 50,
        "kcal": 280,
        "allergens": ["gluten", "nut"],
        "keywords": ["breakfast"],
        "isAvailable": True,
        "isVegetarian": True,
    },
]

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

def register_user_allergy(allergen_type, user_allergies=None):
    if user_allergies is None:
        user_allergies = []

    target = normalize_allergen(allergen_type)
    if target not in user_allergies:
        user_allergies.append(target)

    if len(user_allergies) == 1:
        allergies_str = user_allergies[0]
    else:
        allergies_str = (
            ", ".join(user_allergies[:-1]) + " and " + user_allergies[-1]
        )

    return f"Gotcha! You're allergic to {allergies_str}.", user_allergies

# this is the asking and the checking for allergies

def add_allergies(allergen_type=None, user_allergies=None):
    if user_allergies is None:
        user_allergies = []

    if allergen_type:
        return register_user_allergy(allergen_type, user_allergies)

    print("What are you allergic to? [give only 1|none if none]")
    user_input = input("> ").strip()

    if not user_input or user_input.lower() in ["none"]:
        return (
            "No problem! Let me know if you need any menu recommendations.",
            user_allergies,
        )

    parsed_intent = chatbot.respond(user_input)
    if parsed_intent and parsed_intent.strip().startswith("REGISTER_ALLERGY_"):
        allergen = parsed_intent.strip().replace("REGISTER_ALLERGY_", "")
    else:
        allergen = user_input.lower().strip()

    return register_user_allergy(allergen, user_allergies)

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
        + "\nAdd-on a cup of plain rice for only ₱15 [205 kcal]"
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

        if category == "pork" and ("pork" in keywords or "pork" in name):
            matched_items.append(f"• {item['name']} (₱{item['price']})")
        elif category == "beef" and ("beef" in keywords or "beef" in name):
            matched_items.append(f"• {item['name']} (₱{item['price']})")
        elif category == "chicken" and (
            "chicken" in keywords or "chicken" in name
        ):
            matched_items.append(f"• {item['name']} (₱{item['price']})")
        elif category in ["meat", "meats"] and (
            "meat" in keywords
            or any(
                m in name or m in keywords
                for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
            )
        ):
            matched_items.append(f"• {item['name']} (₱{item['price']})")
        elif category in ["fish", "seafood"] and (
            "fish" in keywords
            or "fish" in allergens
            or "seafood" in allergens
            or any(f in name for f in ["fish", "bangus", "salmon"])
        ):
            matched_items.append(f"• {item['name']} (₱{item['price']})")
        elif category in ["vegetable", "vegetables", "veggie", "veggies"] and (
            any(v in name for v in ["ampalaya", "monggo", "tofu"])
            or item.get("isVegetarian")
        ):
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

        if category == "pork" and ("pork" in keywords or "pork" in name):
            is_excluded = True
        elif category == "beef" and ("beef" in keywords or "beef" in name):
            is_excluded = True
        elif category == "chicken" and (
            "chicken" in keywords or "chicken" in name
        ):
            is_excluded = True
        elif category in ["meat", "meats"] and (
            "meat" in keywords
            or any(
                m in name or m in keywords
                for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
            )
        ):
            is_excluded = True
        elif category in ["fish", "seafood"] and (
            "fish" in keywords
            or "fish" in allergens
            or "seafood" in allergens
            or any(f in name for f in ["fish", "bangus", "salmon"])
        ):
            is_excluded = True
        elif category in ["vegetable", "vegetables", "veggie", "veggies"] and (
            any(v in name for v in ["ampalaya", "monggo", "tofu"])
            or item.get("isVegetarian")
        ):
            is_excluded = True

        if not is_excluded:
            matched_items.append(f"• {item['name']} (₱{item['price']})")

    if not matched_items:
        return (
            f"Sorry, no available options found after excluding '{category}'."
        )
    return (
        f"Here are today's available options without {category}:\n"
        + "\n".join(matched_items)
    )

# with allergen

def get_food_with_allergen(allergen_type):
    target = normalize_allergen(allergen_type)
    matched_items = [
        f"• {item['name']} (₱{item['price']})"
        for item in FOOD_DATABASE
        if item.get("isAvailable")
        and target in [a.lower() for a in item.get("allergens", [])]
    ]
    if not matched_items:
        return f"Sorry, we don't have any available menu items containing '{allergen_type}'."
    return (
        f"Here are the available menu items containing {allergen_type}:\n"
        + "\n".join(matched_items)
    )

# from all the evil that surrounds me defend me

def get_allergen_safe_menu(allergen_type=None, user_allergies=None):
    if user_allergies is None:
        user_allergies = []

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
        if not any(
            user_allergy in item_allergens for user_allergy in user_allergies
        ):
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
    return (
        "Here are today's available vegetarian-friendly options:\n"
        + "\n".join(veg_items)
    )

# suggestion ! ! ! ! coolest part imo

def get_food_suggestion(criteria_type, value=None):
    available = [item for item in FOOD_DATABASE if item.get("isAvailable")]
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
        return f"I recommend {chosen['name']}. It's our cheapest available meal at ₱{chosen['price']}. It has {chosen['kcal']} kcal."

    elif criteria_type == "lowest_cal":
        chosen = min(available, key=lambda x: x["kcal"])
        return f"I recommend {chosen['name']}. It has only {chosen['kcal']} kcal."

    elif criteria_type == "filling":
        chosen = max(available, key=lambda x: x["kcal"])
        return f"If you're really hungry, try {chosen['name']}. It has {chosen['kcal']} kcal."

    elif criteria_type == "vegetarian":
        filtered = [item for item in available if item["isVegetarian"]]
        if not filtered:
            return "Sorry, no vegetarian meals are available."

    elif criteria_type == "category" and value:
        target_cat = value.lower().strip()
        for item in available:
            keywords = [k.lower() for k in item.get("keywords", [])]
            name = item["name"].lower()
            allergens = [a.lower() for a in item.get("allergens", [])]

            if target_cat == "pork" and ("pork" in keywords or "pork" in name):
                filtered.append(item)
            elif target_cat == "beef" and (
                "beef" in keywords or "beef" in name
            ):
                filtered.append(item)
            elif target_cat == "chicken" and (
                "chicken" in keywords or "chicken" in name
            ):
                filtered.append(item)
            elif target_cat in ["meat", "meats"] and (
                "meat" in keywords
                or any(
                    m in name or m in keywords
                    for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
                )
            ):
                filtered.append(item)
            elif target_cat in ["fish", "seafood"] and (
                "fish" in keywords
                or "fish" in allergens
                or "seafood" in allergens
                or any(f in name for f in ["fish", "bangus", "salmon"])
            ):
                filtered.append(item)
            elif target_cat in ["vegetable", "veggie"] and (
                any(v in name for v in ["ampalaya", "monggo", "tofu"])
                or item.get("isVegetarian")
            ):
                filtered.append(item)

    elif criteria_type == "without_category" and value:
        target_cat = value.lower().strip()
        db_allergen_map = {
            "egg": "egg",
            "eggs": "egg",
            "soy": "soybean",
            "soya": "soybean",
            "soybean": "soybean",
            "dairy": "milk",
            "milk": "milk",
            "seafood": "seafood",
            "seafoods": "seafood",
            "crustacean": "crustacean",
            "crustaceans": "crustaceans",
            "nut": "nut",
            "nuts": "nut",
            "wheat": "wheat",
            "gluten": "gluten",
        }
        mapped_allergen = db_allergen_map.get(target_cat, target_cat)

        for item in available:
            keywords = [k.lower() for k in item.get("keywords", [])]
            name = item["name"].lower()
            allergens = [a.lower() for a in item.get("allergens", [])]
            is_excluded = False

            if target_cat == "pork" and ("pork" in keywords or "pork" in name):
                is_excluded = True
            elif target_cat == "beef" and ("beef" in keywords or "beef" in name):
                is_excluded = True
            elif target_cat == "chicken" and (
                "chicken" in keywords
                or "chicken" in name
                or "chicken" in allergens
            ):
                is_excluded = True
            elif target_cat in ["meat", "meats"] and (
                "meat" in keywords
                or any(
                    m in name or m in keywords
                    for m in ["pork", "beef", "chicken", "sausage", "hotdog"]
                )
            ):
                is_excluded = True
            elif target_cat in ["fish", "seafood", "seafoods"] and (
                "fish" in keywords
                or "fish" in allergens
                or "seafood" in allergens
                or "crustaceans" in allergens
                or "crustacean" in allergens
                or any(f in name for f in ["fish", "bangus", "salmon"])
            ):
                is_excluded = True
            elif target_cat in ["vegetable", "veggie", "veggies"] and (
                any(v in name for v in ["ampalaya", "monggo", "tofu"])
                or item.get("isVegetarian")
            ):
                is_excluded = True
            elif mapped_allergen in allergens or target_cat in allergens:
                is_excluded = True

            if not is_excluded:
                filtered.append(item)

        if not filtered:
            return f"Sorry, no available options found after excluding '{value}'."

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

def get_food_description(food_name, last_discussed_food=None):
    if food_name.lower().strip() == "it":
        if not last_discussed_food:
            return "What food are you referring to?", last_discussed_food
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()
    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            desc = item.get("description")
            msg = (
                f"{item['name']} - {desc}"
                if desc
                else f"{item['name']} is on our menu, but has no detailed description."
            )
            return msg, item["name"]

    return (
        f"Sorry, I couldn't find '{food_name.title()}' on our menu.",
        last_discussed_food,
    )


def get_food_price(food_name, last_discussed_food=None):
    if food_name.lower().strip() == "it":
        if not last_discussed_food:
            return (
                "Which dish are you asking the price for?",
                last_discussed_food,
            )
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()
    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            return (
                f"{item['name']} costs ₱{item['price']} alone and ₱{item['price']+15} with white rice.",
                item["name"],
            )

    return (
        f"Sorry, I couldn't find '{food_name.title()}' on our menu.",
        last_discussed_food,
    )


def get_food_calories(food_name, last_discussed_food=None):
    if food_name.lower().strip() == "it":
        if not last_discussed_food:
            return (
                "Which dish are you asking the calorie count for?",
                last_discussed_food,
            )
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()
    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            return f"{item['name']} has {item['kcal']} kcal.", item["name"]

    return (
        f"Sorry, I couldn't find '{food_name.title()}' on our menu.",
        last_discussed_food,
    )


def check_item_allergen(food_name, allergen_type, last_discussed_food=None):
    if food_name.lower().strip() == "it":
        if not last_discussed_food:
            return "Which food item are you referring to?", last_discussed_food
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()
    target_allergen = normalize_allergen(allergen_type)

    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            item_allergens = [a.lower() for a in item["allergens"]]
            if target_allergen in item_allergens:
                msg = f"Yes, {item['name']} contains **{target_allergen}**. (Listed allergens: {', '.join(item['allergens'])})"
            else:
                msg = (
                    f"No, {item['name']} does NOT contain {target_allergen}."
                    if item["allergens"]
                    else f"No, {item['name']} has no declared allergens."
                )
            return msg, item["name"]

    return (
        f"Sorry, I couldn't find '{food_name.title()}' on our menu.",
        last_discussed_food,
    )

# making order 

def process_order_creation(count_str, food_query):
    try:
        count = int(count_str)
        if count <= 0:
            return "Order quantity must be at least 1."
    except ValueError:
        return "Invalid order quantity."

    food_query_clean = food_query.strip().upper()
    selected_item = next(
        (
            item
            for item in FOOD_DATABASE
            if food_query_clean in item["name"].upper()
        ),
        None,
    )

    if not selected_item:
        return f"Sorry, we couldn't find '{food_query.title()}' on our menu."
    if not selected_item.get("isAvailable"):
        return f"Sorry, {selected_item['name']} is currently not available."

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
            orders_queue.append(
                {
                    "id_number": USER_ID_NUMBER,
                    "food_name": selected_item["name"],
                    "count": count,
                    "with_rice": with_rice,
                    "order_number": order_num,
                }
            )
            return f"Order confirmed! Your order number is #{order_num}. You are number {order_num} in queue."
        elif action == "CANCEL":
            return "Order process canceled."
        else:
            print("Please type CONFIRM or CANCEL.")

# show da queue for da impationnt pipols

def get_queue_display():
    if not orders_queue:
        return "The queue is currently empty! No orders waiting."
    queue_numbers = [
        f"#{order['order_number']}" for order in orders_queue
    ]

    queue_chain = " --- ".join(queue_numbers)

    return (
        f"Current Orders in Queue ({len(orders_queue)} Total):\n\n"
        f"{queue_chain}"
    )

def get_food_allergens_list(food_name, last_discussed_food=None):
    if food_name.lower().strip() == "it":
        if not last_discussed_food:
            return "Which food item are you referring to?", last_discussed_food
        food_name = last_discussed_food

    food_name_clean = food_name.strip().upper()
    for item in FOOD_DATABASE:
        if food_name_clean in item["name"].upper():
            allergens = item.get("allergens", [])
            if allergens:
                allergens_str = ", ".join(allergens)
                return f"{item['name']} contains the following allergens: {allergens_str}.", item["name"]
            else:
                return f"{item['name']} has no declared allergens.", item["name"]

    return (
        f"Sorry, I couldn't find '{food_name.title()}' on our menu.",
        last_discussed_food,
    )

# regex

pairs = [

    # dis is creating order na ilalagay sa napakacool na dummy queue YIPEE

    [
        r"(.*)\b(can i pick up|soon|arrive|how long will|how long before|my turn|queue|line|wait time|waiting time|how long is the line|how long is the queue|when will my order|when can i get my order)\b(.*)",
        ["DISPLAY_QUEUE"]
    ],

    [
        r"^\s*(status|situation)\s*,\s*(canteen|cafeteria)\s*$",
        ["We can not track the current state of the cafeteria. However, we can give a hint based on how many orders there are. Just type \"Queue\" to see the number of pending orders."],
    ],

    [
        r".*\b(how to order|how do i order|how to place order|how can i order|ordering process|order guide)\b.*",
        [
            "To place an order, just type the quantity and item name! For example:\n"
            "• 1 Roast Pork\n"
            "• 2 Fried Chicken"
        ],
    ],

    [
        r".*\b(how to order|how do i order|how to place order|how can i order|ordering process|order guide)\b.*",
        [
            "To place an order, just type the quantity and item name! For example:\n"
            "• 1 Roast Pork\n"
            "• 2 Fried Chicken"
        ],
    ],

    # create orders

    [
        r"^\s*(\d+)\s*,\s*(.+)\s*$",
        ["CREATE_ORDER_%1|%2"],
    ],
    [
        r"^\s*(\d+)\s+(.+)\s*$",
        ["CREATE_ORDER_%1|%2"],
    ],

    # add allergy to allergy list

    [
        r".*\b(?:i have|i\'m allergic to|im allergic to|i am allergic to|i can\'t have|i cant have|cannot eat|can\'t eat|cant eat|allergic to|not allowed to eat|dont eat|don\'t eat|avoid)\s+(?:an?\s+)?([a-zA-Z]+)(?:\s+allergy)?.*",
        ["REGISTER_ALLERGY_%1"],
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

    [
        r".*\b(allergens in|allergens of|allergens for)\s+(.+)\b.*",
        ["ALLERGEN_LIST_%2"],
    ],
    [
        r".*\b(.+)\s+(allergens|allergen list)\b.*",
        ["ALLERGEN_LIST_%1"],
    ],
    [
        r".*\b(what allergens are in|what are the allergens in)\s+(.+)\b.*",
        ["ALLERGEN_LIST_%2"],
    ],

    # asking for stuff about certain food
    
    [
        r".*\b(what is|what\'s|tell me about|describe|info on|details for)\s+(.+)\b\s*$",
        ["INFO_%2"],
    ],

    # price checker

    [
        r".*\b(how much is|price of|how much for|cost of|how much)\s+(.+)\b.*",
        ["PRICE_%2"],
    ],

    [
        r".*\b(.+)\s+(price|cost|how much)\b.*",
        ["PRICE_%1"],
    ],

    [
        r".*\b(how much is it|how much does it cost|what is the price|price|how much)\b.*",
        ["PRICE_it"],
    ],

    # calorie checker

    # Calorie checkers (Handles both "calories in roast pork" AND "roast pork calories")
    [
        r".*\b(how many calories|calorie count|kcal|calories)\s+(are\s+|)(in|of|for)\s+(.+)\b.*",
        ["CALORIES_%4"],
    ],
    [
        r".*\b(.+)\s+(calories|calorie count|kcal)\b.*",
        ["CALORIES_%1"],
    ],
    [
        r".*\b(how many calories does it have|how many calories in it|how many calories is it|calories in it)\b.*",
        ["CALORIES_it"],
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

    [
        r".*\b(suggest|recommend|pick|give me a)\b.*\b(without|no|exclude|minus|free from)\b.*\b(pork|beef|chicken|meat|meats|fish|seafood|seafoods|veggie|vegetable|veggies|soy|soya|soybean|gluten|egg|eggs|dairy|milk)\b.*",
        ["SUGGEST_WITHOUT_%3"],
    ],

    # recommend for brokies

    [
        r".*\b(suggest|recommend|what can i get|food|lunch|dinner|breakfast)\b.*\b(\d+)\b\s*(peso|pesos|php|p|budget|).*",
        ["SUGGEST_BUDGET_%2"],
    ],

    # recommendation tong mga sunod

    [
        r".*\b(suggest|recommend|pick|want)\b.*\b(pork|beef|chicken|meat|meats|fish|seafood|veggie|vegetable)\b.*",
        ["SUGGEST_CATEGORY_%2"],
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
        r".*\b(suggest|recommend|what should i eat|pick for me)\b.*",
        ["SUGGEST_GENERAL"],
    ],

    # just indecisive

    [
        r".*\b(suggest|recommend|what should i eat|pick for me)\b.*",
        ["SUGGEST_GENERAL"],
    ],

    # without meats

    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero|doesnt have|doesn\'t have|does not have|has no)\b.*\b(pork)\b.*",
        ["WITHOUT_pork"],
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero|doesnt have|doesn\'t have|does not have|has no)\b.*\b(beef)\b.*",
        ["WITHOUT_beef"],
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero|doesnt have|doesn\'t have|does not have|has no)\b.*\b(chicken)\b.*",
        ["WITHOUT_chicken"],
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero|doesnt have|doesn\'t have|does not have|has no)\b.*\b(fish|seafood|seafoods)\b.*",
        ["WITHOUT_fish"],
    ],
    [
        r".*\b(without|no|not|dont|don\'t|exclude|minus|skip|remove|zero|doesnt have|doesn\'t have|does not have|has no)\b.*\b(meat|meats)\b.*",
        ["WITHOUT_meat"],
    ],
    [
        r".*\b(allergic to|allergy|allergies|no|without|free from|exclude|minus|skip|remove)\s+(to\s+|)\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|wheat|chicken)\b.*",
        ["ALLERGEN_%3"],
    ],
    [
        r".*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|wheat|chicken)\s+(free|allergy|allergies|intolerant)\b.*",
        ["ALLERGEN_%1"],
    ],
    [
        r"^(?!.*\b(no|not|without|cant|can\'t|cannot|dont|don\'t)\b).*\b(food|dish|meal|what)\b.*\b(with|contains|has)\b.*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*",
        ["FOOD_WITH_ALLERGEN_%4"],
    ],
    [
        r".*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*\b(food|dish|meal)\b.*",
        ["FOOD_WITH_ALLERGEN_%1"],
    ],

    # Catches general requests like "food with egg" or "dish with shrimp"
    [
        r"^(?!.*\b(no|not|without|cant|can\'t|cannot|dont|don\'t)\b).*\b(food|dish|meal|what)\b.*\b(with|contains|has)\b.*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*",
        ["FOOD_WITH_ALLERGEN_%4"],
    ],

    # Catches direct questions like "show me food with dairy"
    [
        r".*\b(egg|eggs|gluten|soy|soybean|fish|seafood|milk|dairy|nut|nuts|celery|mustard|sulphite|crustacean|crustaceans|sesame|chicken|wheat)\b.*\b(food|dish|meal)\b.*",
        ["FOOD_WITH_ALLERGEN_%1"],
    ],

    # herbivore 

    [
        r".*\b(vegetarian|veggie|meatless|no meat|plant based|vegetables)\b.*",
        ["FETCH_VEGETARIAN"],
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

    # oh cool

    [
        r".*\b(combo|combos|rice meal|with rice|extra rice|add rice|rice combo)\b.*",
        [
            "All main dishes can be ordered ala carte or made into a meal by adding white rice for an extra ₱15 (205 kcal)!"
        ],
    ],

    # ordering, claiming, or not claiming kung gusto mong mapunta sdfo
    
    

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

    # victor act 4

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
        r"(hi|hello|hey|good (morning|afternoon|evening))",
        [
            "Hello! Welcome to ArcherEats support. How can I help you today?",
            "Hi there! Need help with anything?",
        ],
    ],

    [
        r"(bye|goodbye|exit|quit)",
        [
            "Thank you for using ArcherEats support. Have a great day!",
            "Goodbye! Your ArcherEats support assistant is always here to help.",
        ],
    ],

    [
        r"(.*)(thank|thanks)(.*)",
        ["You're welcome! Enjoy your meal!"]
    ],

# GOGOGOGO SPAM SPAM SPAM ERROR HANDLING SUGGESTION RAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH
    
    [
        r".*\b(cost|price|cheap|expensive|money|peso|pesos|php|pay|how much|price|budget)\b.*",
        [
            "Looking for pricing details? You can ask me:\n"
            "• 'How much is Roast Pork?'\n"
            "• 'Show me meals under 100 pesos'\n"
            "• 'What is the cheapest meal?'"
        ],
    ],

    [
        r".*\b(contain|contains|ingredient|ingredients|inside|recipe|allergy|allergies|allergic|safe|eat|food|dish|meal|can eat|cant eat|can\'t eat|shouldn\'t eat|shouldnt eat)\b.*",
        [
            "Trying to check ingredients or find a safe dish? Try asking:\n"
            "• 'Does Fried Chicken contain eggs?'\n"
            "• 'I am allergic to seafood'\n"
            "• 'Show me food with dairy'"
        ],
    ],

    [
        r".*\b(calorie|calories|kcal|diet|heavy|light|weight|fat|fit|bulk|healthy|health)\b.*",
        [
            "Interested in calorie and nutritional counts? You can ask:\n"
            "• 'How many calories are in Tofu Sisig?'\n"
            "• 'Suggest a low calorie meal'\n"
            "• 'What is the most filling option?'"
        ],
    ],

    [
        r".*\b(hungry|eat|food|lunch|dinner|breakfast|recommend|suggest|want|find|search|options|available)\b.*",
        [
            "Not sure what to choose? Here are some ways you can ask for recommendations:\n"
            "• 'Suggest a pork dish'\n"
            "• 'Show me lunch options'\n"
            "• 'Recommend something vegetarian'\n"
            "• 'Suggest something without chicken'"
        ],
    ],

    [
        r".*\b(order|buy|get|purchase|add|queue|tray)\b.*",
        [
            "Want to place an order? You can easily order by typing the quantity and item name:\n"
            "• '1 Roast Pork'\n"
            "• '2 Fried Chicken'\n"
            "Or ask: 'How do I place an order?'"
        ],
    ],

    [
        r"(.*)(shin|shintaroh|nomoto|emperor)(.*)",
        ["shin did not get enough sleep for this"]
    ],

    [
        r".*",
        [
            "I'm not quite sure what you're looking for, but I can help you with menu info, allergies, and recommendations!\n\n"
            "Try phrasing your query like this:\n"
            "• Menu: 'What's on the menu?' or 'Show me breakfast options'\n"
            "• Food Info: 'Tell me about Braised Beef' or 'Price of Tofu Sisig'\n"
            "• Allergies: 'I am allergic to gluten' or 'Does Pork BBQ contain soy?'\n"
            "• Ordering: '1 Roast Pork'"
        ],
    ],
 ]



chatbot = Chat(pairs, reflections)

if __name__ == "__main__":
    local_user_allergies = []
    local_last_discussed_food = None

    print(
        "Hi, I'm ArcherBot! Ask me anything about the menu, allergies, and suggestions! \n"
        "- What's on the menu?\n"
        "- What can I get if I have seafood allergy?\n"
        "- Suggest anything without pork. \n"
        "- How to place order?"
    )

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

                elif clean_response.startswith("REGISTER_ALLERGY_"):
                    allergen = clean_response.replace("REGISTER_ALLERGY_", "")
                    msg, local_user_allergies = register_user_allergy(
                        allergen, local_user_allergies
                    )
                    print(msg)
                    print(
                        get_allergen_safe_menu(
                            user_allergies=local_user_allergies
                        )
                    )

                elif clean_response.startswith("CATEGORY_"):
                    category = clean_response.replace("CATEGORY_", "")
                    print(get_category_menu(category))

                elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
                    allergen = clean_response.replace("FOOD_WITH_ALLERGEN_", "")
                    print(get_food_with_allergen(allergen))

                elif clean_response.startswith("WITHOUT_"):
                    category = clean_response.replace("WITHOUT_", "")
                    print(get_category_removed_menu(category))

                elif clean_response.startswith("SUGGEST_WITHOUT_"):
                    category = clean_response.replace("SUGGEST_WITHOUT_", "")
                    print(get_food_suggestion("without_category", category))

                elif clean_response.startswith("SUGGEST_CATEGORY_"):
                    category = clean_response.replace("SUGGEST_CATEGORY_", "")
                    print(get_food_suggestion("category", category))

                elif clean_response.startswith("ALLERGEN_"):
                    allergen = clean_response.replace("ALLERGEN_", "")
                    print(
                        get_allergen_safe_menu(
                            allergen, local_user_allergies
                        )
                    )

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
                    msg, local_last_discussed_food = get_food_description(
                        food, local_last_discussed_food
                    )
                    print(msg)

                elif clean_response.startswith("PRICE_"):
                    food = clean_response.replace("PRICE_", "")
                    msg, local_last_discussed_food = get_food_price(
                        food, local_last_discussed_food
                    )
                    print(msg)

                elif clean_response.startswith("CALORIES_"):
                    food = clean_response.replace("CALORIES_", "")
                    msg, local_last_discussed_food = get_food_calories(
                        food, local_last_discussed_food
                    )
                    print(msg)

                elif clean_response.startswith("CHECK_ALLERGEN_"):
                    payload = clean_response.replace("CHECK_ALLERGEN_", "")
                    if "|" in payload:
                        food_item, allergen = payload.split("|", 1)
                        msg, local_last_discussed_food = check_item_allergen(
                            food_item, allergen, local_last_discussed_food
                        )
                        print(msg)
                    else:
                        print("Could not process allergen check query.")

                elif clean_response.startswith("MEAL_"):
                    meal = clean_response.replace("MEAL_", "")
                    print(get_meal_type_menu(meal))

                elif clean_response.startswith("ALLERGEN_LIST_"):
                    food = clean_response.replace("ALLERGEN_LIST_", "")
                    msg, local_last_discussed_food = get_food_allergens_list(
                        food, local_last_discussed_food
                    )
                    print(msg)

                elif clean_response == "DISPLAY_QUEUE":
                    print(get_queue_display())

                elif clean_response.startswith("CREATE_ORDER_"):
                    payload = clean_response.replace("CREATE_ORDER_", "")
                    if "|" in payload:
                        count_str, food_query = payload.split("|", 1)
                        print(process_order_creation(count_str, food_query))

                elif clean_response == "IDENTIFY_ALLERGY":
                    msg, local_user_allergies = add_allergies(
                        user_allergies=local_user_allergies
                    )
                    print(msg)
                    if "Gotcha!" in msg:
                        print(
                            get_allergen_safe_menu(
                                user_allergies=local_user_allergies
                            )
                        )
                else:
                    print(response)
            else:
                print(
                    "I understand the general topic, but could you please rephrase your request?"
                )

        except (KeyboardInterrupt, EOFError, SystemExit):
            break