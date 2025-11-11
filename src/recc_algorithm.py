# By: Hassan Nadeem, EE-24123

import dataset_parser as dsp

import random
from collections import defaultdict


def recommendation_algorithm(
    input_anime, graph, top_n=10, num_walks=1000, walk_length=6
):
    if input_anime not in graph.nodes or graph.nodes[input_anime].type != "anime":
        print(f"Error {input_anime} not found in the graph")
        return []

    landings = defaultdict(int)
    similarity_cache = {}

    for _ in range(num_walks):
        Curr_Node_id = input_anime
        for _ in range(walk_length):
            try:
                neighbour = graph.get_neighbors(Curr_Node_id)
            except KeyError:
                break

            if not neighbour:
                break

            # Computing similarities is expensive, do it just once per anime.
            Neighbour_id = [node for node, _ in neighbour]
            Neighbour_weight = []
            for node, score in neighbour:
                if graph.nodes[node].type == "anime":
                    if node not in similarity_cache:
                        similarity_cache[node] = dsp.genre_similarity(input_anime, node)
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
            Curr_Node_id != input_anime
            and Curr_Node_id in graph.nodes
            and graph.nodes[Curr_Node_id].type == "anime"
        ):
            landings[Curr_Node_id] += 1

    sorted_recommendations = sorted(
        landings.items(), key=lambda item: item[1], reverse=True
    )

    return [anime_title for anime_title, _ in sorted_recommendations[:top_n]]
