import heapq

# ------------------------
# Dijkstra Traffic Routing
# ------------------------
class TrafficSignalDijkstra:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start_node):
        pq = [(0, start_node)]
        shortest_path = {node: float('inf') for node in self.graph}
        shortest_path[start_node] = 0
        previous_nodes = {}

        while pq:
            current_cost, current_node = heapq.heappop(pq)

            for neighbor, weight in self.graph[current_node]:
                distance = current_cost + weight
                if distance < shortest_path[neighbor]:
                    shortest_path[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return shortest_path, previous_nodes

    def find_optimal_signal_path(self, start_node, end_node):
        shortest_path, previous_nodes = self.dijkstra(start_node)
        path = []
        while end_node:
            path.append(end_node)
            end_node = previous_nodes.get(end_node)
        return path[::-1], shortest_path[path[0]]


# ------------------------
# Traffic Signal Controller
# ------------------------
def decide_signals(detection_output):
    lanes = detection_output['lanes']
    ambulance = detection_output['ambulance_detected']

    signal_plan = {
        'left': {'status': 'red', 'time': 0},
        'center': {'status': 'red', 'time': 0},
        'right': {'status': 'red', 'time': 0}
    }
    # 🚦 Normal mode: Find lane with highest density
    max_lane = max(lanes, key=lanes.get)
    max_count = lanes[max_lane]
    
    # New dynamic green time logic
    base_time = 10           # start at 10 seconds minimum
    per_vehicle_time = 2.5   # add time based on density
    max_green_time = 60      # cap to avoid starvation
    
    green_time = min(int(base_time + per_vehicle_time * max_count), max_green_time)
    
    # Assign signal
    signal_plan[max_lane]['status'] = 'green'
    signal_plan[max_lane]['time'] = green_time


    if ambulance:
        # Use Dijkstra to prioritize the best lane path for ambulance
        traffic_graph = {
            "left": [("center", 5), ("right", 7)],
            "center": [("left", 6), ("right", 8), ("EV_Clearance", 2)],
            "right": [("left", 7), ("center", 5)],
            "EV_Clearance": []
        }

        dijkstra_model = TrafficSignalDijkstra(traffic_graph)
        path, cost = dijkstra_model.find_optimal_signal_path("center", "EV_Clearance")

        # Set path lanes to green
        for lane in path:
            if lane in signal_plan:
                signal_plan[lane]['status'] = 'green'
                signal_plan[lane]['time'] = 15  # You can tune this

        return signal_plan

    # Normal mode: highest density lane gets green
    if not lanes:
        return signal_plan  # all red fallback

    max_lane = max(lanes, key=lanes.get)
    max_count = lanes[max_lane]
    
    base_time = 10           # increase base time
    per_vehicle_time = 2.5   # more time per vehicle
    # Cap green time for demo visibility
    max_green_time = 60
    green_time = min(base_time + int(per_vehicle_time * max_count), max_green_time)

    # base_time = 5
    # per_vehicle_time = 1.5
    # green_time = int(base_time + per_vehicle_time * max_count)

    signal_plan[max_lane]['status'] = 'green'
    signal_plan[max_lane]['time'] = green_time

    return signal_plan


# 🔍 Quick test
if __name__ == "__main__":
    test_output = {
        'lanes': {'left': 10, 'center': 12, 'right': 5},
        'ambulance_detected': True
    }

    signals = decide_signals(test_output)
    print("🚦 Signal Plan:", signals)
