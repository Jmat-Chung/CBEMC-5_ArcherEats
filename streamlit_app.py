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

st.markdown("""
    <style>
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


# --- 2. Chat Session History & State Machine ---
# We use this to remember where the user is in the ordering process
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm ArcherEats. How can I help you?"}
    ]
if "order_state" not in st.session_state:
    st.session_state.order_state = "IDLE"  # Can be IDLE, AWAITING_RICE, AWAITING_CONFIRM
if "pending_order" not in st.session_state:
    st.session_state.pending_order = None


# --- 3. Conversational Ordering Functions ---

def start_web_order(count_str, food_query):
    """Step 1: Validate item and ask about rice."""
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

    # Save details into memory and change bot state
    st.session_state.pending_order = {
        "item": selected_item,
        "count": count,
        "with_rice": False
    }
    st.session_state.order_state = "AWAITING_RICE"

    return f"Would you like to add rice to your {count}x {selected_item['name']} for an additional ₱15 per item? [y/n]"

def generate_order_summary():
    """Step 2: Show the receipt and ask for confirmation."""
    pending = st.session_state.pending_order
    item = pending["item"]
    count = pending["count"]
    with_rice = pending["with_rice"]

    unit_price = item["price"] + (15 if with_rice else 0)
    total = unit_price * count
    rice_text = "(with rice)" if with_rice else "(ala carte)"

    summary = (
        "--- ORDER SUMMARY ---\n"
        f"ID Number : {USER_ID_NUMBER}\n"
        f"Item      : {count}x {item['name']} {rice_text}\n"
        f"Unit Price: ₱{unit_price}\n"
        f"Total     : ₱{total}\n"
        "---------------------\n"
        "Type CONFIRM to place your order or CANCEL to abort."
    )
    return summary

def finalize_order():
    """Step 3: Save order to queue and clear memory."""
    pending = st.session_state.pending_order
    order_num = len(orders_queue) + 1
    
    new_order = {
        "id_number": USER_ID_NUMBER,
        "food_name": pending["item"]["name"],
        "count": pending["count"],
        "with_rice": pending["with_rice"],
        "order_number": order_num,
    }
    orders_queue.append(new_order)
    
    return f"✅ **Order Placed Successfully!**\nYour order number is `#{order_num}`. You are number {order_num} in queue."


# --- 4. Render Chat History ---
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# --- 5. User Input & Bot Response Handling ---
if user_input := st.chat_input("Ask ArcherEats..."):
    
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    user_input_clean = user_input.strip().lower()
    bot_text = ""

    # 2. Check which "State" the conversation is in
    
    # STATE: Waiting for Rice (y/n)
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
            bot_text = "Please answer with 'y' or 'n'. Would you like to add rice?"

    # STATE: Waiting for Confirmation (CONFIRM/CANCEL)
    elif st.session_state.order_state == "AWAITING_CONFIRM":
        if user_input_clean == "confirm":
            bot_text = finalize_order()
            # Reset state back to normal
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        elif user_input_clean == "cancel":
            bot_text = "Order cancelled. How else can I help you?"
            # Reset state back to normal
            st.session_state.order_state = "IDLE"
            st.session_state.pending_order = None
        else:
            bot_text = "Please type CONFIRM to place your order or CANCEL to abort."

    # STATE: Normal Chatbot (IDLE)
    else:
        # Custom override for the word "order" matching your prompt example exactly
        if user_input_clean == "order":
            bot_text = "To order, please head to the lower left corner and select your meal from there! I could also order for you! Just say what you want to order and I'll do it for you (e.g., '1, Roast Pork')"
        else:
            # Send to NLTK chatbot
            response = chatbot.respond(user_input)
            
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
                elif clean_response == "IDENTIFY_ALLERGY":
                    bot_text = "Please specify what you are allergic to (e.g., 'I am allergic to eggs')."
                
                # --- NEW ORDER ROUTING ---
                elif clean_response.startswith("CREATE_ORDER_"):
                    payload = clean_response.replace("CREATE_ORDER_", "")
                    if "|" in payload:
                        count_str, food_query = payload.split("|", 1)
                        bot_text = start_web_order(count_str, food_query)
                    else:
                        bot_text = "Invalid order format."
                else:
                    bot_text = clean_response
            else:
                bot_text = "I understand the topic, but could you please rephrase your request?"

    # 3. Format the text for Streamlit Markdown (preserving line breaks)
    bot_text = str(bot_text).replace('\n', '  \n')

    # 4. Render bot message and save to history
    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_text)
