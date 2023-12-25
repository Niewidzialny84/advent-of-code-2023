import networkx as nx

def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()
    
def findTwoGrupsSizes(lines: list[str]) -> int:
    graph = nx.Graph()

    for line in lines:
        left, right = line.split(':')

        for node in right.strip().split():
            graph.add_edge(left, node)
            graph.add_edge(node, left)

    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    a, b = nx.connected_components(graph)

    return len(a) * len(b)

testArray = [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr'
]

def main():
    lines = read_file()
    print(findTwoGrupsSizes(lines))

main()