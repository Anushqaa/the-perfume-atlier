import numpy as np
import pandas as pd
from umap import UMAP
import os
from dotenv import load_dotenv

load_dotenv()

def generate_umap_projections(embeddings_path, csv_path, output_path):
    embeddings = np.load(embeddings_path)
    df = pd.read_csv(csv_path)
    
    reducer = UMAP(n_components=3, random_state=42)
    projections = reducer.fit_transform(embeddings)
    
    df['umap_x'] = projections[:,0]
    df['umap_y'] = projections[:,1]
    df['umap_z'] = projections[:,2]
    
    df.to_csv(output_path, index=False)
    print(f"UMAP projections saved to {output_path}")

if __name__ == '__main__':
    generate_umap_projections(
        os.getenv("EMBEDDINGS_PATH"),
        os.getenv("CSV_PATH"),
        os.getenv("UMAP_PATH")
    )