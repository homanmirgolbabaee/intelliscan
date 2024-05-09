import time
import streamlit as st
from llama_index.core import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    set_global_service_context,
    Settings
)
from llama_index.llms.ollama import Ollama
import openai

def create_index(api_key):
    # Set API key for OpenAI
    openai.api_key = api_key
    Settings.llm = Ollama(model="llama2", request_timeout=120.0)

    documents = SimpleDirectoryReader(input_dir='data', required_exts=[".pdf", ".csv"]).load_data()
    service_context = ServiceContext.from_defaults(embed_model="local:BAAI/bge-small-en-v1.5", chunk_size=300)
    set_global_service_context(service_context)
    nodes = service_context.node_parser.get_nodes_from_documents(documents)
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    return index.as_query_engine()

def typewriter_effect(text, delay=0.05):
    for char in text:
        time.sleep(delay)
        yield char

def query_index(api_key, query_engine, query):
    # Set API key each time before querying
    openai.api_key = api_key
    return query_engine.query(query)

def render():
    st.title("Document Query Chatbot")

    # Input API key via sidebar
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    # Button for creating index in the sidebar
    if st.sidebar.button("Create Index"):
        with st.spinner("Creating index..."):
            st.session_state.query_engine = create_index(api_key)
            st.sidebar.success("Index created successfully!")
            
            
    # Informational message for users
    st.info("Hint: Ask about today's patients report?")
    
    
    # Chat input for querying
    user_input = st.chat_input("Enter your query")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        if st.session_state.query_engine:
            with st.spinner("Querying..."):
                response = query_index(api_key, st.session_state.query_engine, user_input)
                if response and hasattr(response, 'response'):
                    message_container = st.empty()
                    stream = typewriter_effect(response.response)
                    message_container.write_stream(stream)
                else:
                    st.error("No response found or incorrect response format.")
        else:
            st.error("Please create the index first and ensure your API key is valid.")

