#!/usr/bin/env python3
"""Prim simulator: muestra paso a paso en la terminal la ejecución del algoritmo de Prim.

Uso:
  python prim_simulator.py --graph example_graph.json --start A [--pause]

El formato de JSON esperado está en `example_graph.json` (nodos y lista de aristas).

Autor: Alejandro Aguirre Díaz
"""
import json
import heapq
import argparse
import sys
from typing import Dict, List, Tuple, Set


def load_graph_from_json(path: str) -> Dict[str, List[Tuple[str, float]]]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Espera estructura: {"nodes": [...], "edges": [[u,v,w], ...]}
    adj: Dict[str, List[Tuple[str, float]]] = {n: [] for n in data.get('nodes', [])}
    for u, v, w in data.get('edges', []):
        if u not in adj:
            adj[u] = []
        if v not in adj:
            adj[v] = []
        adj[u].append((v, float(w)))
        adj[v].append((u, float(w)))
    return adj


class PrimSimulator:
    def __init__(self, graph: Dict[str, List[Tuple[str, float]]]):
        self.graph = graph

    def run(self, start: str, pause: bool = False) -> Tuple[List[Tuple[str, str, float]], float]:
        if start not in self.graph:
            raise ValueError(f"Start node '{start}' not found in graph")

        visited: Set[str] = set([start])
        mst_edges: List[Tuple[str, str, float]] = []
        total_weight: float = 0.0

        # Min-heap de aristas (weight, u, v) donde u está en visited y v no
        heap: List[Tuple[float, str, str]] = []
        for v, w in self.graph[start]:
            heapq.heappush(heap, (w, start, v))

        step = 1
        print(f"Inicio Prim desde: {start}\n")
        print(f"Nodos totales: {len(self.graph)}\n")

        while heap and len(visited) < len(self.graph):
            # Mostrar estado del heap
            heap_snapshot = [f"({u}-{v}:{w})" for w, u, v in sorted(heap)]
            print(f"Step {step}: heap front (ordenado): {heap_snapshot}")

            w, u, v = heapq.heappop(heap)
            if v in visited:
                print(f"  - Se omite arista {u}-{v} (vértice {v} ya visitado)")
                step += 1
                if pause:
                    input('Presiona Enter para continuar...')
                continue

            # Seleccionamos la arista mínima que conecta con un vértice no visitado
            visited.add(v)
            mst_edges.append((u, v, w))
            total_weight += w
            print(f"  + Seleccionada arista: {u} - {v} (peso {w})")
            print(f"    Vértices visitados: {sorted(list(visited))}")
            print(f"    APM hasta ahora (aristas): {mst_edges}")
            print(f"    Peso total acumulado: {total_weight}\n")

            # Añadir nuevas aristas que conectan v con no visitados
            added = []
            for nb, nbw in self.graph[v]:
                if nb not in visited:
                    heapq.heappush(heap, (nbw, v, nb))
                    added.append((v, nb, nbw))
            if added:
                print(f"    Se añadieron al heap las aristas desde {v}: {added}")
            else:
                print(f"    No se añadieron aristas nuevas desde {v}")

            step += 1
            if pause:
                input('Presiona Enter para continuar...')

        if len(visited) != len(self.graph):
            print("\nAdvertencia: el grafo no está conectado. Se obtuvo un bosque (APM por componente).")
        else:
            print("\nCompletado: se visitaron todos los vértices.")
        print(f"Peso total del APM: {total_weight}")
        print(f"Aristas del APM: {mst_edges}")
        return mst_edges, total_weight


def main():
    parser = argparse.ArgumentParser(description='Simulador paso a paso del algoritmo de Prim')
    parser.add_argument('--graph', '-g', default='example_graph.json', help='Ruta al JSON del grafo (default: example_graph.json)')
    parser.add_argument('--start', '-s', default=None, help='Vértice inicial (token). Si no se especifica, se usa el primer nodo del grafo')
    parser.add_argument('--pause', '-p', action='store_true', help='Pausar entre pasos (presiona Enter)')
    args = parser.parse_args()

    try:
        graph = load_graph_from_json(args.graph)
    except FileNotFoundError:
        print(f"Error: archivo de grafo no encontrado: {args.graph}")
        sys.exit(1)

    if not graph:
        print(f"Error: el grafo cargado desde {args.graph} está vacío o no tiene nodos.")
        sys.exit(1)

    start_node = args.start if args.start is not None else next(iter(graph))
    print(f"Usando grafo: {args.graph}")
    print(f"Vértice inicial: {start_node}\n")

    sim = PrimSimulator(graph)
    sim.run(start_node, pause=args.pause)


if __name__ == '__main__':
    main()
