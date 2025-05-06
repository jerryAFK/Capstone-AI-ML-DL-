import heapq

class TrafficSignalDijkstra:
    def _init_(self, graph):
        self.graph = graph  # Graph of traffic signal transitions

    def dijkstra(self, start_node):
        # Priority queue for selecting the minimum cost node
        pq = [(0, start_node)]  # (cost, node)
        shortest_path = {node: float('inf') for node in self.graph}
        shortest_path[start_node] = 0
        previous_nodes = {}

        while pq:
            current_cost, current_node = heapq.heappop(pq)

            # Process neighbors
            for neighbor, weight in self.graph[current_node]:
                distance = current_cost + weight
                if distance < shortest_path[neighbor]:
                    shortest_path[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return shortest_path, previous_nodes

    def find_optimal_signal_path(self, start_node, end_node):
        shortest_path, previous_nodes = self.dijkstra(start_node)

        # Trace the path from end node to start node
        path = []
        while end_node:
            path.append(end_node)
            end_node = previous_nodes.get(end_node)
        return path[::-1], shortest_path[path[0]]

# Define the traffic graph (signal states with transition costs)
traffic_graph = {
    "A_Green": [("B_Green", 5), ("C_Green", 7)],
    "B_Green": [("A_Green", 6), ("C_Green", 8), ("EV_Clearance", 2)],  # Emergency vehicle path
    "C_Green": [("A_Green", 7), ("B_Green", 5)],
    "EV_Clearance": [("A_Green", 3)]
}

# Initialize Dijkstra-based traffic control
traffic_control = TrafficSignalDijkstra(traffic_graph)

# Find the best sequence (starting from "A_Green" to "EV_Clearance")
optimal_path, min_wait_time = traffic_control.find_optimal_signal_path("A_Green", "EV_Clearance")

print("Optimal Traffic Signal Sequence:", optimal_path)
print("Minimum Waiting Time:", min_wait_time)