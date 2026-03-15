# AILITRIV: AI-Powered Academic Research Assistant with Web Search, Document RAG, OCR Vision

### Project Description:  
AILITRIV is an advanced tool designed to accelerate literature reviews and academic research by leveraging the latest in AI technologies. The system utilizes **Large Language Models (LLMs)** and **Streamlit** to offer an intuitive, premium dark-themed interface. It integrates **web search grounding**, **Retrieval-Augmented Generation (RAG)** for local documents, and **Optical Character Recognition (OCR)** to create a comprehensive research companion. The tool not only finds online literature but also lets users chat directly with their PDFs and extract insights from complex scientific diagrams, providing a seamless and highly productive research experience.

#### Key Features:
1. **Web Search Agent**:  
   Users can ask general research questions, and the agent scrapes the internet to ground its answers in real, up-to-date information and academic contexts.

2. **Document Q&A (RAG Agent)**:  
   Users can upload research papers (PDF, TXT). The system chunks and embeds the text into a local **FAISS vector database**, allowing the AI to answer highly specific questions based purely on the provided text.

3. **Vision & Layout Extraction (OCR Agent)**:  
   Upload images of machine learning architectures, data tables, or charts. The multimodal AI extracts visible text and explains the visual content using its vast pre-trained knowledge base.

4. **Multi-Model Fallback System**:  
   - Built with deep resilience using a custom fallback architecture.
   - Leverages **Gemini 2.5 Flash**, **Llama 3.3 70B**, **Llama 4 Scout Vision**, and **GPT-OSS-120B** to ensure the system gracefully degrades and succeeds even if primary APIs rate-limit or fail.

#### Project Structure:
```text
AILITRIV/
├── .env                     # Environment variables (API Keys)
├── .gitignore               # Git ignore file
├── Backend/                 # Core backend logic
│   ├── agents/              # Specialized AI agents
│   │   ├── ocr_agent.py     # Image and screenshot extraction
│   │   ├── rag_agent.py     # Local PDF document indexing
│   │   ├── search_agent.py  # Internet search & grounding
│   │   └── __pycache__/     # Python bytecode cache
│   ├── utils/               # Utilities & configs
│   │   ├── llm.py           # LLM configurations (Gemini, Llama, Groq)
│   │   ├── styles.py        # Streamlit premium styling definitions
│   │   └── __pycache__/     # Python bytecode cache
│   └── requirements.txt     # Python dependencies
├── Frontend/                # Streamlit user interface
│   ├── .streamlit/          # Theme configuration
│   └── app.py               # Main UI application entry point
├── data/                    # Data storage for uploads or temporary files
├── vectorstore/             # Local database storage
│   └── faiss_index/         # Indexed semantic vectors for RAG
└── README.md                # Documentation
```

#### Setup Instructions:
1. **API Key Configuration**:  
   - Obtain an **API Key** from the [GROQ Console](https://console.groq.com/keys) and the [Google AI Studio](https://aistudio.google.com/app/apikey).  
   - Create a `.env` file in the root directory (`LR/LR/.env`).
   - Add your keys in the following format:
     ```env
     GROQ_API_KEY=your_groq_key_here
     GEMINI_API_KEY=your_gemini_key_here
     ```

2. **Dependency Installation**:  
   Install the required Python dependencies by running:  
   ```bash
   pip install -r Backend/requirements.txt
   ```

3. **Run the Application**:  
   Launch the Streamlit app from the root project folder with the following command:  
   ```bash
   python -m streamlit run Frontend/app.py
   ```

#### Use Case:  
This tool serves as an invaluable resource for students, academics, and researchers, enabling them to comprehend dense academic papers with minimal effort. By automating literature web searches, document parsing, context-aware Q&A, and visual chart extraction, researchers can synthesize findings faster and focus entirely on innovation and writing.

# Video Tutotrial Link: https://youtu.be/ucK6pZ9THSw
# LangSmith Tracer

LR ID:7c4112c1-b2fa-44b0-9052-be37885925df
Link: https://smith.langchain.com/o/e3c87f62-84cf-4978-bfdc-88b1cde523fa/projects/p/7c4112c1-b2fa-44b0-9052-be37885925df?timeModel=%7B%22duration%22%3A%221d%22%7D
OpenAI(OSS 120B): https://smith.langchain.com/public/4533446c-6cb2-4949-89fe-840b425281c5/r
GROQ: https://smith.langchain.com/public/33baa6ef-39dd-4553-b2d3-bcb8086972ac/r
GoogleGenAI:https://smith.langchain.com/public/04192dbb-bb79-4ac5-82b4-10d786bd6bfc/r
