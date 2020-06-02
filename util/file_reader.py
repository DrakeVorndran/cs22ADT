from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # TODO: Use 'open' to open the file
    my_file = open(filename)
    
    

    # TODO: Use the first line (G or D) to determine whether graph is directed 
    # and create a graph object
    graph_type = my_file.readline().strip()
    if graph_type == "G" :
        graph = Graph(False)
    elif graph_type == "D" :
        graph = Graph(True)
    else:
        raise ValueError("Invalid Graph type")

    # TODO: Use the second line to add the vertices to the graph
    vertices = my_file.readline().strip().split(",")
    for vertex in vertices:
        graph.add_vertex(vertex)


    # TODO: Use the 3rd+ line to add the edges to the graph
    for edge in my_file:
        vertex1, vertex2 = edge.strip()[1:-1].split(",")
        graph.add_edge(vertex1, vertex2)

    return graph
    pass

if __name__ == '__main__':

    graph = read_graph_from_file('test.txt')

    print(graph)