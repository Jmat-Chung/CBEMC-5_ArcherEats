import streamlit as st
# Import chatbot and helpers from your ChatBot.py
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

# Page configuration & DLSU Green Theme
st.set_page_config(page_title="ArcherBot", page_icon="🏹", layout="centered")

# Custom CSS for DLSU Green Header
st.markdown("""
    <style>
    .main-header {
        background-color: #1e5a36;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        font-family: 'Georgia', serif;
        color: white;
        margin: 0;
    }
    .main-header p {
        margin: 0;
        opacity: 0.8;
    }
    </style>
    <div class="main-header">
        <p>Powered by DLSU Dining</p>
        <h1>ArcherBot</h1>
    </div>
""", unsafe_allow_html=True)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm ArcherBot 🤖 Ask me anything about today's menu, prices, or allergens!"}
    ]

# Display Existing Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Chat Input Field
if user_input := st.chat_input("Ask ArcherBot..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process response via NLTK Chatbot
    raw_response = chatbot.respond(user_input)
    clean_response = raw_response.strip() if raw_response else ""

    # Parse Directives
    if clean_response == "FETCH_MENU":
        bot_text = get_available_menu()
    elif clean_response == "FETCH_VEGETARIAN":
        bot_text = get_vegetarian_menu()
    elif clean_response.startswith("CATEGORY_"):
        bot_text = get_category_menu(clean_response.replace("CATEGORY_", ""))
    elif clean_response.startswith("WITHOUT_"):
        bot_text = get_category_removed_menu(clean_response.replace("WITHOUT_", ""))
    elif clean_response.startswith("MEAL_"):
        bot_text = get_meal_type_menu(clean_response.replace("MEAL_", ""))
    elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
        bot_text = get_food_with_allergen(clean_response.replace("FOOD_WITH_ALLERGEN_", ""))
    elif clean_response.startswith("ALLERGEN_"):
        bot_text = get_allergen_safe_menu(clean_response.replace("ALLERGEN_", ""))
    elif clean_response.startswith("SUGGEST_CATEGORY_"):
        bot_text = get_food_suggestion("category", clean_response.replace("SUGGEST_CATEGORY_", ""))
    elif clean_response.startswith("SUGGEST_BUDGET_"):
        bot_text = get_food_suggestion("budget", clean_response.replace("SUGGEST_BUDGET_", ""))
    elif clean_response == "SUGGEST_HIGHCAL":
        bot_text = get_food_suggestion("high_cal")
    elif clean_response == "SUGGEST_LOWCAL":
        bot_text = get_food_suggestion("low_cal")
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
            item_name, allergen = payload.split("|", 1)
            bot_text = check_item_allergen(item_name, allergen)
        else:
            bot_text = "Could not check allergen."
    elif clean_response.startswith("CREATE_ORDER_"):
        payload = clean_response.replace("CREATE_ORDER_", "")
        if "|" in payload:
            count_str, food_query = payload.split("|", 1)
            selected_item = next((item for item in FOOD_DATABASE if food_query.upper() in item["name"].upper()), None)
            if selected_item and selected_item.get("isAvailable"):
                order_num = len(orders_queue) + 1
                orders_queue.append({
                    "id_number": USER_ID_NUMBER,
                    "food_name": selected_item["name"],
                    "count": int(count_str),
                    "with_rice": True,
                    "order_number": order_num,
                })
                bot_text = f"✅ **Order Placed!**\n• {count_str}x {selected_item['name']} (with rice)\n• Total: ₱{(selected_item['price']+15)*int(count_str)}\n• Order #{order_num}"
            else:
                bot_text = "Item not found or unavailable."
        else:
            bot_text = "Invalid order."
    elif clean_response:
        bot_text = clean_response
    else:
        bot_text = "I'm sorry, could you please rephrase your request?"

    # Display & store bot response
    with st.chat_message("assistant"):
        st.markdown(bot_text)
    st.session_state.messages.append({"role": "assistant", "content": bot_text})