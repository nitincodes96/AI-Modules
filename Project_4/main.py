import os
import tempfile
import shutil
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- Configuration & Initialization ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

CHROMA_PERSIST_DIR = "./chroma_db"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

st.set_page_config(page_title="Dynamic RAG Assistant", page_icon="📚", layout="wide")
st.title("📚 Dynamic Conversational RAG")

# Initialize session state for chat history and database readiness
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db_ready" not in st.session_state:
    st.session_state.db_ready = os.path.exists(CHROMA_PERSIST_DIR)

# --- Core Functions ---
def get_vector_store():
    """Initializes and returns the persistent ChromaDB connection."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)

def process_and_store_documents(uploaded_files):
    """Chunks uploaded PDFs and stores them in the persistent ChromaDB."""
    all_chunks = []
    
    for file in uploaded_files:
        # Securely save uploaded file for LangChain loader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.getbuffer())
            temp_path = temp_file.name
        
        try:
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            
            # Tag metadata for source tracking
            for doc in docs:
                doc.metadata["source"] = file.name
                
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            all_chunks.extend(splitter.split_documents(docs))
        finally:
            # Ensure cleanup even if chunking fails
            os.remove(temp_path)

    # Initialize embeddings and store directly into persistent directory
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    Chroma.from_documents(
        documents=all_chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PERSIST_DIR
    )
    return len(all_chunks)

def clear_knowledge_base():
    """Wipes the database and resets the chat."""
    if os.path.exists(CHROMA_PERSIST_DIR):
        shutil.rmtree(CHROMA_PERSIST_DIR)
    st.session_state.messages = []
    st.session_state.db_ready = False

# --- 1. Sidebar: Document Management ---
with st.sidebar:
    st.header("⚙️ Knowledge Base Setup")
    
    # Placeholder for database status
    status_placeholder = st.empty()
    if st.session_state.db_ready:
        status_placeholder.success("Database Status: **Active**")
    else:
        status_placeholder.warning("Database Status: **Empty**")

    uploaded_files = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files and st.button("🚀 Process & Index Documents", use_container_width=True):
        with st.spinner("Analyzing and chunking documents. This may take a moment..."):
            chunk_count = process_and_store_documents(uploaded_files)
            st.session_state.db_ready = True
            st.session_state.messages = [] # Clear history on new document upload
            status_placeholder.success(f"Indexed {chunk_count} chunks successfully!")
            st.rerun()

    st.divider()
    st.subheader("Danger Zone")
    if st.button("🗑️ Clear Database & Chat", type="primary", use_container_width=True):
        clear_knowledge_base()
        st.rerun()

# --- 2. Main Area: Gated Chat Interface ---
if not st.session_state.db_ready:
    # Placeholder empty state
    st.info("👋 Welcome! Please upload your PDF documents in the sidebar and click **'Process & Index Documents'** to build your local knowledge base. The chat will unlock once indexing is complete.")
    st.stop()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display source expander if sources were attached to the assistant message
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("View Document Sources"):
                for source in msg["sources"]:
                    st.markdown(f"**{source['file']}**")
                    st.caption(source['content'])

# Chat Input & Processing
if query := st.chat_input("Ask a question about your documents..."):
    
    # 1. Display and save user query
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # 2. Retrieve & Generate
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Retrieving relevant passages..."):
            vector_store = get_vector_store()
            results = vector_store.similarity_search(query, k=5)
            
            if not results:
                fallback_msg = "I couldn't find any relevant information in the uploaded documents to answer that."
                message_placeholder.markdown(fallback_msg)
                st.session_state.messages.append({"role": "assistant", "content": fallback_msg})
                st.stop()
            
            # Extract sources for UI tracking
            sources_data = [
                {"file": doc.metadata.get("source", "Unknown"), "content": doc.page_content} 
                for doc in results
            ]
            
            # Format context string for the prompt
            context = "\n\n---\n\n".join([
                f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" 
                for doc in results
            ])
            
        with st.spinner("Analyzing and drafting response..."):
            llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
            
            # Build conversation history for the LLM
            system_prompt = (
                "You are an expert AI document assistant. Your job is to answer the user's questions "
                "based STRICTLY on the provided context below. Do not use outside knowledge. "
                "If the context does not contain the answer, say 'I cannot find the answer in the provided documents.'\n\n"
                f"DOCUMENT CONTEXT:\n{context}"
            )
            
            llm_messages = [SystemMessage(content=system_prompt)]
            
            # Inject previous chat turns (limit to last 6 messages to save tokens)
            for msg in st.session_state.messages[-6:-1]: 
                if msg["role"] == "user":
                    llm_messages.append(HumanMessage(content=msg["content"]))
                else:
                    llm_messages.append(AIMessage(content=msg["content"]))
                    
            # Add current query
            llm_messages.append(HumanMessage(content=query))
            
            # Execute LLM call
            response = llm.invoke(llm_messages)
            answer = response.content
            
            # Display final answer
            message_placeholder.markdown(answer)
            
            # Display sources in UI
            with st.expander("View Document Sources"):
                for src in sources_data:
                    st.markdown(f"**{src['file']}**")
                    st.caption(src['content'])
            
            # Save to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "sources": sources_data
            })