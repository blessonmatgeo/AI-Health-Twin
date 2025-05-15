import os
import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

# Streamlit UI
def main():
    st.set_page_config(page_title="Chat with your PDF", layout="wide")
    st.title("📄 AI PDF Chatbot")
    
    # Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        if "pdf_text" not in st.session_state:
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
        
        if st.button("Process PDF and Start Chat"):
            setup_chatbot()

    # If chatbot is initialized, show chat interface
    if "qa_chain" in st.session_state:
        chat_interface()

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "".join(page.get_text("text") for page in doc)
    return text.strip()

# Setup Chatbot Function
def setup_chatbot():
    with st.spinner("Processing PDF... Please wait."):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_text(st.session_state.pdf_text)

        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(text_chunks, embeddings)
        retriever = vector_store.as_retriever()
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            retriever=retriever,
            memory=memory
        )
    
    st.success("Chatbot is ready! Start asking questions.")

# Chat Interface Function
def chat_interface():
    st.subheader("💬 Chat with your PDF")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chat messages
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input
    user_input = st.chat_input("Ask something about the PDF...")
    if user_input:
        st.chat_message("user").write(user_input)

        response = st.session_state.qa_chain({"question": user_input})
        bot_reply = response["answer"]

        st.chat_message("assistant").write(bot_reply)

        # Store chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

if __name__ == "__main__":
    main()
