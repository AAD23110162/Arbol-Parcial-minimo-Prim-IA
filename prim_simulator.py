#!/usr/bin/env python3
"""
Prim simulator: simulador paso a paso del algoritmo de Prim.

Descripción:
    Este script ejecuta el algoritmo de Prim sobre un grafo no dirigido y ponderado,
    mostrando en la terminal cada paso: estado del heap de aristas, arista seleccionada,
    vértices visitados y peso acumulado del árbol parcial mínimo (APM).

Salida:
    El programa imprime en la consola el desarrollo del algoritmo y al final muestra
    el peso total del APM y la lista de aristas seleccionadas.

Autor: Alejandro Aguirre Díaz

"""
import json
import heapq
import argparse
import sys
import os
import glob
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


def find_path_in_mst(mst_edges: List[Tuple[str, str, float]], start: str, target: str):
    """Busca un camino entre start y target dentro del APM (lista de aristas).
    Devuelve una tupla (lista_nodos, peso) o None si no hay camino.
    """
    from collections import deque

    # Construir adjacencia del APM
    adj = {}
    for u, v, w in mst_edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    if start == target:
        return ([start], 0.0)

    q = deque([start])
    prev = {start: None}

    while q:
        node = q.popleft()
        for nb, _ in adj.get(node, []):
            if nb not in prev:
                prev[nb] = node
                if nb == target:
                    q.clear()
                    break
                q.append(nb)

    if target not in prev:
        return None

    # Reconstruir camino
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path = list(reversed(path))

    # Calcular peso del camino
    weight = 0.0
    for a, b in zip(path, path[1:]):
        # buscar peso en adj
        found = False
        for nb, w in adj.get(a, []):
            if nb == b:
                weight += w
                found = True
                break
        if not found:
            # debería ser imposible si el camino viene del APM
            pass

    return (path, weight)


def main():
    parser = argparse.ArgumentParser(description='Simulador paso a paso del algoritmo de Prim')
    parser.add_argument('--graph', '-g', default='example_graph.json', help='Ruta al JSON del grafo (default: example_graph.json)')
    parser.add_argument('--start', '-s', default=None, help='Vértice inicial (token). Si no se especifica, se usa el primer nodo del grafo')
    parser.add_argument('--mode', '-m', choices=['demo', 'interactive'], default='demo', help='Modo de ejecución: demo (por defecto) o interactive')
    parser.add_argument('--pause', '-p', action='store_true', help='Pausar entre pasos (presiona Enter)')
    args = parser.parse_args()

    # Preguntar modo al iniciar (permite elegir 1=demo o 2=interactive)
    default_mode = args.mode
    print('Elige modo:')
    print('  1) demo (ejecuta Prim usando el grafo/argumentos)')
    print('  2) interactive (lista grafos y permite selección interactiva)')
    choice = input(f"Selecciona modo [1/2] (Enter = {'1' if default_mode=='demo' else '2'}): ").strip()
    if choice == '1':
        mode = 'demo'
    elif choice == '2':
        mode = 'interactive'
    else:
        mode = default_mode

    # Demo mode: comportamiento clásico (cargar grafo pasado por --graph)
    if mode == 'demo':
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
        return

    # Interactive mode: listar grafos .json disponibles y pedir selección de nodos
    if mode == 'interactive':
        # Si el usuario pasó --graph y existe, usarlo; sino listar archivos .json
        if args.graph and os.path.exists(args.graph):
            chosen_graph = args.graph
        else:
            json_files = sorted(glob.glob('*.json'))
            if not json_files:
                print('No se encontraron archivos .json en el directorio actual.')
                sys.exit(1)
            print('Grafos disponibles:')
            for i, jf in enumerate(json_files, start=1):
                print(f"  {i}) {jf}")
            sel = input('Elige el número del grafo a cargar (o escribe ruta): ').strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if idx < 0 or idx >= len(json_files):
                    print('Selección inválida.')
                    sys.exit(1)
                chosen_graph = json_files[idx]
            else:
                chosen_graph = sel

        try:
            graph = load_graph_from_json(chosen_graph)
        except FileNotFoundError:
            print(f"Error: archivo de grafo no encontrado: {chosen_graph}")
            sys.exit(1)

        if not graph:
            print(f"Error: el grafo cargado desde {chosen_graph} está vacío o no tiene nodos.")
            sys.exit(1)

        # Vista previa: listar aristas del grafo (sin duplicados)
        edges_seen = set()
        print('\nAristas del grafo:')
        for u in sorted(graph.keys()):
            for v, w in graph[u]:
                pair = tuple(sorted((u, v)))
                if pair in edges_seen:
                    continue
                edges_seen.add(pair)
                print(f"  {pair[0]} - {pair[1]} (peso {w})")

        nodes = sorted(list(graph.keys()))
        print('\nNodos disponibles:')
        print(', '.join(nodes))

        # Pedir nodo inicio
        while True:
            start_node = input('Introduce vértice inicial: ').strip()
            if start_node in graph:
                break
            print('Vértice no encontrado. Intenta de nuevo.')

        # Pedir nodo destino (opcional)
        target_node = input('Introduce vértice destino (opcional, Enter para omitir): ').strip()
        if target_node == '':
            target_node = None
        elif target_node not in graph:
            print('Vértice destino no encontrado. Se ignorará la búsqueda de camino.')
            target_node = None

        print(f"\nCargando grafo: {chosen_graph}")
        print(f"Inicio: {start_node}")
        if target_node:
            print(f"Destino: {target_node}")
        print('')

        sim = PrimSimulator(graph)
        mst_edges, total = sim.run(start_node, pause=args.pause)

        if target_node:
            path = find_path_in_mst(mst_edges, start_node, target_node)
            if path is None:
                print(f"No hay camino entre {start_node} y {target_node} en el APM.")
            else:
                path_nodes, path_weight = path
                print(f"Camino en el APM desde {start_node} hasta {target_node}: {path_nodes}")
                print(f"Peso del camino en el APM: {path_weight}")
        return



if __name__ == '__main__':
    main()
