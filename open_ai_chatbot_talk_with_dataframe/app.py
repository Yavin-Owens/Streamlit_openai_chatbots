import os
import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
from Y_secrets import openai_api_key
# Supported file formats
file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}

@st.cache(allow_output_mutation=True, ttl=7200)  # Cache for 2 hours
def load_data(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None

def main():
    st.set_page_config(page_title="LangChain: Chat with pandas DataFrame", page_icon="🦜")
    st.title("🦜 LangChain: Chat with pandas DataFrame")
    
    uploaded_file = st.file_uploader("Upload a Data file", type=list(file_formats.keys()))
    if uploaded_file:
        df = load_data(uploaded_file)

    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.get("messages", []):
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="What is this data about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            return

        llm = ChatOpenAI(api_key=openai_api_key)
        pandas_df_agent = create_pandas_dataframe_agent(
            llm=llm,
            dataframe=df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
        )

        response = pandas_df_agent.run(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

if __name__ == '__main__':
    main()
