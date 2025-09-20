# The Perfume Atelier

An **end-to-end AI-powered recommendation platform** blending **Generative AI, Vector Databases, and Interactive Visualization** to help users discover their *signature scent*.

This project showcases my expertise as a **Full-Stack Machine Learning / AI Engineer** in building production-ready, containerized, multimodal applications that unify **LLMs, vector search, and rich frontends** into one seamless experience.

<br>![demo](https://github.com/Anushqaa/the-perfume-atlier/blob/master/assets/demo.gif)
---

## ✦ Overview

The Perfume Atelier reimagines fragrance discovery by combining:

* **Conversational Recommendation Chatbot** – powered by **DeepSeek 3.1 LLM** with prompt engineering, memory, and reasoning chains.
* **Vector Search Engine** – perfume embeddings indexed via **FAISS (HNSW)** for similarity retrieval.
* **Perfume DNA Visualizer** – an interactive **3D UMAP + Plotly visualization** mapping complex scent relationships.
* **Microservice Architecture** – fully containerized **FastAPI backend** and **Streamlit frontend**, orchestrated with **Docker Compose** and deployed on cloud services.

The result is a **scalable, production-grade, AI-driven recommendation system** with both functionality and aesthetic polish.

---

## ✦ Features

* **Conversational Flow**

  * LLM-driven dialogue that gathers preferences through smart follow-up questions.
  * Few-shot prompting and chain-of-thought reasoning for refined recommendations.

* **Recommendation Engine**

  * Real-time similarity search across perfumes using **vector embeddings + FAISS**.
  * Results displayed as interactive **flashcards with image, notes, and descriptions**.

* **Perfume DNA Explorer**

  * Navigate an interactive **3D visualization of perfumes in vector space**.
  * Discover hidden scent clusters and relationships.

* **Production Deployment**

  * Modular **frontend (Streamlit)** and **backend (FastAPI)** as microservices.
  * **Dockerized architecture** with `docker-compose` for local development.
  * Deployed on **Render** for public availability.

---

## ✦ Tech Stack

<div align="center">

| Domain             | Technologies                                                                                                                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend**       | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit\&logoColor=white) ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?logo=plotly\&logoColor=white)                                                                                       |
| **Backend**        | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi\&logoColor=white) ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python\&logoColor=white)                                                                                             |
| **Vector DB / ML** | ![FAISS](https://img.shields.io/badge/-FAISS-005F9E?logo=facebook\&logoColor=white) ![UMAP](https://img.shields.io/badge/-UMAP-6D9DC5?logo=scipy\&logoColor=white) ![ScikitLearn](https://img.shields.io/badge/-ScikitLearn-F7931E?logo=scikit-learn\&logoColor=white) |
| **LLM / AI**       | ![DeepSeek](https://img.shields.io/badge/-DeepSeek3.1-1C1C1C?logo=openai\&logoColor=white)                                                                                                                                                                             |
| **Deployment**     | ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker\&logoColor=white) ![Render](https://img.shields.io/badge/-Render-46E3B7?logo=render\&logoColor=white)                                                                                                |
| **Other**          | ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas\&logoColor=white) ![Numpy](https://img.shields.io/badge/-NumPy-013243?logo=numpy\&logoColor=white)                                                                                                   |

</div>  

---

## ✦ Project Structure

```bash
├── /notebook          # Prototype experiments for vector search engine
├── /models
│   ├── preprocess.py  # Data preprocessing for perfume dataset
│   ├── faiss_ops.py   # FAISS index pipeline with HNSW configuration
│   └── visualization.py # UMAP generation for visualization
├── /frontend          # Streamlit app: chatbot UI + visualization
├── /backend           # FastAPI backend: LLM, search, services
├── docker-compose.yml # Microservice orchestration
```

<p align="center">
  <img src="https://raw.githubusercontent.com/Anushqaa/the-perfume-atlier/refs/heads/master/assets/directory.png" width="30%"/>
</p>

---

## ✦ Media Showcase

<p align="center">
  <img src="https://raw.githubusercontent.com/Anushqaa/the-perfume-atlier/refs/heads/master/assets/home.png" width="70%" alt="Landing Page"/>
  <br/><i>Chatbot interface for conversational recommendations<br></i>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Anushqaa/the-perfume-atlier/refs/heads/master/assets/dna.png" width="70%" alt="Perfume DNA Visualization"/>
  <br/><i>Interactive 3D visualization of perfumes in vector space<br></i>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Anushqaa/the-perfume-atlier/refs/heads/master/assets/docker.png" width="50%" alt="Docker Compose Architecture"/>
  <br/><i>Microservice architecture powered by Docker Compose<br></i>
</p>

---

## ✦ Getting Started

**Prerequisites**

* Docker & Docker Compose installed

**Run locally**

```bash
# Build and start services
docker-compose up --build
```

Frontend will be available at: **[http://localhost:8501](http://localhost:8501)**
Backend API will be available at: **[http://localhost:8000](http://localhost:8000)**

---

## ✦ License

Licensed under **Apache 2.0** – see [LICENSE](./LICENSE) for details.

---

## ✦ Contact

For collaboration or opportunities, feel free to connect:

**\[Anushqaa]**

\[https://imaqui.streamlit.app] • \[anushqa.shekhawat@gmail.com]
