import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# Setup
# -----------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖"
)

st.title("🤖 AI Customer Support Agent")


# -----------------------------
# Mock Database
# -----------------------------
ORDERS = {
    "ORD-123": {
        "product": "Wireless Headphones",
        "status": "shipped",
        "policy": "30-day return allowed"
    },

    "ORD-456": {
        "product": "Keyboard",
        "status": "delivered",
        "policy": "final sale - no returns"
    },

    "ORD-789": {
        "product": "Mouse",
        "status": "processing",
        "policy": "30-day return allowed"
    }
}


# -----------------------------
# Tool Function
# -----------------------------
def get_order_details(order_id):
    order = ORDERS.get(order_id)

    if order:
        return json.dumps({
            "order_id": order_id,
            **order
        })

    return json.dumps({
        "error": "Order not found"
    })


# -----------------------------
# Tool Definition
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Get order status, product and return policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID, for example ORD-123"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a customer support AI for an online store.

Follow these rules:

1. Never guess or invent order information.
2. If the customer provides an order ID, use the get_order_details tool.
3. Final-sale orders cannot be returned.
4. Orders with a 30-day return policy can be returned.
5. If an order is not found, ask the customer to verify their order ID.
6. If you cannot solve the customer's problem, escalate it to a human.
7. Be friendly and concise.

Always return valid JSON in exactly this format:

{
    "customer_message": "Your response to the customer",
    "action": "none"
}

The action must be exactly one of:

- none
- issue_refund
- escalate_to_human
- awaiting_information

Do not use markdown.
Do not add ```json.
Do not add any text outside the JSON.
"""


# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Ask about your order...")


if prompt:

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # -----------------------------
    # Prepare Messages
    # -----------------------------
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)


    # -----------------------------
    # First AI Call
    # -----------------------------
    with st.spinner("Thinking..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        assistant_message = response.choices[0].message


        # -----------------------------
        # Check Tool Call
        # -----------------------------
        if assistant_message.tool_calls:

            tool_call = assistant_message.tool_calls[0]

            # Get arguments selected by AI
            arguments = json.loads(
                tool_call.function.arguments
            )

            order_id = arguments["order_id"]


            # Execute Python tool
            tool_result = get_order_details(order_id)


            # Add AI's tool request
            messages.append(assistant_message)


            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })


            # -----------------------------
            # Second AI Call
            # -----------------------------
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            answer = final_response.choices[0].message.content

        else:

            # AI answered without using a tool
            answer = assistant_message.content


    # -----------------------------
    # Parse JSON Response
    # -----------------------------
    try:

        result = json.loads(answer)

        customer_message = result.get(
            "customer_message",
            "Sorry, I couldn't process your request."
        )

        action = result.get(
            "action",
            "none"
        )

    except json.JSONDecodeError:

        # Fallback if AI doesn't return JSON
        customer_message = answer
        action = "none"


    # -----------------------------
    # Display Final Response
    # -----------------------------
    with st.chat_message("assistant"):
        st.write(customer_message)
        if action != "none":
            st.caption(f"Action: {action}")


    # -----------------------------
    # Save Only Customer Message
    # -----------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": customer_message
    })