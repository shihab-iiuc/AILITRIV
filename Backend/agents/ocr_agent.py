import base64
from langchain_core.messages import HumanMessage, SystemMessage
from Backend.utils.llm import (
    get_gemini_2_5_flash,
    get_llama_4_scout_17b,
    get_llama_4_scout
)

SYSTEM_PROMPT = """
You are an AI vision research assistant.

When analyzing an image:
1. Extract any visible text (OCR).
2. Identify if the image contains a diagram, table, chart, or architecture.
3. Explain the visual content clearly.
4. If it is a machine learning architecture, describe the components.

IMPORTANT:
- If the user asks about a concept like SVM, CNN, etc...,
  you may use your general knowledge even if the definition
  is not explicitly written in the image.
- If the image contains relevant context, combine it with your knowledge.
"""


def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def get_ocr_stream(image_bytes: bytes, query: str | None = None):
    """
    Streams OCR + vision analysis response.
    Model fallback order:
    1. Gemini 2.5 Flash
    2. Llama 4 Scout 17B
    3. Llama 3.2 / Llama Scout
    """

    if not query:
        query = "Describe this image and extract all visible text."

    # Model fallback order
    llms_to_try = [
        get_gemini_2_5_flash(),
        get_llama_4_scout_17b(),
        get_llama_4_scout(),
    ]

    base64_image = image_to_base64(image_bytes)

    # Build a highly structured multi-modal content block
    human_msg = HumanMessage(
        content=[
            {
                "type": "text", 
                "text": f"User's request regarding this image: {query}\n\nIMPORTANT INSTRUCTION: Use your vast pre-trained knowledge to answer the user's request. If they ask for the meaning, definition, or explanation of a concept shown in the image, DO NOT say 'it is not defined in the image'. Explain it using your own internal knowledge."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            },
        ]
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        human_msg
    ]

    last_exception = None

    for llm in llms_to_try:
        try:
            stream = llm.stream(messages)
            produced_output = False

            for chunk in stream:
                # Handle standard LangChain AIMessageChunk objects
                if hasattr(chunk, "content") and chunk.content:
                    produced_output = True
                    yield chunk.content
                # Handle raw string yields (sometimes happens with Groq fallbacks)
                elif isinstance(chunk, str) and chunk:
                    produced_output = True
                    yield chunk
                # Handle dict yields
                elif isinstance(chunk, dict) and chunk.get("content"):
                    produced_output = True
                    yield chunk["content"]

            # stop fallback if model worked
            if produced_output:
                return

        except Exception as e:
            last_exception = e
            continue

    # all models failed
    if last_exception:
        raise last_exception
    else:
        raise RuntimeError("All OCR/Vision models failed.")