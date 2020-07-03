from graphs.graph import Graph, Vertex

class WeightedVertex(object):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> (obj, weight)

    def get_id(self):
        return self.__id

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
        return [(neighbor.__id, weight) for neighbor, weight in self.__neighbors_dict.values()]
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

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj
    
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        # TODO: Implement this function.
        new_vertex = WeightedVertex(vertex_id)
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
        if not self.__is_directed:
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
        def sortFunc(e):
            return e[2]
        def sortFunc2(e):
            return e[0]

        edges = []
        for vertex in self.get_vertices():
            for neighbor, weight in vertex.get_neighbors_with_weights():
                if ((neighbor, vertex.get_id(), weight) not in edges):
                    edges.append((vertex.get_id(), neighbor, weight))
        edges.sort(reverse=True, key=sortFunc2)
        edges.sort(reverse=True, key=sortFunc)
        


        # TODO: Create a dictionary `parent_map` to map vertex -> its "parent". 
        # Initialize it so that each vertex is its own parent.
        parent_map = {vertex.get_id(): vertex.get_id() for vertex in self.get_vertices()}
        
        # TODO: Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)
        solution = []
        # TODO: While the spanning tree holds < V-1 edges, get the smallest 
        # edge. If the two vertices connected by the edge are in different sets 
        # (i.e. calling `find()` gets two different roots), then it will not 
        # create a cycle, so add it to the solution set and call `union()` on 
        # the two vertices.
        while len(solution) < len(self.get_vertices()) - 1 and len(edges) > 0:
            current_edge = edges.pop()
            group1 = self.find(parent_map, current_edge[0])
            group2 = self.find(parent_map, current_edge[1])
            if group1 != group2:
                self.union(parent_map, current_edge[0], current_edge[1])
                solution.append(current_edge)
        return solution
        # TODO: Return the solution list.
    
    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.

        Assume that the graph is connected.
        """
        # TODO: Create a dictionary `vertex_to_weight` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_weight = {vertex.get_id(): float("inf") for vertex in self.get_vertices()}
        # TODO: Choose one vertex and set its weight to 0
        start_vertex = list(vertex_to_weight.keys())[0]
        vertex_to_weight[start_vertex] = 0
        edges = [(start_vertex, edge_id, weight) for edge_id, weight in self.get_vertex(start_vertex).get_neighbors_with_weights()]
        print(edges)
        # TODO: While `vertex_to_weight` is not empty:
        # 1. Get the minimum-weighted remaining vertex, remove it from the
        #    dictionary, & add its weight to the total MST weight
        # 2. Update that vertex's neighbors, if edge weights are smaller than
        #    previous weights
        parent_map = {vertex.get_id(): vertex.get_id() for vertex in self.get_vertices()}
        solution = []
        def sortFunc(e):
            return e[2]
        edges.sort(reverse=True, key=sortFunc)
        while len(solution) < len(self.get_vertices()) - 1 and len(edges) > 0:
            print(edges)
            current_edge = edges.pop()
            group1 = self.find(parent_map, current_edge[0])
            group2 = self.find(parent_map, current_edge[1])
            if group1 != group2:
                self.union(parent_map, current_edge[0], current_edge[1])
                solution.append(current_edge)
                for new_edge, weight in self.get_vertex(current_edge[1]).get_neighbors_with_weights():
                    edges.append((current_edge[1], new_edge, weight))
                    edges.sort(reverse=True, key=sortFunc)
        total = 0
        for edge in solution:
            total += edge[2]
        return total

                    
        print(solution)
        # TODO: Return total weight of MST
