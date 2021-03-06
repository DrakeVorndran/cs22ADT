from collections import deque

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # neighbor_id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.__id] = vertex_obj
        pass

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the neighbor_id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # neighbor_id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        new_vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex
        

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with neighbor_id `vertex_id1` to vertex with neighbor_id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        vertex1 = self.__vertex_dict[vertex_id1]
        vertex2 = self.__vertex_dict[vertex_id2]
        vertex1.add_neighbor(vertex2)
        if(not self.__is_directed):
            vertex2.add_neighbor(vertex1)
        pass
        
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.pop()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The neighbor_id of the start vertex.
        target_id (string): The neighbor_id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The neighbor_id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        seen = set()
        dist_dict = {start_id: 0}
        quene = [start_id]
        current_dist = 0
        correct_dist = []
        while len(quene) > 0 and current_dist < target_distance:
            current_id = quene.pop(0)
            seen.add(current_id)
            current_dist = dist_dict[current_id]
            current_vertex = self.get_vertex(current_id)
            for neighbor in current_vertex.get_neighbors():
                neighbor_id = neighbor.get_id()
                if neighbor_id not in seen:
                    quene.append(neighbor_id)
                
                if neighbor_id not in dist_dict:
                    dist_dict[neighbor_id] = current_dist + 1
                    if current_dist + 1 == target_distance:
                        correct_dist.append(neighbor_id)
        return correct_dist

    def is_bipartite(self):
        start_id = list(self.__vertex_dict.keys())[0]
        quene = [start_id]
        color_dict = {start_id: 0}
        seen = set()
        seen.add(start_id)
        current_color = 0
        while len(quene) > 0:
            current_id = quene.pop(0)
            current_color = color_dict[current_id]
            seen.add(current_id)
            current_node = self.get_vertex(current_id)
            for neighbor in current_node.get_neighbors():
                neighbor_id = neighbor.get_id()
                if neighbor_id in color_dict:
                    if color_dict[neighbor_id] == current_color:
                        return False
                else:
                    color_dict[neighbor_id] = (current_color + 1) % 2
                    quene.append(neighbor_id)
        return True

    def find_connected_components(self):
        all_ids = set(self.__vertex_dict.keys())

        components = []

        while len(all_ids) > 0:
            start_id = list(all_ids).pop()
            all_ids.remove(start_id)
            start_vertex = self.get_vertex(start_id)
            seen = set()
            quene = [start_id]
            seen.add(start_id)
            while len(quene) > 0:
                current_id = quene.pop(0)
                current_vertex = self.get_vertex(current_id)
                for neighbor in current_vertex.get_neighbors():
                    neighbor_id = neighbor.get_id()
                    if neighbor_id in all_ids:
                        all_ids.remove(neighbor_id)
                    if neighbor_id not in seen:
                        quene.append(neighbor_id)
                        seen.add(neighbor_id)
            components.append(list(seen))
        return(components)
    
    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        verts = self.get_vertices()
        indegree_dict = {}
        for vert in verts:
            if vert.get_id() not in indegree_dict:
                indegree_dict[vert.get_id()] = 0
            for neighbor in vert.get_neighbors():
                neighbor_id = neighbor.get_id()
                if neighbor_id in indegree_dict:
                    indegree_dict[neighbor_id] += 1
                else:
                    indegree_dict[neighbor_id] = 1
        
        indeg0 = []
        for vertex_id, indegree in indegree_dict.items():
            if indegree == 0:
                indeg0.append(vertex_id)
        
        sorted_list = []

        while len(indeg0) > 0:
            current_id = indeg0.pop()
            sorted_list.append(current_id)
            current_vertex = self.get_vertex(current_id)
            for neighbor in current_vertex.get_neighbors():
                neighbor_id = neighbor.get_id()
                indegree_dict[neighbor_id] -= 1
                if indegree_dict[neighbor_id] == 0:
                    indeg0.append(neighbor_id)
        return sorted_list

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        stack = [start_id]
        path = []
        depth = {}
        depth[start_id] = 0

        while len(stack) > 0:
            current_id = stack.pop()
            current_depth = depth[current_id]
            current_vertex = self.get_vertex(current_id)
            path = path[:current_depth + 1]
            path.append(current_id)
            for neighbor in current_vertex.get_neighbors():
                neighbor_id = neighbor.get_id()
                if neighbor_id not in depth:
                    if neighbor_id == target_id:
                        path.append(neighbor_id)
                        return path
                    depth[neighbor_id] = current_depth + 1
                    stack.append(neighbor_id)


    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        def recursive_cycle_finder(vertex, stack=set()):
            if vertex in stack:
                return True
            stack.add(vertex)
            print(all_ids, vertex)
            if(vertex in all_ids):
                all_ids.remove(vertex)
            vertex_obj = self.get_vertex(vertex)
            for neighbor in vertex_obj.get_neighbors():
                neighbor_id = neighbor.get_id()
                print("Neighbor", neighbor_id)
                cycle = recursive_cycle_finder(neighbor_id, stack)
                if cycle:
                    return True
            stack.remove(vertex)
            return False

        all_ids = set(self.__vertex_dict.keys())

        visited = set()
        while len(all_ids) > 0:
            start_id = list(all_ids)[0]
            cycle = recursive_cycle_finder(start_id)
            if cycle:
                return True
        return False

        
                

        pass











