import streamlit as st
import requests
import re
import json
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

COLORS = {
    'background1':"#04000B", 
    'sidebar_bg': "#7A587A",
    'user_textbox': '#FFF7F3',         
    'user_text': '#9283a9',         
    'perfumer_textbox': '#EDDFE0',    
    'perfumer_text': '#A87676',       
    'sidebar_text': '#F0EBE3',
    "title": "#e5eaf5",
    "markdown": "#c7d0e0",
    'button_bg': '#F49BAB',            
    'button_text': '#533B4D',    
    'flashcard_bg': '#FEF3E2',         
    'flashcard_text': '#441752',       
    'accent': '#FFD66B'              
}

st.set_page_config(page_title="The Perfumer's Atelier", page_icon="data/assets/perfume.png", initial_sidebar_state="collapsed")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def clear_session():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

st.sidebar.image("data/assets/coco.jpg", width=160)
st.sidebar.title("Perfume Explorer")
page = st.sidebar.radio("Choose", ["Find My Fragrance", "Perfume DNA (UMAP)"])
if st.sidebar.button("🔄 Restart Consultation", key="restart_top", type="primary"):
    clear_session()

API_BASE = os.getenv('BACKEND_URL')

def chatbot_ui():
    st.markdown("## The Perfumer's Atelier")
    st.markdown("Discover your perfect fragrance through our AI-powered consultation")
    
    if "session_id" not in st.session_state:
        try:
            resp = requests.post(f"{API_BASE}/start")
            response_data = resp.json()
            st.session_state.session_id = response_data["session_id"]
            st.session_state.chat_history = [{"role": "assistant", "content": response_data["initial_message"]}]
            st.session_state.completed = False
            st.session_state.final_query = None
            st.session_state.show_results = False
        except Exception as e:
            st.error(f"Failed to initialize chat: {str(e)}")
            return

    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant" and not msg.get("content").startswith("[QUERY COMPLETE]"):
            st.markdown(f"<div class='perfumer-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    
    if not st.session_state.completed:
        with st.form(key='chat_form'):
            user_input = st.text_input("Your response:", key="user_input", placeholder="Type your response here...")
            col1, col2 = st.columns([4, 1])
            with col1:
                submit_button = st.form_submit_button("Send")
            with col2:
                if st.form_submit_button("🔄 Restart"):
                    clear_session()
            
            if submit_button and user_input.strip():
                try:
                    payload = {"content": user_input, "session_id": st.session_state.session_id}
                    res = requests.post(f"{API_BASE}/chat", json=payload)
                    if res.status_code == 200:
                        response = res.json()["response"]
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        if "[QUERY COMPLETE]" in response:
                            match = re.search(r"\{.*\}", response, re.DOTALL)
                            if match:
                                try:
                                    extracted = json.loads(match.group())
                                    st.session_state.final_query = extracted["query"]
                                    st.session_state.completed = True
                                except json.JSONDecodeError:
                                    st.error("Failed to parse preferences")
                        st.rerun()
                    else:
                        st.error("Error communicating with the fragrance consultant")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

    elif not st.session_state.show_results:
        st.success("🎉 Your Fragrance Profile is Complete!")
        st.markdown(f"""
            <div style="background-color: {COLORS['flashcard_bg']}; 
                      color: {COLORS['flashcard_text']}; 
                      padding: 1.5rem; 
                      border-radius: 12px; 
                      margin: 1rem 0;
                      border-left: 4px solid {COLORS['accent']};">
                <strong>Your Personalized Scent Profile:</strong><br>
                "{st.session_state.final_query}"
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🌟 Show Me My Signature Scents!", key="show_results"):
                st.session_state.show_results = True
                st.rerun()
        with col2:
            if st.button("🔄 Start Over", key="restart_1"):
                clear_session()

    else:
        with st.spinner("Curating your perfect fragrance collection..."):
            try:
                payload = {"query": st.session_state.final_query, "top_k": 6}
                resp = requests.post(f"{API_BASE}/search", json=payload)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        st.subheader("✨ Your Curated Fragrance Collection")
                        for perfume in results:
                            st.markdown(f"""
                                <div class='flashcard'>
                                    <img src="{perfume['image_url']}" class='flashcard-image' alt="{perfume['Name']}">
                                    <div class='flashcard-content'>
                                        <h3 style='color: {COLORS['accent']}; margin-top: 0;'>{perfume['Name']}</h3>
                                        <p style='color: #999; font-style: italic; margin-bottom: 0.5rem;'>by {perfume['Brand']}</p>
                                        <p style='margin-bottom: 0.5rem;'><strong>Notes:</strong> {perfume['Notes']}</p>
                                        <p style='margin-bottom: 0; font-size: 0.9rem;'>{perfume['Description']}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("No perfect matches found. Let's refine your preferences!")
                else:
                    st.error("Error retrieving recommendations")
            except Exception as e:
                st.error(f"Failed to retrieve results: {str(e)}")
        
        if st.button("🔄 Start New Consultation", key="restart_2"):
            clear_session()

def perfume_dna_page():
    st.title("Perfume DNA: Explore the Fragrance Universe")
    st.markdown("Visualize the 'DNA' of perfumes using a 3D UMAP projection. Each point is a perfume, colored by brand. Hover to see details!")

    try:
        umap_df = pd.read_csv('data/umap.csv')
        brand_codes = umap_df['Brand'].astype('category').cat.codes
        brand_names = umap_df['Brand'].astype('category').cat.categories

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=umap_df['umap_x'],
            y=umap_df['umap_y'],
            z=umap_df['umap_z'],
            mode='markers',
            marker=dict(
                size=10,
                color=brand_codes,
                colorscale='magma',
                opacity=0.85,
                colorbar=dict(title='Brand', tickvals=list(range(len(brand_names))), ticktext=brand_names)
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Brand: %{customdata[1]}<br>"
                "Notes: %{customdata[2]}<br>"
                "Description: %{customdata[3]}<br>"
                "<extra></extra>"
            ),
            customdata=umap_df[['Name', 'Brand', 'Notes', 'Description']].values
        ))

        fig.update_layout(
            scene=dict(
                xaxis_title='UMAP X',
                yaxis_title='UMAP Y',
                zaxis_title='UMAP Z'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=650,
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error("UMAP data not found. Please ensure 'data/with_umap.csv' exists.")

if page == "Find My Fragrance":
    chatbot_ui()
elif page == "Perfume DNA (UMAP)":
    perfume_dna_page()