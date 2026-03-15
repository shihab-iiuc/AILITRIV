import os
import re
import tempfile

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from Backend.utils.llm import get_llm


# -----------------------------
# TEXT CLEANING
# -----------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def remove_journal_headers(text: str) -> str:
    patterns = [
        r"International Journal.*?ISSN.*?",
        r"Volume\s+\d+.*?Issue\s+\d+",
        r"www\..*?\.com",
    ]

    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    return text


# -----------------------------
# BUILD VECTOR STORE
# -----------------------------
def build_vector_store(uploaded_files):

    all_docs = []

    for uploaded_file in uploaded_files:

        suffix = os.path.splitext(uploaded_file.name)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        if suffix == ".pdf":
            loader = PyMuPDFLoader(tmp_path)

        elif suffix == ".txt":
            loader = TextLoader(tmp_path, encoding="utf-8")

        else:
            os.unlink(tmp_path)
            continue

        docs = loader.load()

        for d in docs:
            d.page_content = clean_text(remove_journal_headers(d.page_content))

        all_docs.extend(docs)

        os.unlink(tmp_path)

    # -----------------------------
    # Chunking
    # -----------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_docs)

    print(f"\n[INFO] Total chunks created: {len(chunks)}")

    # Debug preview
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n[Chunk {i}] {chunk.page_content[:400]}")

    # -----------------------------
    # Embeddings
    # -----------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store


# -----------------------------
# QUERY EXPANSION
# -----------------------------
def expand_query(question, llm):

    queries = [question]

    try:
        prompt = f"""
        Generate 2 alternative short search queries for retrieving
        relevant sections from a research paper.

        Question: {question}

        Return only comma separated phrases.
        """

        res = llm.invoke([
            SystemMessage(content="You generate search queries."),
            HumanMessage(content=prompt)
        ])

        extra = [q.strip() for q in res.content.split(",") if q.strip()]
        queries.extend(extra[:2])

    except:
        pass

    return queries


# -----------------------------
# ASK QUESTION (STREAMING)
# -----------------------------
def ask_stream(question, vector_store, chat_history=None):

    llm = get_llm()

    queries = expand_query(question, llm)

    # -----------------------------
    # Retrieval with MMR
    # -----------------------------
    all_docs = []
    seen = set()

    for q in queries:

        docs = vector_store.max_marginal_relevance_search(
            q,
            k=8,
            fetch_k=30
        )

        for d in docs:

            if d.page_content not in seen:
                all_docs.append(d)
                seen.add(d.page_content)

    context = "\n\n".join(
        clean_text(doc.page_content)
        for doc in all_docs[:20]
    )

    # -----------------------------
    # Prompt
    # -----------------------------
    system_prompt = f"""
You are an AI academic research assistant.

You are reading extracted sections of a research paper.

Tasks:
- Identify sections like Abstract, Methodology, Results, Conclusion
- Answer based only on the provided context
- If the context contains only journal metadata, say the paper content was not retrieved

Context:
{context}
"""

    messages = [SystemMessage(content=system_prompt)]

    if chat_history:
        for msg in chat_history[-6:]:

            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))

            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=question))

    # -----------------------------
    # STREAM RESPONSE
    # -----------------------------
    for chunk in llm.stream(messages):

        if chunk.content:
            yield chunk.content


# -----------------------------
# SHOW RETRIEVED CHUNKS
# -----------------------------
def get_retrieved_chunks(question, vector_store):

    results = vector_store.similarity_search_with_score(question, k=5)

    chunks = []

    for doc, score in results:

        relevance = max(0, round((1 / (1 + score)) * 100, 1))

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", None)

        chunks.append({
            "content": clean_text(doc.page_content),
            "source": os.path.basename(source) if source != "Unknown" else source,
            "page": page,
            "score": score,
            "relevance": relevance
        })

    return chunks


# -----------------------------
# VECTOR DB MANAGER
# -----------------------------
class VectorDBManager:

    def __init__(self, db_path="vectorstore/faiss_index"):

        self.db_path = db_path

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = None

        self._load()

    def _load(self):

        if os.path.exists(self.db_path):

            try:
                self.vector_store = FAISS.load_local(
                    self.db_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )

            except:
                self.vector_store = None

    def add_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        if self.vector_store is None:

            self.vector_store = FAISS.from_documents(
                chunks,
                self.embeddings
            )

        else:

            self.vector_store.add_documents(chunks)

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.vector_store.save_local(self.db_path)

    def similarity_search(self, query, k=5):

        if self.vector_store is None:

            self._load()

            if self.vector_store is None:
                return []

        return self.vector_store.similarity_search(query, k=k)
