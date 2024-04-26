import streamlit as st
from langchain.llms import OpenAI
import dotenv
from chat import create_docchain_retriever, create_retrieval_chain, reply, create_chat_history

#dotenv.load_dotenv()
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# input filepath
docchain, retriever = create_docchain_retriever('review_sample.csv')
retrieval_chain = create_retrieval_chain(docchain, retriever)
chat_history = create_chat_history()

def backend_process(user_input):
    global chat_history
    # Imagine this function processes the input and returns a result
    output, chat_history = reply(user_input, retrieval_chain, chat_history)
    return f"Processed: {output}"

st.title('Camellia Grill Review Chatbot')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')


def generate_response(input_text):
    #llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(backend_process(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What is the Camellia Grill?')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)