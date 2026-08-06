# =====================================================================
#  CBEMC-5 X40
#  Final Project - ArcherEats Chatbot
#  Members:
#    - CHUNG, Josh Matthew A.
#    - NOMOTO, Shintaroh
#    - RICALDE, Jhobert Alfonso V.
#    - VASCO, Victor Gerald N.
# =====================================================================

import streamlit as st
from ChatBot import (
    chatbot, 
    FOOD_DATABASE, 
    orders_queue,
    USER_ID_NUMBER,
    register_user_allergy,
    get_available_menu, 
    get_vegetarian_menu,
    get_meal_type_menu,
    get_category_menu,
    get_category_removed_menu,
    get_food_with_allergen,
    get_allergen_safe_menu,
    get_food_suggestion,
    get_food_description,
    get_food_price,
    get_food_calories,
    check_item_allergen
)

st.set_page_config(page_title="ArcherEats", page_icon="🏹", layout="centered")

# --- Initialize Session Memory State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm ArcherBot! Ask me anything about the menu, allergies, and suggestions!  \n- What's on the menu?  \n- What can I get if I have seafood allergy?  \n- Suggest anything without pork.  \n- How to place order?"}
    ]
if "order_state" not in st.session_state:
    st.session_state.order_state = "IDLE"
if "pending_order" not in st.session_state:
    st.session_state.pending_order = None

# LOCAL MEMORY IN SESSION STATE
if "user_allergies" not in st.session_state:
    st.session_state.user_allergies = []
if "last_discussed_food" not in st.session_state:
    st.session_state.last_discussed_food = None


def start_web_order(count_str, food_query):
    try:
        count = int(count_str)
        if count <= 0: return "Order quantity must be at least 1."
    except ValueError:
        return "Invalid order quantity."

    food_query_clean = food_query.strip().upper()
    selected_item = next((item for item in FOOD_DATABASE if food_query_clean in item["name"].upper()), None)

    if not selected_item:
        return f"Sorry, we couldn't find '{food_query.title()}' on our menu."
    if not selected_item.get("isAvailable"):
        return f"Sorry, {selected_item['name']} is currently not available."

    st.session_state.pending_order = {
        "item": selected_item,
        "count": count,
        "with_rice": False
    }
    st.session_state.order_state = "AWAITING_RICE"
    st.session_state.last_discussed_food = selected_item["name"]

    return f"Would you like to add rice to your {count}x {selected_item['name']} for an additional ₱15 per item? [y/n]"


def generate_order_summary():
    pending = st.session_state.pending_order
    item = pending["item"]
    count = pending["count"]
    with_rice = pending["with_rice"]

    unit_price = item["price"] + (15 if with_rice else 0)
    total = unit_price * count
    rice_text = "(with rice)" if with_rice else "(ala carte)"

    return (
        "--- ORDER SUMMARY ---\n"
        f"ID Number : {USER_ID_NUMBER}\n"
        f"Item      : {count}x {item['name']} {rice_text}\n"
        f"Unit Price: ₱{unit_price}\n"
        f"Total     : ₱{total}\n"
        "---------------------\n"
        "Type CONFIRM to place your order or CANCEL to abort."
    )


# --- Render Messages ---
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# --- Handle Input ---
if user_input := st.chat_input("Ask ArcherEats..."):
    user_input = user_input.replace('\n', '').replace('\r', '').strip()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    user_input_clean = user_input.strip().lower()
    bot_text = ""

    # Ordering state engine
    if st.session_state.order_state == "AWAITING_RICE":
        if user_input_clean in ['y', 'yes']:
            st.session_state.pending_order["with_rice"] = True
            bot_text = generate_order_summary()
            st.session_state.order_state = "AWAITING_CONFIRM"
        elif user_input_clean in ['n', 'no']:
            st.session_state.pending_order["with_rice"] = False
            bot_text = generate_order_summary()
            st.session_state.order_state = "AWAITING_CONFIRM"
        else:
            bot_text = "Please answer with 'y' or 'n'."

    elif st.session_state.order_state == "AWAITING_CONFIRM":
        if user_input_clean == "confirm":
            pending = st.session_state.pending_order
            order_num = len(orders_queue) + 1
            orders_queue.append({
                "id_number": USER_ID_NUMBER,
                "food_name": pending["item"]["name"],
                "count": pending["count"],
                "with_rice": pending["with_rice"],
                "order_number": order_num,
            })
            bot_text = f"✅ **Order Placed Successfully!**\nYour order number is `#{order_num}`."
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        elif user_input_clean == "cancel":
            bot_text = "Order cancelled."
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        else:
            bot_text = "Please type CONFIRM or CANCEL."

    # Standard query processing
    else:
        response = chatbot.respond(user_input)
        
        if response:
            clean_response = response.strip()

            if clean_response == "FETCH_MENU":
                bot_text = get_available_menu()
            elif clean_response == "FETCH_VEGETARIAN":
                bot_text = get_vegetarian_menu()
            elif clean_response.startswith("CATEGORY_"):
                bot_text = get_category_menu(clean_response.replace("CATEGORY_", ""))
            elif clean_response.startswith("WITHOUT_"):
                bot_text = get_category_removed_menu(clean_response.replace("WITHOUT_", ""))
            elif clean_response.startswith("ALLERGEN_"):
                allergen = clean_response.replace("ALLERGEN_", "")
                bot_text = get_allergen_safe_menu(allergen, st.session_state.user_allergies)
            elif clean_response.startswith("INFO_"):
                food = clean_response.replace("INFO_", "")
                bot_text, st.session_state.last_discussed_food = get_food_description(food, st.session_state.last_discussed_food)
            elif clean_response.startswith("PRICE_"):
                food = clean_response.replace("PRICE_", "")
                bot_text, st.session_state.last_discussed_food = get_food_price(food, st.session_state.last_discussed_food)
            elif clean_response.startswith("CALORIES_"):
                food = clean_response.replace("CALORIES_", "")
                bot_text, st.session_state.last_discussed_food = get_food_calories(food, st.session_state.last_discussed_food)
            elif clean_response.startswith("CHECK_ALLERGEN_"):
                payload = clean_response.replace("CHECK_ALLERGEN_", "")
                if "|" in payload:
                    food_item, allergen = payload.split("|", 1)
                    bot_text, st.session_state.last_discussed_food = check_item_allergen(food_item, allergen, st.session_state.last_discussed_food)
            elif clean_response == "IDENTIFY_ALLERGY":
                bot_text = "Please state your allergy (e.g., 'I am allergic to eggs')."
            elif clean_response.startswith("CREATE_ORDER_"):
                payload = clean_response.replace("CREATE_ORDER_", "")
                if "|" in payload:
                    count_str, food_query = payload.split("|", 1)
                    bot_text = start_web_order(count_str, food_query)
            else:
                bot_text = clean_response
        else:
            bot_text = "I understand the topic, but could you please rephrase?"

    bot_text = str(bot_text).replace('\n', '  \n')
    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_text)