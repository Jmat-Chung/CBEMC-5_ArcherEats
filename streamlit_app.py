import streamlit as st
import re

# Import the chatbot and helper functions from ChatBot.py
from ChatBot import (
    chatbot, 
    FOOD_DATABASE, 
    orders_queue,
    USER_ID_NUMBER,
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

# --- 1. Page Configuration & Custom DLSU Green Header ---
st.set_page_config(page_title="ArcherEats", page_icon="🏹", layout="centered")

# Custom CSS for DLSU Green branding matching your reference image
st.markdown("""
    <style>
    /* Dark Green Header Bar */
    .main-header {
        background-color: #1e5a36; /* DLSU Green */
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
""", unsafe_allow_html=True)


# --- 2. Chat Session History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hi! I'm ArcherEats 🤖 Ask me anything about today's menu, prices, or allergens!"
        }
    ]


# --- 3. Web-Safe Order Function (No blocking terminal inputs) ---
def web_process_order(count_str, food_query):
    try:
        count = int(count_str)
        if count <= 0:
            return "Order quantity must be at least 1."
    except ValueError:
        return "Invalid order quantity."

    food_query_clean = food_query.strip().upper()
    selected_item = next((item for item in FOOD_DATABASE if food_query_clean in item["name"].upper()), None)

    if not selected_item:
        return f"Sorry, we couldn't find '{food_query.title()}' on our menu."

    if not selected_item.get("isAvailable"):
        return f"Sorry, {selected_item['name']} is currently not available."

    order_num = len(orders_queue) + 1
    new_order = {
        "id_number": USER_ID_NUMBER,
        "food_name": selected_item["name"],
        "count": count,
        "with_rice": False,
        "order_number": order_num,
    }
    orders_queue.append(new_order)
    
    unit_price = selected_item["price"]
    total = unit_price * count
    
    return (
        f"✅ **Order Placed!**\n\n"
        f"• **Item:** {count}x {selected_item['name']}\n"
        f"• **Total:** ₱{total}\n"
        f"• **Order Number:** `#{order_num}`\n\n"
        f"You are number {order_num} in queue."
    )


# --- 4. Render Chat History ---
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# --- 5. User Input & Bot Response Handling ---
if user_input := st.chat_input("Ask ArcherEats..."):
    # Render user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Process response with ChatBot logic
    response = chatbot.respond(user_input)
    bot_text = "I understand the topic, but could you please rephrase your request?"

    if response:
        clean_response = response.strip()

        if clean_response == "FETCH_MENU":
            bot_text = get_available_menu()
        elif clean_response == "FETCH_VEGETARIAN":
            bot_text = get_vegetarian_menu()
        elif clean_response.startswith("CATEGORY_"):
            bot_text = get_category_menu(clean_response.replace("CATEGORY_", ""))
        elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
            bot_text = get_food_with_allergen(clean_response.replace("FOOD_WITH_ALLERGEN_", ""))
        elif clean_response.startswith("WITHOUT_"):
            bot_text = get_category_removed_menu(clean_response.replace("WITHOUT_", ""))
        elif clean_response.startswith("SUGGEST_CATEGORY_"):
            bot_text = get_food_suggestion("category", clean_response.replace("SUGGEST_CATEGORY_", ""))
        elif clean_response.startswith("ALLERGEN_"):
            bot_text = get_allergen_safe_menu(clean_response.replace("ALLERGEN_", ""))
        elif clean_response.startswith("SUGGEST_BUDGET_"):
            bot_text = get_food_suggestion("budget", clean_response.replace("SUGGEST_BUDGET_", ""))
        elif clean_response == "SUGGEST_HIGHCAL":
            bot_text = get_food_suggestion("high_cal")
        elif clean_response == "SUGGEST_LOWCAL":
            bot_text = get_food_suggestion("low_cal")
        elif clean_response == "SUGGEST_GENERAL":
            bot_text = get_food_suggestion("general")
        elif clean_response.startswith("SUGGEST_ALLERGEN_"):
            bot_text = get_food_suggestion("allergen", clean_response.replace("SUGGEST_ALLERGEN_", ""))
        elif clean_response == "SUGGEST_CHEAPEST":
            bot_text = get_food_suggestion("cheapest")
        elif clean_response == "SUGGEST_LOWESTCAL":
            bot_text = get_food_suggestion("lowest_cal")
        elif clean_response == "SUGGEST_FILLING":
            bot_text = get_food_suggestion("filling")
        elif clean_response == "SUGGEST_VEGETARIAN":
            bot_text = get_food_suggestion("vegetarian")
        elif clean_response.startswith("INFO_"):
            bot_text = get_food_description(clean_response.replace("INFO_", ""))
        elif clean_response.startswith("PRICE_"):
            bot_text = get_food_price(clean_response.replace("PRICE_", ""))
        elif clean_response.startswith("CALORIES_"):
            bot_text = get_food_calories(clean_response.replace("CALORIES_", ""))
        elif clean_response.startswith("CHECK_ALLERGEN_"):
            payload = clean_response.replace("CHECK_ALLERGEN_", "")
            if "|" in payload:
                food_item, allergen = payload.split("|", 1)
                bot_text = check_item_allergen(food_item, allergen)
            else:
                bot_text = "Could not process allergen check."
        elif clean_response.startswith("MEAL_"):
            bot_text = get_meal_type_menu(clean_response.replace("MEAL_", ""))
        elif clean_response.startswith("CREATE_ORDER_"):
            payload = clean_response.replace("CREATE_ORDER_", "")
            if "|" in payload:
                count_str, food_query = payload.split("|", 1)
                bot_text = web_process_order(count_str, food_query)
        elif clean_response == "IDENTIFY_ALLERGY":
            bot_text = "Please specify what you are allergic to (e.g., 'I am allergic to eggs')."
        else:
            bot_text = clean_response

    # Render bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_text)
