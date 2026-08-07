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

# Import chatbot engine and data helpers from ChatBot.py
from ChatBot import (
    FOOD_DATABASE,
    USER_ID_NUMBER,
    chatbot,
    check_item_allergen,
    get_allergen_safe_menu,
    get_available_menu,
    get_category_menu,
    get_category_removed_menu,
    get_food_calories,
    get_food_description,
    get_food_price,
    get_food_suggestion,
    get_food_with_allergen,
    get_meal_type_menu,
    get_queue_display,
    get_vegetarian_menu,
    orders_queue,
    register_user_allergy,
    get_food_allergens_list,
)

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="ArcherEats", page_icon="🏹", layout="centered")

# --- Custom Styling Header ---
st.markdown(
    """
    <style>
    .main-header {
        background-color: #1e5a36;
        color: white;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .main-header .sub-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 14px;
        font-weight: 300;
        opacity: 0.9;
    }
    .main-header .main-title {
        font-family: 'Georgia', serif;
        font-size: 34px;
        font-weight: bold;
        margin-top: 4px;
    }
    </style>
    
    <div class="main-header">
        <div class="sub-text">CBEMC-5 ChatBot by CHUNG-NOMOTO-RICALDE-VASCO</div>
        <div class="main-title">ArcherEats</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I'm ArcherBot! Ask me anything about the menu, allergies, and suggestions!  \n- What's on the menu?  \n- What can I get if I have seafood allergy?  \n- Suggest anything without pork.  \n- How to place order?",
        }
    ]
if "order_state" not in st.session_state:
    st.session_state.order_state = "IDLE"
if "pending_order" not in st.session_state:
    st.session_state.pending_order = None

if "user_allergies" not in st.session_state:
    st.session_state.user_allergies = []
if "last_discussed_food" not in st.session_state:
    st.session_state.last_discussed_food = None


# --- Web Ordering State Logic ---
def start_web_order(count_str, food_query):
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

    st.session_state.pending_order = {
        "item": selected_item,
        "count": count,
        "with_rice": False,
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


# --- Render Conversation History ---
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# --- Chat Input Processing ---
if user_input := st.chat_input("Ask ArcherEats..."):
    user_input = user_input.replace("\n", "").replace("\r", "").strip()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    user_input_clean = user_input.strip().lower()
    bot_text = ""

    # 1. Active Order State Machine
    if st.session_state.order_state == "AWAITING_RICE":
        if user_input_clean in ["y", "yes"]:
            st.session_state.pending_order["with_rice"] = True
            bot_text = generate_order_summary()
            st.session_state.order_state = "AWAITING_CONFIRM"
        elif user_input_clean in ["n", "no"]:
            st.session_state.pending_order["with_rice"] = False
            bot_text = generate_order_summary()
            st.session_state.order_state = "AWAITING_CONFIRM"
        else:
            bot_text = "Please answer with 'y' or 'n'."

    elif st.session_state.order_state == "AWAITING_CONFIRM":
        if user_input_clean == "confirm":
            pending = st.session_state.pending_order
            order_num = len(orders_queue) + 1
            orders_queue.append(
                {
                    "id_number": USER_ID_NUMBER,
                    "food_name": pending["item"]["name"],
                    "count": pending["count"],
                    "with_rice": pending["with_rice"],
                    "order_number": order_num,
                }
            )
            bot_text = f"✅ **Order Placed Successfully!**\nYour order number is `#{order_num}`."
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        elif user_input_clean == "cancel":
            bot_text = "Order cancelled."
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        else:
            bot_text = "Please type CONFIRM or CANCEL."

    # 2. Main Chatbot Routing (Connected directly to ChatBot.py responses)
    else:
        response = chatbot.respond(user_input)

        if response:
            clean_response = response.strip()

            if clean_response == "FETCH_MENU":
                bot_text = get_available_menu()
            elif clean_response == "FETCH_VEGETARIAN":
                bot_text = get_vegetarian_menu()
            elif clean_response == "DISPLAY_QUEUE":
                bot_text = get_queue_display()
            elif clean_response.startswith("CATEGORY_"):
                bot_text = get_category_menu(
                    clean_response.replace("CATEGORY_", "")
                )
            elif clean_response.startswith("WITHOUT_"):
                bot_text = get_category_removed_menu(
                    clean_response.replace("WITHOUT_", "")
                )
            elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
                bot_text = get_food_with_allergen(
                    clean_response.replace("FOOD_WITH_ALLERGEN_", "")
                )
            elif clean_response.startswith("ALLERGEN_"):
                allergen = clean_response.replace("ALLERGEN_", "")
                bot_text = get_allergen_safe_menu(
                    allergen, st.session_state.user_allergies
                )
            elif clean_response.startswith("REGISTER_ALLERGY_"):
                allergen = clean_response.replace("REGISTER_ALLERGY_", "")
                confirm_msg, st.session_state.user_allergies = (
                    register_user_allergy(
                        allergen, st.session_state.user_allergies
                    )
                )
                safe_menu = get_allergen_safe_menu(
                    user_allergies=st.session_state.user_allergies
                )
                bot_text = f"{confirm_msg}\n\n{safe_menu}"
            elif clean_response.startswith("SUGGEST_CATEGORY_"):
                cat = clean_response.replace("SUGGEST_CATEGORY_", "")
                bot_text = get_food_suggestion("category", cat)
            elif clean_response.startswith("SUGGEST_WITHOUT_"):
                cat = clean_response.replace("SUGGEST_WITHOUT_", "")
                bot_text = get_food_suggestion("without_category", cat)
            elif clean_response.startswith("SUGGEST_BUDGET_"):
                amount = clean_response.replace("SUGGEST_BUDGET_", "")
                bot_text = get_food_suggestion("budget", amount)
            elif clean_response.startswith("SUGGEST_ALLERGEN_"):
                allergen = clean_response.replace("SUGGEST_ALLERGEN_", "")
                bot_text = get_food_suggestion("allergen", allergen)
            elif clean_response == "SUGGEST_HIGHCAL":
                bot_text = get_food_suggestion("high_cal")
            elif clean_response == "SUGGEST_LOWCAL":
                bot_text = get_food_suggestion("low_cal")
            elif clean_response == "SUGGEST_GENERAL":
                bot_text = get_food_suggestion("general")
            elif clean_response == "SUGGEST_CHEAPEST":
                bot_text = get_food_suggestion("cheapest")
            elif clean_response == "SUGGEST_LOWESTCAL":
                bot_text = get_food_suggestion("lowest_cal")
            elif clean_response == "SUGGEST_FILLING":
                bot_text = get_food_suggestion("filling")
            elif clean_response == "SUGGEST_VEGETARIAN":
                bot_text = get_food_suggestion("vegetarian")

            # --- ITEM DETAIL HANDLERS (INFO, PRICE, CALORIES, ALLERGEN CHECKS) ---
            elif clean_response.startswith("INFO_"):
                food = clean_response.replace("INFO_", "")
                bot_text, st.session_state.last_discussed_food = (
                    get_food_description(
                        food, st.session_state.last_discussed_food
                    )
                )
            elif clean_response.startswith("PRICE_"):
                food = clean_response.replace("PRICE_", "")
                bot_text, st.session_state.last_discussed_food = (
                    get_food_price(food, st.session_state.last_discussed_food)
                )
            elif clean_response.startswith("CALORIES_"):
                food = clean_response.replace("CALORIES_", "")
                bot_text, st.session_state.last_discussed_food = (
                    get_food_calories(
                        food, st.session_state.last_discussed_food
                    )
                )
            elif clean_response.startswith("CHECK_ALLERGEN_"):
                payload = clean_response.replace("CHECK_ALLERGEN_", "")
                if "|" in payload:
                    food_item, allergen = payload.split("|", 1)
                    bot_text, st.session_state.last_discussed_food = (
                        check_item_allergen(
                            food_item,
                            allergen,
                            st.session_state.last_discussed_food,
                        )
                    )

            elif clean_response == "IDENTIFY_ALLERGY":
                bot_text = (
                    "Please state your allergy (e.g., 'I am allergic to eggs')."
                )

            elif clean_response.startswith("ALLERGEN_LIST_"):
                food = clean_response.replace("ALLERGEN_LIST_", "")
                bot_text, st.session_state.last_discussed_food = (
                    get_food_allergens_list(
                        food, st.session_state.last_discussed_food
                    )
                )
            elif clean_response.startswith("CREATE_ORDER_"):
                payload = clean_response.replace("CREATE_ORDER_", "")
                if "|" in payload:
                    count_str, food_query = payload.split("|", 1)
                    bot_text = start_web_order(count_str, food_query)
            else:
                bot_text = clean_response
        else:
            bot_text = (
                "I didn't quite catch that. Here are a few ways you can ask me:\n\n"
                "• **Menu**: *'What's on the menu?'*\n"
                "• **Allergies**: *'I have a soy allergy'*\n"
                "• **Suggestions**: *'Suggest a meal under 100 pesos'*\n"
                "• **Order**: *'1 Roast Pork'*"
            )

    bot_text = str(bot_text).replace("\n", "  \n")
    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_text)