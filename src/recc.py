import dataset_parser as dsp
import weighed_graph as wg

# Useful constants for testing graph.
NARUTO_ANIME_ID: int = 20
BLEACH_ANIME_ID: int = 269

dsp.merge_datasets()

details = dsp.construct_details()

# Example of genre similarity function.
print(dsp.genre_similarity(NARUTO_ANIME_ID, BLEACH_ANIME_ID))

# Creating the graph from the data.
graph = wg.Graph()
for user, watched_anime in details.items():
    graph.add_node(user, 'user')
    for id, anime_details in watched_anime.items():
        title, genres, score = (
            anime_details["title"],
            anime_details["genre"],
            anime_details["score"],
        )
        graph.add_node(title, 'anime', { 'genres': genres })
        graph.add_edge(user, title, score)
        # Graph is unidirectional.
        graph.add_edge(title, user, score)
