import dataset_parser as dsp
import weighed_graph as wg
import recc_algorithm as ra

# Useful constants for testing graph.
NARUTO_ANIME_ID: int = 20
BLEACH_ANIME_ID: int = 269

dsp.merge_datasets()

details = dsp.construct_details()

# Creating the graph from the data.
graph = wg.Graph()
for user, watched_anime in details.items():
    graph.add_node(user, "user")
    for id, anime_details in watched_anime.items():
        title, genres, score = (
            anime_details["title"],
            anime_details["genre"],
            anime_details["score"],
        )
        graph.add_node(id, "anime", {"genres": genres})
        graph.add_edge(user, id, score)
        # Graph is unidirectional.
        graph.add_edge(id, user, score)

# Using the algorithm on an example initial anime.
anime_id = BLEACH_ANIME_ID
anime_title = dsp.extract_title_from_id(anime_id)
if anime_title:
    print(f"\nFinding recommendations for: {anime_title} (Random Walk)...")
    recs = ra.recommendation_algorithm(anime_id, graph, num_walks=5000)

    if recs:
        print("--- Top 10 Recommendations (Random Walk) ---")
        for i, id in enumerate(recs, 1):
            print(f"{i}. {dsp.extract_title_from_id(id)}")
    else:
        print(f"Could not find any recommendations for {anime_title}.")

# Example output:
"""
Finding recommendations for: Bleach (Random Walk)...
--- Top 10 Recommendations (Random Walk) ---
1. One Piece
2. Code Geass: Lelouch of the Rebellion
3. Naruto
4. Code Geass: Lelouch of the Rebellion R2
5. InuYasha
6. Fullmetal Alchemist
7. Fullmetal Alchemist: Brotherhood
8. Ouran High School Host Club
9. Rurouni Kenshin
10. Darker than Black
"""
