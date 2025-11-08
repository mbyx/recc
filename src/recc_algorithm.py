import random
from collections import defaultdict

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
    
