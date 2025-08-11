import random

#generowanie grafu
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
    edges = random_spanning_tree(n)
    all_pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    remaining = list(set(all_pairs) - set(tuple(sorted(e)) for e in edges))
    extra = random.randint(0, max_edges - (n - 1))
    random.shuffle(remaining)
    edges.extend(remaining[:extra])
    return edges

def edges_to_list(edges):
    if not edges:
        return {}
    nodes = {u for u, v in edges} | {v for u, v in edges}
    n = max(nodes) + 1
    graf = {i: [] for i in range(n)}
    for u, v in edges:
        graf[u].append(v)
        graf[v].append(u)
    return graf



# wykrywanie cykli
def find_all_cycles(graf_lista):
    n = len(graf_lista)
    cycles = set()

    def dfs(u, start, parent, path, used_edges):
        for node in graf_lista[u]:
            edge = tuple(sorted((u, node)))
            if edge in used_edges:
                continue
            if node == parent:
                continue

            #   program po napotkaniu wierzchołka, który już jest na ścieżce zapisuje cykl
            if node in path:
                idx = path.index(node)
                cycle = path[idx:] + [node]

                 #normalizacja cyklu
                min_node = min(cycle)
                #obrót listy, by zacząć od min_node
                while cycle[0] != min_node:
                    cycle.append(cycle.pop(0))

                #sprawdzaie  odwróconej wersji
                rev = list(reversed(cycle))
                if rev[0] == min_node and rev < cycle:
                    cycle = rev
                cycles.add(tuple(cycle))
                continue

            used_edges.add(edge)
            path.append(node)
            dfs(node, start, u, path, used_edges)
            path.pop()
            used_edges.remove(edge)

    for start in range(n):
        dfs(start, start, -1, [start], set())

    return [list(c) for c in cycles]


if __name__ == "__main__":

    #Generowanie losowego grafu spójnego  o zadanej liczbie wierzchołków
    n = int(input("Witaj w programie do wyszukiwania cyklów w grafie. \n Podaj liczbę wierzchołków grafu: ").strip())
    edges = generate_random_connected_graph(n)
    graf_lista = edges_to_list(edges)

    print("\nWygenerowany graf (lista sąsiedztwa):")
    for u, nbrs in graf_lista.items():
        print(f"   {u}: {nbrs}")

    # Wykrywanie i wyświetlenie cykli
    cycles = find_all_cycles(graf_lista)
    if cycles:
        print("\nZnalezione cykle:")
        for cyc in cycles:
            print("  ", " -> ".join(map(str, cyc)))
        print('Koniec programu')
    else:
        print("\nNie znaleziono cyklu w grafie")
        print('Koniec progrmau')
