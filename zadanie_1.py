import random

# zamiana macierzy sąsiedztwa na listę sąsiedztwa 
def matrix_to_list(matrix):

    n = len(matrix)
    graf_lista = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                graf_lista[i].append(j)
    return graf_lista

#zamiana macierzy sąsiedztwa na listę krawędzi
def matrix_to_edges(matrix):
    n = len(matrix)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j]:
                edges.append((i, j))
    return edges


def list_to_matrix(graf_lista):
    n = max(graf_lista.keys()) + 1
    matrix = [[0] * n for _ in range(n)]
    for u, nbrs in graf_lista.items():
        for v in nbrs:
            matrix[u][v] = 1
    return matrix

    #zamiana listy sąsiedztwa do listy krawędzi
def list_to_edges(graf_lista):
    edges = set()
    for u, nbrs in graf_lista.items():
        for v in nbrs:
            a, b = min(u, v), max(u, v)
            edges.add((a, b))
    return list(edges)



    #lista krawędzi do listy sąsiedztwa
def edges_to_list(edges):
    if not edges:
        return {}

    nodes = {u for u, v in edges} | {v for u, v in edges}
    n = max(nodes) + 1
    graf_lista = {i: [] for i in range(n)}
    for u, v in edges:
        graf_lista[u].append(v)
        graf_lista[v].append(u)
    return graf_lista


    #lista krawędzi do macierzy sąsiedztwa
def edges_to_matrix(edges):
  
    if not edges:
        return []

    n = max(max(u, v) for u, v in edges) + 1
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1
    return matrix


    #konwertowanie 
def graph_converter(graph, input_type):
 
    if input_type == 'graf_lista':
        mat = list_to_matrix(graph)
        eds = list_to_edges(graph)
        return {'graf_lista': graph, 'graf_macierz': mat, 'gr_lista_krawedzi': eds}

    if input_type == 'graf_macierz':
        lst = matrix_to_list(graph)
        eds = matrix_to_edges(graph)
        return {'graf_macierz': graph,'graf_lista': lst, 'gr_lista_krawedzi': eds}

    if input_type == 'gr_lista_krawedzi':
        lst = edges_to_list(graph)
        mat = edges_to_matrix(graph)
        return {'gr_lista_krawedzi': graph,'graf_lista': lst, 'graf_macierz': mat }

    raise ValueError(f"Nieznany typ reprezentacji grafu: {input_type}")

    #generowanie losowego graf

    #generowane drzewa rozpinającego w celu zapewnienia spójności grafu
def random_spanning_tree(n):

    nodes = list(range(n))
    random.shuffle(nodes)
    connected = {nodes[0]}
    remaining = set(nodes[1:])
    tree_edges = []

    while remaining:
        u = random.choice(list(connected))
        v = random.choice(list(remaining))
        tree_edges.append((u, v))
        connected.add(v)
        remaining.remove(v)

    return tree_edges

def generate_random_connected_graph(n):
    if n < 1:
        return []

    max_edges = n * (n - 1) // 2
    # najpierw drzewo (n-1 krawędzi)
    edges = random_spanning_tree(n)

    # losowanie ile dodatkowych krawędzi dołożyć
    extra = random.randint(0, max_edges - (n - 1))

    # wszystkie możliwe krawędzie, które nie wystąpiły w drzewie
    all_pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    remaining = list(set(all_pairs) - set(tuple(sorted(e)) for e in edges))
    random.shuffle(remaining)

    edges.extend(remaining[:extra])
    return edges


    #generowanie loswego grafu spójnego 
def random_graph(n, representation='graf_lista'):
    edges = generate_random_connected_graph(n)
    if representation == 'gr_lista_krawedzi':
        return edges
    if representation == 'graf_lista':
        return edges_to_list(edges)
    if representation == 'graf_macierz':
        return edges_to_matrix(edges)
    raise ValueError("Nieznany format wyjściowy: " + str(representation))


if __name__ == "__main__":
    
    #     przykładowe inputy:
    graf_lista = {0: [1, 2], 1: [0, 2], 2: [0, 1]}      #graf z trzema wierzchołkami
    graf_macierz = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ]                                                   #graf z czterema wierzchołkami

    gr_lista_krawedzi = [(0, 1), (1, 2), (0, 2), (2, 3), (2, 4)]    #graf z pięcioma wierzchołkami

    # konwersje
    print("Konwersja z listy sąsiedztwa:  \n", graph_converter(graf_lista, 'graf_lista'))
    print("\n")
    print("Konwersja z macierzy sąsiedztwa: \n ", graph_converter(graf_macierz, 'graf_macierz'))
    print("\n")
    print("Konwersja z listy krawędzi:  \n", graph_converter(gr_lista_krawedzi, 'gr_lista_krawedzi'))
    print("\n")


    #losowy graf:
      # losowy graf spójny o 5 wierzchołkach
    g_edges  = random_graph(5, 'gr_lista_krawedzi')
    g_list   = random_graph(5, 'graf_lista')
    g_matrix = random_graph(5, 'graf_macierz')
    print("Losowy graf - krawędzie:", g_edges)
    print("Losowy graf - lista sąsiedztwa:", g_list)
    print("Losowy graf - macierz sąsiedztwa:", g_matrix)

