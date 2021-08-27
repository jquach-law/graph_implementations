# Course: CS261 - Data Structures
# Author: Justin Quach-Law
# Assignment: Assignment 6 - Portfolio Project
# Description: A directed-weighted graph class with methods to add, remove and get vertices and edges.
# It also performs depth-first search, breadth-first search and checks if a graph is cyclic. Lastly,
# it also performs Dijkstra search for the shortest path.

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph
        """
        self.v_count += 1
        self.adj_matrix.append(list())
        for lst in self.adj_matrix:
            while len(lst) < self.v_count:
                lst.append(0)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edges to the graph
        """
        size = len(self.adj_matrix) - 1
        if src > size or dst > size:
            return
        if src < 0 or dst < 0:
            return
        if src == dst:
            return
        if weight < 0:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove edge from the graph
        """
        size = len(self.adj_matrix) - 1
        if src > size or dst > size:
            return
        if src < 0 or dst < 0:
            return
        if src == dst:
            return

        if self.adj_matrix[src][dst] == 0:
            return
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        count = 0
        lst_vertices = list()
        for lst in self.adj_matrix:
            lst_vertices.append(count)
            count += 1

        return lst_vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        lst_edges = list()
        row = 0
        for lst in self.adj_matrix:
            row += 1
            column = 0
            for vertex in lst:
                column += 1
                if vertex != 0:
                    lst_edges.append((row - 1, column - 1, vertex))
        return lst_edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        size = len(path)
        if size == 0 or size == 1:
            return True

        index = 0
        while index < size:
            src = path[index]
            dst = path[index + 1]
            if self.adj_matrix[src][dst] > 0:
                if dst == path[-1]:
                    return True
                index += 1
            else:
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        last = len(self.adj_matrix) - 1
        if v_start > last:
            return list()

        visited = list()
        stack = deque(list())
        stack.append(v_start)
        while len(stack) > 0:
            pick = stack.pop()
            if pick not in visited:
                visited.append(pick)
                if pick == v_end:
                    return visited

                index = -1
                matrix = self.adj_matrix
                while (index + len(matrix)) >= 0:
                    if matrix[pick][index] > 0:
                        stack.append(len(matrix) + index)
                    index -= 1

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        last = len(self.adj_matrix) - 1
        if v_start > last:
            return list()

        visited = list()
        queue = deque(list())
        queue.append(v_start)
        while len(queue) > 0:
            pick = queue.popleft()
            visited.append(pick)
            if pick == v_end:
                return visited

            index = 0
            matrix = self.adj_matrix
            while index < len(matrix):
                if matrix[pick][index] > 0:
                    if index not in visited:
                        if index not in queue:
                            queue.append(index)
                index += 1

        return visited

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        row_index = 0
        size = len(self.adj_matrix)
        while row_index < size:

            visited = list()
            stack = deque(list())
            first = row_index
            excluded_first = False
            stack.append(first)
            while len(stack) > 0:
                pick = stack.pop()
                if pick not in visited:
                    visited.append(pick)
                    # excluding first from visited list
                    if excluded_first is False:
                        visited.remove(pick)
                        excluded_first = True
                    elif pick == first:
                        return True

                    index = -1
                    matrix = self.adj_matrix
                    while (index + size) >= 0:
                        if matrix[pick][index] > 0:
                            stack.append(size + index)
                        index -= 1

            row_index += 1

        return False

    def dijkstra(self, src: int) -> []:
        """
        Computes the shortest path from a given vertex to other vertices
        """

        matrix = self.adj_matrix
        size = len(matrix)

        visited = dict()
        priority_q = deque(list())
        priority_q.append((0, src))
        while len(priority_q) > 0:
            # dequeue shortest path
            v_tuple = priority_q.popleft()
            v_len = v_tuple[0]
            vertex = v_tuple[1]
            if vertex not in visited:
                visited[vertex] = v_len

                index = 0
                for edge in matrix[vertex]:
                    if edge > 0:
                        priority_q.append((edge + v_len, index))
                    index += 1
                # sort priority queue
                to_list = list(priority_q)
                to_list.sort()
                priority_q = deque(to_list)

        paths = list()
        for vertex in range(size):
            if vertex not in visited:
                visited[vertex] = float('inf')
            paths.append(visited[vertex])

        return paths



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
