import streamlit as st
import ChatBot  # Imports your database and functions

st.set_page_config(page_title="ArcherEats", page_icon="🍔")
st.title("🍔 ArcherEats ChatBot")

# Initialize the chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm ArcherEats. How can I help you?"}
    ]

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Web-safe Order Processing (Bypasses the terminal y/n input for rice)
def web_process_order(count_str, food_query):
    try:
        count = int(count_str)
        if count <= 0:
            return "Order quantity must be at least 1."
    except ValueError:
        return "Invalid order quantity."

    food_query_clean = food_query.strip().upper()
    selected_item = None

    for item in ChatBot.FOOD_DATABASE:
        if food_query_clean in item["name"].upper():
            selected_item = item
            break

    if not selected_item:
        return f"Sorry, we couldn't find '{food_query.title()}' on our menu."

    if not selected_item.get("isAvailable"):
        return f"Sorry, {selected_item['name']} is currently not available."

    order_num = len(ChatBot.orders_queue) + 1
    
    # Process order immediately without asking for rice to avoid terminal freeze
    new_order = {
        "id_number": ChatBot.USER_ID_NUMBER,
        "food_name": selected_item["name"],
        "count": count,
        "with_rice": False, 
        "order_number": order_num,
    }
    ChatBot.orders_queue.append(new_order)
    
    unit_price = selected_item["price"]
    total = unit_price * count
    
    return f"✅ **Order confirmed!**\n\nYour order number is #{order_num}. You are number {order_num} in queue.\nTotal: ₱{total}."

# Main Chat Input
if user_input := st.chat_input("Type your message here..."):
    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get raw response from NLTK
    response = ChatBot.chatbot.respond(user_input)
    bot_response = "I understand the general topic, but could you please rephrase your request?"

    if response:
        clean_response = response.strip()

        # Route the specific tags to your ChatBot functions
        if clean_response == "FETCH_MENU":
            bot_response = ChatBot.get_available_menu()
        elif clean_response == "FETCH_VEGETARIAN":
            bot_response = ChatBot.get_vegetarian_menu()
        elif clean_response.startswith("CATEGORY_"):
            category = clean_response.replace("CATEGORY_", "")
            bot_response = ChatBot.get_category_menu(category)
        elif clean_response.startswith("FOOD_WITH_ALLERGEN_"):
            allergen = clean_response.replace("FOOD_WITH_ALLERGEN_", "")
            bot_response = ChatBot.get_food_with_allergen(allergen)
        elif clean_response.startswith("WITHOUT_"):
            category = clean_response.replace("WITHOUT_", "")
            bot_response = ChatBot.get_category_removed_menu(category)
        elif clean_response.startswith("SUGGEST_CATEGORY_"):
            category = clean_response.replace("SUGGEST_CATEGORY_", "")
            bot_response = ChatBot.get_food_suggestion("category", category)
        elif clean_response.startswith("ALLERGEN_"):
            allergen = clean_response.replace("ALLERGEN_", "")
            bot_response = ChatBot.get_allergen_safe_menu(allergen)
        elif clean_response.startswith("SUGGEST_BUDGET_"):
            amount = clean_response.replace("SUGGEST_BUDGET_", "")
            bot_response = ChatBot.get_food_suggestion("budget", amount)
        elif clean_response == "SUGGEST_HIGHCAL":
            bot_response = ChatBot.get_food_suggestion("high_cal")
        elif clean_response == "SUGGEST_LOWCAL":
            bot_response = ChatBot.get_food_suggestion("low_cal")
        elif clean_response == "SUGGEST_GENERAL":
            bot_response = ChatBot.get_food_suggestion("general")
        elif clean_response.startswith("SUGGEST_ALLERGEN_"):
            allergen = clean_response.replace("SUGGEST_ALLERGEN_", "")
            bot_response = ChatBot.get_food_suggestion("allergen", allergen)
        elif clean_response == "SUGGEST_CHEAPEST":
            bot_response = ChatBot.get_food_suggestion("cheapest")
        elif clean_response == "SUGGEST_LOWESTCAL":
            bot_response = ChatBot.get_food_suggestion("lowest_cal")
        elif clean_response == "SUGGEST_FILLING":
            bot_response = ChatBot.get_food_suggestion("filling")
        elif clean_response == "SUGGEST_VEGETARIAN":
            bot_response = ChatBot.get_food_suggestion("vegetarian")
        elif clean_response.startswith("INFO_"):
            food = clean_response.replace("INFO_", "")
            bot_response = ChatBot.get_food_description(food)
        elif clean_response.startswith("PRICE_"):
            food = clean_response.replace("PRICE_", "")
            bot_response = ChatBot.get_food_price(food)
        elif clean_response.startswith("CALORIES_"):
            food = clean_response.replace("CALORIES_", "")
            bot_response = ChatBot.get_food_calories(food)
        elif clean_response.startswith("CHECK_ALLERGEN_"):
            payload = clean_response.replace("CHECK_ALLERGEN_", "")
            if "|" in payload:
                food_item, allergen = payload.split("|", 1)
                bot_response = ChatBot.check_item_allergen(food_item, allergen)
            else:
                bot_response = "Could not process allergen check query."
        elif clean_response.startswith("MEAL_"):
            meal = clean_response.replace("MEAL_", "")
            bot_response = ChatBot.get_meal_type_menu(meal)
        elif clean_response.startswith("CREATE_ORDER_"):
            payload = clean_response.replace("CREATE_ORDER_", "")
            if "|" in payload:
                count_str, food_query = payload.split("|", 1)
                bot_response = web_process_order(count_str, food_query)
        elif clean_response == "IDENTIFY_ALLERGY":
            bot_response = "Please tell me exactly what you are allergic to (e.g., 'I am allergic to eggs')."
        else:
            bot_response = clean_response

    # Display Bot Message
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
