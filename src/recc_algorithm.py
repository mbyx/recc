import random
from collections import defaultdict

#My written algorithm
def Recommendation_algorithm(Input_anime,Graph,Top_n=10,num_walks=1000,walk_lenght=6):
    landings = defaultdict(int)
    if Input_anime not in Graph.nodes or Graph.nodes[Input_anime].type != 'anime':
      print(f"Error {Input_anime} not found in the graph")
      return []
    
    print(f"{num_walks} random walks from {Input_anime}")
    for i in range(num_walks):
      Curr_Node_id = Input_anime
      for _ in range(walk_lenght):
        try:
          neighbour = Graph.get_neighbors(Curr_Node_id)
        except KeyError:
          break
        
        if not neighbour:
          break
        
        Neighbour_id = [node for node, weight in neighbour]
        Neighbour_weight = [weight for node, weight in neighbour]
        
        Curr_Node_id = random.choices(Neighbour_id, weights = Neighbour_weight,k=1)[0]
        
      if (Curr_Node_id != Input_anime and Curr_Node_id in Graph.nodes and Graph.nodes[Curr_Node_id].type == 'anime'):
        landings[Curr_Node_id] += 1
      
    sorted_recommendations = sorted(landings.items(), key=lambda item: item[1], reverse=True)
      
    return [anime_title for anime_title, score in sorted_recommendations[:Top_n]]
    
'''#Your generated algorithm
def get_recommendations_random_walk(graph, start_anime_title, top_n=10, num_walks=1000, walk_length=6):
    """
    Finds anime recommendations using a weighted random walk.
    
    Args:
        graph (wg.Graph): The populated graph object.
        start_anime_title (str): The title of the anime to start from.
        top_n (int): The number of recommendations to return.
        num_walks (int): The number of random walks to perform.
        walk_length (int): The number of steps in each walk.

    Returns:
        list: A list of recommended anime titles.
    """
    
    # This dictionary will store {anime_title: count_of_landings}
    landings = defaultdict(int)

    # 1. Check if the input anime is valid
    if start_anime_title not in graph.nodes or graph.nodes[start_anime_title].type != 'anime':
        print(f"Error: Anime '{start_anime_title}' not found in the graph.")
        return []

    print(f"Starting {num_walks} random walks from '{start_anime_title}'...")
    
    # 2. Start the main loop for all walks
    for _ in range(num_walks):
        current_node_id = start_anime_title
        
        # 3. Perform a single walk
        for _ in range(walk_length):
            try:
                neighbors = graph.get_neighbors(current_node_id)
            except KeyError:
                break # This node has no neighbors, end this walk

            if not neighbors:
                break # No neighbors, end this walk

            # 4. Prepare for a weighted random choice
            #    We are more likely to walk to a node with a higher score (weight)
            neighbor_ids = [node for node, weight in neighbors]
            neighbor_weights = [weight for node, weight in neighbors]
            
            # 5. Perform the weighted random choice
            #    random.choices returns a list, so we take the first item [0]
            current_node_id = random.choices(neighbor_ids, weights=neighbor_weights, k=1)[0]
        
        # 6. The walk is over. Check where we landed.
        #    We only care if we landed on an ANIME that is NOT our starting anime.
        if (current_node_id != start_anime_title and 
            current_node_id in graph.nodes and 
            graph.nodes[current_node_id].type == 'anime'):
            
            # 7. Increment the counter for that anime
            landings[current_node_id] += 1

    # 8. Sort the recommendations by the number of times we landed on them
    sorted_recommendations = sorted(landings.items(), key=lambda item: item[1], reverse=True)

    # 9. Return just the titles of the top_n anime
    return [anime_title for anime_title, score in sorted_recommendations[:top_n]]'''
        
  

