import streamlit as st 
from langchain_core.messages import HumanMessage, AIMessage

def get_response(user_input):
    return "Hello"

# app configuration
st.set_page_config(page_title="Talk with website",layout="wide")
st.title("Talk with website")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
    AIMessage(
        content = "Hi, I am a chatbot"
        ),
]


# app sidebar
with st.sidebar:
    st.header("Configuration")
    website_url = st.text_input("Website URL", "https://www.google.com")

# app user input and response 
user_input = st.chat_input("Ask youre question here")
if user_input is not None and user_input != "":
    # with st.chat_message("User"):
    #     st.write(user_input)
    # with st.chat_message("AI"):
    #     st.write(response)
    response = get_response(user_input)
    # chat_history.append(HumanMessage(content=user_input))
    # chat_history.append(AIMessage(content=response))
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response))

# app chat history
# with st.sidebar:
#     # st.write(chat_history)
#     st.write(st.session_state.chat_history)

# conversation history // loops through the chat history and prints out the messages in the chat history table
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)