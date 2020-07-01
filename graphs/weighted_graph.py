from graphs.graph import Graph, Vertex

class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        # TODO: Implement this function.
        self.__neighbors_dict[vertex_obj.__id] = (vertex_obj, weight)
        pass

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        # TODO: Implement this function.]
        return self.__neighbors_dict.keys()
        pass

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        # TODO: Implement this function.
        return [(neighbor.__id, weight) for neighbor, weight in self.__neighbors_dict]
        pass


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        """
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # id -> object
        self.__is_directed = is_directed


    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        # TODO: Implement this function.
        new_vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex

    

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # TODO: Implement this function.
        vertex1 = self.get_vertex(vertex_id1)
        vertex2 = self.get_vertex(vertex_id2)
        vertex1.add_neighbor(vertex2, weight)
        if self.__is_directed:
            vertex2.add_neighbor(vertex1, weight)

        pass

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root


    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # TODO: Create a list of all edges in the graph, sort them by weight 
        # from smallest to largest
        

        # TODO: Create a dictionary `parent_map` to map vertex -> its "parent". 
        # Initialize it so that each vertex is its own parent.

        # TODO: Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)

        # TODO: While the spanning tree holds < V-1 edges, get the smallest 
        # edge. If the two vertices connected by the edge are in different sets 
        # (i.e. calling `find()` gets two different roots), then it will not 
        # create a cycle, so add it to the solution set and call `union()` on 
        # the two vertices.

        # TODO: Return the solution list.
