import faiss
import numpy as np
import pandas as pd
import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from sentence_transformers import SentenceTransformer
import uvicorn
from openai import AsyncOpenAI 
import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
try:
    CSV_PATH = "data/perfumes.csv"
    EMBEDDINGS_PATH = "data/embeddings.npy"
    INDEX_PATH = "data/index.faiss"
except Exception as e:
    raise RuntimeError("Failed to load paths. Ensure the files exist.") from e

df = pd.read_csv(CSV_PATH)
index = faiss.read_index(INDEX_PATH)
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
id_map = df.set_index("id").to_dict('index')


client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

app = FastAPI(title="Perfume Finder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions: Dict[str, dict] = {}

class ChatMessage(BaseModel):
    content: str
    session_id: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

def initialize_session(session_id: str):
    sessions[session_id] = {
        "messages": [
            {
                "role": "system",
                "content": """You are a sophisticated perfume consultant conducting a personalized fragrance consultation. Your goal is to gather user preferences through exactly 3-4 conversational turns before creating their scent profile.

                    CONVERSATION STRUCTURE:
                    1. Start with a warm greeting and ask about their preferred scent families/notes
                    2. Ask about the mood, feeling, or impression they want the fragrance to convey
                    3. Ask about occasion, season, or when they plan to wear it
                    4. Summarize their preferences and ask for confirmation.
                    5. create the final query JSON, do not show the user the JSON, end the conversation with a confirmation message.

                    GUIDELINES:
                    - Ask ONE question at a time
                    - Wait for the user's response before moving to the next question, for each question you ask you must take the users answer into account. The previous chat history is available to you and must contain the message by user as the last message.
                    - Do NOT ask for more than 3-4 pieces of information
                    - Be conversational, warm, and professional. Do not include cues or instructions in your responses, only dialogues.
                    - Do NOT create the JSON until you have gathered all 3 pieces of information.
                    - Do NOT hallucinate user responses - only respond to what they actually say.
                    - Do NOT conclude the conversation until you have all necessary information as well as the JSON and the confirmation of user at the final turn.
                    - Keep responses concise (2-3 sentences max per response)

                    FINAL STEP: After gathering all preferences, create this exact JSON format:
                    {
                    "query": "[detailed summary combining scent notes, mood/feeling, and occasion/season]"
                    }
                    Start the conversation now with a greeting."""
            }
        ],
        "completed": False,
        "step": 0
    }

@app.post("/start")
async def start_chat():
    session_id = str(uuid.uuid4())
    initialize_session(session_id)
    
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=sessions[session_id]["messages"],
            temperature=0.7
        )
        initial_message = response.choices[0].message.content
        sessions[session_id]["messages"].append({"role": "assistant", "content": initial_message})
        
        return {
            "session_id": session_id,
            "initial_message": initial_message
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {str(e)}"
        )

@app.post("/chat")
async def chat(message: ChatMessage): 
    session = sessions.get(message.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session["completed"]:
        return {"response": "Chat completed. Use /search with extracted parameters."}
    
    session["messages"].append({"role": "user", "content": message.content})
    session["step"] += 1

    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=session["messages"],
            temperature=0.7
        )
        res = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {str(e)}"
        )
    
    session["messages"].append({"role": "assistant", "content": res})

    extracted_json = extract_json(res)
    if extracted_json and "query" in extracted_json:
        session["completed"] = True
        session["query"] = extracted_json["query"]
        res += "\n\n[QUERY COMPLETE]"
    
    return {"response": res}

@app.post("/search")
async def search_perfumes(request: SearchRequest): 
    query_vector = model.encode([request.query])
    faiss.normalize_L2(query_vector)

    distances, indices = index.search(query_vector, request.top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        idx_int = int(idx)
        perfume = id_map.get(idx_int)
        if not perfume:
            continue
        
        results.append({
            'id': idx_int,
            'Name': str(perfume['Name']),
            'Brand': str(perfume['Brand']),
            'Description': str(perfume['Description']),
            'Notes': str(perfume['Clean_Notes']),
            'image_url': str(perfume['Image URL']),
            'Distance': float(dist)
        })

        if len(results) >= request.top_k:
            break

    return {'results': results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
