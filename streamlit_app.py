import streamlit as st
from streamlit_chat import message
import re

# Import the chatbot and helper functions from your now-silent ChatBot.py
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

# 1. Custom Visual Branding and Layout from the image
st.set_page_config(page_title="ArcherBot", page_icon="🏹", layout="centered")

# Custom CSS for colors and appearance (Matching the dark green header and fonts)
st.markdown("""
    <style>
    /* Dark Green Header Band */
    .main-header {
        background-color: #1e5a36; /* Exact DLSU Green */
        color: white;
        padding: 20px 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
    }
    .main-header .sub-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 14px;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: -5px;
    }
    .main-header .main-title {
        font-family: 'Georgia', serif; /* Serif-like font for "ArcherBot" */
        font-size: 36px;
        font-weight: bold;
        margin: 0;
    }
    
    /* Fix input alignment and general container spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Advanced chat styling adjustment for cleaner integration */
    [data-testid="stChatMessage"] {
        padding: 1rem 1.5rem;
    }
    </style>
    
    <div class="main-header">
        <span class="sub-text">Powered by DLSU Dining</span>
        <span class="main-title">ArcherBot</span>
    </div>
""", unsafe_allow_html=True)


# 2. Chat History Initializer (Remembering the conversation)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm ArcherBot 🤖 Ask me anything about today's menu, prices, or allergens!"}
    ]


# 3. Web-Safe Order Creation (Bypasses terminal y/n input)
# We must use this instead of process_order_creation() which freezes the server
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
        "with_rice": False, # Default to without rice, we cannot ask y/n easily on web
        "order_number": order_num,
    }
    orders_queue.append(new_order)
    
    unit_price = selected_item["price"]
    total = unit_price * count
    
    # Using markdown for nice formatting of the receipt
    bot_text = (
        f"✅ **Order Placed!**\n\n"
        f"• ID Number : `{USER_ID_NUMBER}`\n"
        f"• Item      : {count}x {selected_item['name']} (ala carte)\n"
        f"• Unit Price: ₱{unit_price}\n"
        f"• Total     : **₱{total}**\n\n"
        f"Your order number is **#{order_num}**. You are number {order_num} in queue."
    )
    return bot_text


# 4. Main Chat Interface Logic
# The chat bubbles are generated dynamically, pinned inputs below.

# Display all existing chat history from the session memory
for idx, msg in enumerate(st.session_state.messages):
    # Using advanced streamlit_chat component for better visual bubbles (and avatars)
    message(
        msg["content"], 
        is_user=(msg["role"] == "user"), 
        key=f"msg_{idx}", 
        # Using a green avatar for the bot
        logo="https://raw.githubusercontent.com/streamlit/chat-sample/master/logo/logo-green.png" if msg["role"] == "assistant" else None
    )


# 5. Handle New User Input
if user_input := st.chat_input("Ask ArcherBot..."):
    # Display and store the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"new_{len(st.session_state.messages)}")

    # Process response via NLTK chatbot
    response = chatbot.respond(user_input)
    bot_text = "I understand the topic, but could you please rephrase your request?"

    if response:
        clean_response = response.strip()

        # Complex response handler (Connecting NLTK intent tags to logic)
        # All original intents from ChatBot.py's while loop are mapped here.
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
                # Call our specialized web order function (NO BLOCKING INPUTS)
                bot_text = web_process_order(count_str, food_query)
        elif clean_response == "IDENTIFY_ALLERGY":
            bot_text = "Please specify exactly what you are allergic to (e.g., 'I am allergic to eggs')."
        else:
            bot_text = clean_response

    # Display and store the bot's response
    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    message(
        bot_text, 
        is_user=False, 
        key=f"bot_{len(st.session_state.messages)}",
        logo="https://raw.githubusercontent.com/streamlit/chat-sample/master/logo/logo-green.png"
    )
