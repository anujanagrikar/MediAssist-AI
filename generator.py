from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(results):
    documents = results["documents"][0]
    return "\n\n".join(documents)


def generate_answer(question, context):

    prompt = f"""
    You are MediAssist AI.

    Answer ONLY using the evidence below.

    QUESTION:
    {question}

    EVIDENCE:
    {context}

    INSTRUCTIONS:
    - Give a concise answer.
    - Use bullet points if appropriate.
    - Do not copy article text verbatim.
    - If evidence is insufficient, say so.

    ANSWER:
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content