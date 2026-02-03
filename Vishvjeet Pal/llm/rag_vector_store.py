from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm.rag_data import get_all_documents

embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_rag_index(db, faiss_file: str ="faiss_index"):
    docs=get_all_documents(db)

    splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs=splitter.split_documents(docs)

    vector_store=FAISS.from_documents(split_docs, embedding_model)
    vector_store.save_local(faiss_file)
    return vector_store

