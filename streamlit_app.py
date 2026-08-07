# =====================================================================
#  CBEMC-5 X40
#  Final Project - ArcherEats Chatbot
#  Members:
#    - CHUNG, Josh Matthew A.
#    - NOMOTO, Shintaroh
#    - RICALDE, Jhobert Alfonso V.
#    - VASCO, Victor Gerald N.
# =====================================================================

from datetime import datetime
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
    get_food_allergens_list,
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
)

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="ArcherEats", page_icon="🎯", layout="centered")

# --- Custom Styling (Header, Cards, Allergen Pills, Bottom Tabs) ---
st.markdown(
    """
<style>
    /* Top Dark Green Header Bar */
    .main-header {
        background-color: #1e5a36;
        color: white;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-header .sub-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 13px;
        font-weight: 300;
        opacity: 0.9;
    }
    .main-header .main-title {
        font-family: 'Georgia', serif;
        font-size: 30px;
        font-weight: bold;
        margin-top: 2px;
    }

    /* Custom Menu Cards - Dark Mode Compatible */
    .menu-card {
        background-color: var(--secondary-background-color); 
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-top: 5px solid #1e5a36;
    }
    .item-title { 
        font-size: 22px; 
        font-weight: bold; 
        font-family: 'Georgia', serif; 
        color: var(--text-color); 
        margin-bottom: 6px; 
    }
    .item-desc { 
        font-size: 14px; 
        color: var(--text-color); 
        opacity: 0.75; 
        margin-bottom: 14px; 
        line-height: 1.4;
    }
    .item-stats { 
        font-size: 14px; 
        color: var(--text-color);
        opacity: 0.6;
        margin-bottom: 14px; 
        display: flex;
        gap: 12px;
    }
    .item-price { color: #4caf50; font-weight: bold; font-size: 16px; } 
    .item-cal { color: var(--text-color); opacity: 0.9; font-weight: bold; font-size: 16px; }
    
    /* Allergen Pills */
    .allergen-container { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
    .allergen-label { font-size: 12px; color: var(--text-color); opacity: 0.6; margin-right: 4px; }
    .pill {
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    .pill-Gluten { background-color: #fef0c7; color: #b58509; }
    .pill-Milk { background-color: #e0f2fe; color: #026aa2; }
    .pill-Fish { background-color: #e0f2fe; color: #0284c7; }
    .pill-Seafood { background-color: #ffe4e6; color: #e11d48; }
    .pill-Celery { background-color: #dcfce7; color: #166534; }
    .pill-Mustard { background-color: #ffedd5; color: #c2410c; }
    .pill-Soybean { background-color: #dcfce7; color: #15803d; }
    .pill-Egg, .pill-Eggs { background-color: #fef0c7; color: #b58509; }
    .pill-Chicken { background-color: #fef3c7; color: #92400e; }
    .pill-Sulphite { background-color: #f3e8ff; color: #6b21a8; }
    .pill-Crustacean, .pill-Crustaceans { background-color: #ffe4e6; color: #9f1239; }
    .pill-default { 
        background-color: var(--background-color); 
        color: var(--text-color); 
        border: 1px solid var(--text-color); 
    }

    /* Fix Tabs to Bottom Navigation Bar */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        bottom: 0px;
        left: 0px;
        right: 0px;
        background-color: var(--background-color); 
        padding: 6px 0px 12px 0px;
        z-index: 999;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        border-top: 1px solid var(--secondary-background-color);
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        justify-content: center;
        padding-top: 6px;
        padding-bottom: 6px;
    }

    .stChatFloatingInputContainer {
        bottom: 65px !important;
        background-color: transparent;
    }

    .block-container {
        padding-bottom: 110px;
    }
</style>

<div class="main-header">
    <span style="font-size: 28px;">🎯</span>
    <div>
        <div class="sub-text">CBEMC-5 ChatBot by CHUNG-NOMOTO-RICALDE-VASCO</div>
        <div class="main-title">ArcherEats</div>
    </div>
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


# --- Tabs Navigation ---
tab_menu, tab_cart, tab_chat, tab_profile = st.tabs(
    ["📋 Menu", "🛍️ Cart", "💬 Chat", "👤 Profile"]
)


# =====================================================================
# TAB 1: MENU PAGE
# =====================================================================
with tab_menu:
    st.markdown(
        "<h1 style='font-family: Georgia, serif; margin-bottom: 0px;'>Today's Menu</h1>",
        unsafe_allow_html=True,
    )

    current_date = datetime.now().strftime("%A, %B %d").replace(" 0", " ")
    st.markdown(
        f"<p style='color: #888; font-size: 15px; margin-bottom: 22px;'>{current_date}</p>",
        unsafe_allow_html=True,
    )

    for item in FOOD_DATABASE:
        if not item.get("isAvailable", True):
            continue

        allergens = item.get("allergens", [])
        allergens_html = ""
        for a in allergens:
            pill_class = f"pill-{a.capitalize()}"
            allergens_html += f'<span class="pill {pill_class}">{a.capitalize()}</span>'

        if not allergens_html:
            allergens_html = '<span class="pill pill-default">None</span>'

        desc = item.get("description", "")
        if not desc:
            desc = "Delicious meal prepared fresh daily at the UH Cafeteria."

        kcal_val = item.get("kcal", item.get("calories", "N/A"))

        card_html = f"""
        <div class="menu-card">
            <div class="item-title">{item['name'].title()}</div>
            <div class="item-desc">{desc}</div>
            <div class="item-stats">
                <span>Price <span class="item-price">₱{item['price']}</span></span>
                <span style="color: #ddd;">|</span>
                <span>Calories <span class="item-cal">{kcal_val} kcal</span></span>
            </div>
            <div class="allergen-container">
                <span class="allergen-label">Contains:</span>
                {allergens_html}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


# =====================================================================
# TAB 2: CART & QUEUE
# =====================================================================
with tab_cart:
    st.markdown("### 🛍️ Current Orders Queue")
    if not orders_queue:
        st.info("No active orders in queue right now. Use the Chat to place an order!")
    else:
        for order in orders_queue:
            rice_text = "with rice" if order["with_rice"] else "ala carte"
            st.success(
                f"**Order #{order['order_number']}** — "
                f"{order['count']}x {order['food_name']} ({rice_text}) | ID: `{order['id_number']}`"
            )


# =====================================================================
# TAB 3: CHATBOT INTERFACE
# =====================================================================
with tab_chat:
    # --- Render Conversation History ---
    for msg in st.session_state.messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # --- Chat Input Processing ---
    if user_input := st.chat_input("Ask ArcherEats..."):
        user_input = user_input.replace("\n", "").replace("\r", "").strip()
        
        # 1. Save user message to state (Do NOT draw it yet)
        st.session_state.messages.append({"role": "user", "content": user_input})

        user_input_clean = user_input.strip().lower()
        bot_text = ""

        # 2. Active Order State Machine
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

        # 3. Main Chatbot Routing 
        else:
            response = chatbot.respond(user_input)

            if response:
                clean_response = response.strip()

                if clean_response == "FETCH_MENU":
                    bot_text = get_available_menu()

                elif clean_response.startswith("ALLERGEN_LIST_"):
                    food = clean_response.replace("ALLERGEN_LIST_", "")
                    bot_text, st.session_state.last_discussed_food = (
                        get_food_allergens_list(
                            food, st.session_state.last_discussed_food
                        )
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

                elif clean_response.startswith("ALLERGEN_"):
                    allergen = clean_response.replace("ALLERGEN_", "")
                    bot_text = get_allergen_safe_menu(
                        allergen, st.session_state.user_allergies
                    )

                elif clean_response == "FETCH_VEGETARIAN":
                    bot_text = get_vegetarian_menu()
                elif clean_response == "DISPLAY_QUEUE":
                    bot_text = get_queue_display()
                elif clean_response.startswith("MEAL_"):
                    meal = clean_response.replace("MEAL_", "")
                    bot_text = get_meal_type_menu(meal)
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
                    bot_text = "Please state your allergy (e.g., 'I am allergic to eggs')."

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

        # 4. Save bot message to state and Refresh Page
        bot_text = str(bot_text).replace("\n", "  \n")
        st.session_state.messages.append({"role": "assistant", "content": bot_text})
        
        # This redraws the whole page perfectly so the new messages flow above the chat bar
        st.rerun()


# =====================================================================
# TAB 4: PROFILE
# =====================================================================
with tab_profile:
    st.markdown("### 👤 User Profile")
    st.write(f"**ID Number:** `{USER_ID_NUMBER}`")

    registered = st.session_state.user_allergies
    if registered:
        allergies_formatted = ", ".join([a.capitalize() for a in registered])
        st.write(f"**Registered Allergies:** {allergies_formatted}")
    else:
        st.write("**Registered Allergies:** None declared")

    st.write("**Account Type:** Student / Customer")
