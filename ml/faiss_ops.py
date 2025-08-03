import pandas as pd
import numpy as np
import faiss
import os
from dotenv import load_dotenv

load_dotenv()

def build_index(embeddings_path, csv_path, index_output_path):

    embeddings = np.load(embeddings_path)
    df = pd.read_csv(csv_path)

    faiss.normalize_L2(embeddings)
    d = embeddings.shape[1]

    id_map = df.set_index("id").to_dict('index')
    index = faiss.IndexIDMap(faiss.IndexFlatL2(d))
    index.add_with_ids(embeddings, df['id'].values.astype('int64'))

    faiss.write_index(index, index_output_path)
    print(f"FAISS index saved to {index_output_path}")

    return index, id_map

if __name__ == '__main__':  
    build_index(
        os.getenv("EMBEDDINGS_PATH"),
        os.getenv("CSV_PATH"),
        os.getenv("INDEX_PATH")
    )