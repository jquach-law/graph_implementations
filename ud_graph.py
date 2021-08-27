# Course: CS261 - Data Structures
# Author: Justin Quach-Law
# Assignment: Assignment 6 - Portfolio Project
# Description: An undirected graph class with methods to add, remove and get vertices and edges.
# It also performs depth-first search, breadth-first search and checks if graph is cyclic.

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = list()

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return

        # if vertex dont exist
        if u not in self.adj_list:
            self.adj_list[u] = list()
        if v not in self.adj_list:
            self.adj_list[v] = list()

        # if edge dont exist
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # if vertex dont exist
        if v not in self.adj_list:
            return
        if u not in self.adj_list:
            return

        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)
        if u in self.adj_list[v]:
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return

        # list of connected edges
        list_edge = self.adj_list[v]

        # in connect edges, remove given vertex, v
        for pair in list_edge:
            self.adj_list[pair].remove(v)

        # remove vertex
        self.adj_list.pop(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list)

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        check = list()
        lst_edges = list()

        for vertex in self.adj_list:
            for neighbor in self.adj_list[vertex]:
                if (str(vertex), neighbor) not in check:
                    lst_edges.append((str(vertex), neighbor))
                    check.append((neighbor, str(vertex)))

        return lst_edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # if empty path
        if len(path) == 0:
            return True

        # initial vertex
        try:
            vertex = self.adj_list[path[0]]
        except:
            return False

        # find next vertex
        pos = 1
        while pos < len(path):
            if path[pos] in vertex:
                vertex = self.adj_list[path[pos]]
                pos += 1
            else:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        visited = list()
        lst_vertices = list(self.adj_list)
        if v_start not in lst_vertices:
            return visited

        stack = deque(list())
        stack.append(v_start)
        while len(stack) > 0:
            pick = stack.pop()
            if pick not in visited:
                visited.append(pick)
                if pick == v_end:
                    return visited

                # sorting successors in ascending order
                to_sort = list()
                for successor in self.adj_list[pick]:
                    to_sort.append(successor)
                to_sort.sort()
                # appending popped succesors, creating descending order to stack
                # (thus pop from stack in ascending order)
                while len(to_sort) > 0:
                    stack.append(to_sort.pop())

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited = list()
        lst_vertices = list(self.adj_list)
        if v_start not in lst_vertices:
            return visited

        queue = deque(list())
        queue.append(v_start)
        while len(queue) > 0:
            pick = queue.popleft()
            visited.append(pick)
            if pick == v_end:
                return visited

            to_sort = list()
            for successor in self.adj_list[pick]:
                to_sort.append(successor)
            to_sort.sort()

            for sorted_successor in to_sort:
                if sorted_successor not in visited:
                    if sorted_successor not in queue:
                        queue.append(sorted_successor)

        return visited

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        count = 0
        lst_vertices = list(self.adj_list)
        while len(lst_vertices) > 0:
            start = lst_vertices[0]
            component = self.bfs(start)
            count += 1
            for vertex in component:
                if vertex in lst_vertices:
                    lst_vertices.remove(vertex)
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        index = 0
        lst_vertices = list(self.adj_list)
        while index < len(lst_vertices):

            visited = list()
            stack = deque(list())
            first = lst_vertices[index]
            excluded_first = False
            # if list is not empty, else
            try:
                second = min(self.adj_list[first])
            except:
                index += 1
                continue

            stack.append(second)
            while len(stack) > 0:
                pick = stack.pop()
                if pick not in visited:
                    visited.append(pick)
                    if pick == first:
                        return True
                    # sorting successors in ascending order
                    to_sort = list()
                    for successor in self.adj_list[pick]:
                        to_sort.append(successor)
                    to_sort.sort()

                    # excluding first from stack
                    if excluded_first is False:
                        to_sort.remove(first)
                        excluded_first = True

                    # appending popped succesors, creating descending order to stack
                    # (thus pop from stack in ascending order)
                    while len(to_sort) > 0:
                        stack.append(to_sort.pop())

            index += 1

        return False



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    print(g)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
