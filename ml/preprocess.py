import pandas as pd
import re
import numpy as np
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()


def clean_notes(notes):
    lemmatizer = WordNetLemmatizer()
    notes = re.split(r'[,/]', notes)
    return [lemmatizer.lemmatize(note.strip().lower()) for note in notes if note.strip()]

def clean(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip().lower()

def create_combined_text(row):
    return f"{row['Name']} by {row['Brand']}. {row['Description']}. Notes include: {', '.join(row['Clean_Notes'])}."

def generate_embeddings(df, model):
    df['embedding'] = df['text'].apply(lambda x: model.encode(x).tolist())
    return df

def preprocess_data(input_path, output_csv, embeddings_path):
    df = pd.read_csv(input_path)
    
    required_columns = ['Name', 'Brand', 'Description', 'Notes']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing required columns in dataset")
    df = df.dropna(subset=required_columns)

    df['Clean_Notes'] = df['Notes'].apply(clean_notes)
    df['Description'] = df['Description'].apply(clean)
    df['text'] = df.apply(create_combined_text, axis=1)

    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    df = generate_embeddings(df, model)
    embeddings = np.vstack(df["embedding"].values)
    
    df.to_csv(output_csv, index=False)
    np.save(embeddings_path, embeddings)
    print(f"Data saved to {output_csv}")
    print(f"Embeddings saved to {embeddings_path}")

if __name__ == "__main__":
    preprocess_data(
        '/data/perfumes.csv',
        os.getenv('CSV_PATH'),
        os.getenv('EMBEDDINGS_PATH')
    )
