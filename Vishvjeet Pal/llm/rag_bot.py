import os
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from llm.rag_vector_store import build_rag_index 
from core.utils.database import SessionLocal
from core.utils.config import settings

embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def load_rag_bot(faiss_file: str = "faiss_index"):
    if not os.path.exists(f"{faiss_file}/index.faiss"):
        print("FAISS index not found. Bulding it now...")
        db=SessionLocal()
        vector_store=build_rag_index(db, faiss_file)
        db.close()

    else:
        vector_store=FAISS.load_local(
            faiss_file,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    retriever=vector_store.as_retriever(k=3)

    llm=ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=200,
        api_key=os.getenv(settings.GROQ_API_KEY)
    )

    prompt=ChatPromptTemplate.from_template(
        """
You are a helpful assistant of a Task Tracker System.
Use ONLY the provided context to answer the question.
Do not provide additional information. Just answer the question.
If the answer is not in the context, say "Sorry I don't Know."

Context:
{context}

Question:
{question}
        """
    )

    rag_chain=(
        {
            "context":retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever
