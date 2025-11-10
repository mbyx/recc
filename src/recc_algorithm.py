# By: Hassan Nadeem, EE-24123

import dataset_parser as dsp

import random
from collections import defaultdict


def Recommendation_algorithm(
    Input_anime, Graph, Top_n=10, num_walks=1000, walk_lenght=6
):
    landings = defaultdict(int)
    if Input_anime not in Graph.nodes or Graph.nodes[Input_anime].type != "anime":
        print(f"Error {Input_anime} not found in the graph")
        return []
    similarity_cache = {}
    for i in range(num_walks):
        Curr_Node_id = Input_anime
        for _ in range(walk_lenght):
            try:
                neighbour = Graph.get_neighbors(Curr_Node_id)
            except KeyError:
                break

            if not neighbour:
                break

			# Computing similarities is expensive, do it just once per anime.
            Neighbour_id = [node for node, weight in neighbour]
            Neighbour_weight = []
            for node, score in neighbour:
                if Graph.nodes[node].type == "anime":
                    if node not in similarity_cache:
                        similarity_cache[node] = dsp.genre_similarity(Input_anime, node)
                    sim = similarity_cache[node]
                else:
                    sim = 0.0
                Neighbour_weight.append(0.05 * score + 0.95 * sim)

            if sum(Neighbour_weight) == 0:
                Curr_Node_id = random.choice(Neighbour_id)
            else:
                Curr_Node_id = random.choices(
                    Neighbour_id, weights=Neighbour_weight, k=1
                )[0]

        if (
            Curr_Node_id != Input_anime
            and Curr_Node_id in Graph.nodes
            and Graph.nodes[Curr_Node_id].type == "anime"
        ):
            landings[Curr_Node_id] += 1

    sorted_recommendations = sorted(
        landings.items(), key=lambda item: item[1], reverse=True
    )

    return [anime_title for anime_title, score in sorted_recommendations[:Top_n]]
