import numpy as np
import pandas as pd
from openai import OpenAI

def load_dataset(source: str) -> pd.core.frame.DataFrame:
    pd_vectors = pd.read_json(source)
    return pd_vectors.drop(columns=["text"], errors="ignore").fillna("")


def cosine_similarity(a, b):
    if len(a) > len(b):
        b = np.pad(b, (0, len(a) - len(b)), "constant")
    elif len(b) > len(a):
        a = np.pad(a, (0, len(b) - len(a)), "constant")
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_videos(
    query: str, dataset: pd.core.frame.DataFrame, rows: int
) -> pd.core.frame.DataFrame:

    video_vectors = dataset.copy()

    query_embeddings = client.embeddings.create(
        input=query,
        model=model
    ).data[0].embedding

    video_vectors["similarity"] = video_vectors["ada_v2"].apply(
        lambda x: cosine_similarity(
            np.array(query_embeddings),
            np.array(x)
        )
    )
    mask = video_vectors["similarity"] >= SIMILARITIES_RESULTS_THRESHOLD
    video_vectors = video_vectors[mask].copy()

    video_vectors = video_vectors.sort_values(
        by="similarity",
        ascending=False
    ).head(rows)

    return video_vectors.head(rows)


def display_results(videos: pd.core.frame.DataFrame, query: str):

    def _gen_yt_url(video_id: str, seconds: int) -> str:
        return f"https://youtu.be/{video_id}?t={seconds}"
    
    print(f"\nvideos simlart to'{query}':")
    for _,row in videos.iterrows():
         youtube_url=_gen_yt_url(row,["video_id"],row["seconds"])
         print(f"-{row['title']}")
         print(f"summary{''.join(row['summary'].split()[:15])}...")
         print(f"similarty{row['similarity']}")
         print(f"   Speakers: {row['speaker']}")

pd_vectors=load_dataset(DATASET_NAME)

while True:
    query=input("enter a  query")
    if query == 'exit':
        break
videos=get_videos(query,pd_vectors,5)
display_results(videos,query)

    