from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from langchain.chains.combine_documents import create_stuff_documents_chain

from typing import Dict
from langchain_core.runnables import RunnablePassthrough


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


def create_document_chain(file_path):
    
    # Load data
    loader = CSVLoader(file_path=file_path)
    data = loader.load()

    # Split data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    # Store vectorized data in a vector db
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

    chat = ChatOpenAI(model="gpt-3.5-turbo-1106")

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

    return document_chain


def create_retrieval_chain(document_chain, retriever):
    retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
    ).assign(
        answer=document_chain,
    )
    
    return retrieval_chain