from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Real-world Logistics Data
# Node Format: { id: { name: str, type: str, pos: [x, y] } }
AIRPORT_MAP = {
    0: {"name": "Main Check-In", "type": "origin", "pos": [50, 225]},
    1: {"name": "Security Scan A", "type": "process", "pos": [200, 100]},
    2: {"name": "Security Scan B", "type": "process", "pos": [200, 350]},
    3: {"name": "Central Sorter", "type": "hub", "pos": [400, 225]},
    4: {"name": "Gate 1-10 (North)", "type": "gate", "pos": [600, 80]},
    5: {"name": "Gate 11-20 (South)", "type": "gate", "pos": [600, 370]},
    6: {"name": "International Pier", "type": "gate", "pos": [750, 225]}
}

# Graph Edges: (Source, Target, Weight/Distance)
EDGES = [
    (0, 1, 10), (0, 2, 12), (1, 3, 15), (2, 3, 15),
    (3, 4, 20), (3, 5, 20), (3, 6, 25), (4, 6, 10), (5, 6, 10)
]

def get_dijkstra(start, end):
    adj = {i: [] for i in AIRPORT_MAP}
    for u, v, w in EDGES:
        adj[u].append((v, w))
        adj[v].append((u, w)) # Bi-directional belts

    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited: continue
        
        path = path + [node]
        if node == end: return path, cost
        
        visited.add(node)
        for neighbor, weight in adj[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return [], 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config')
def config():
    return jsonify({"nodes": AIRPORT_MAP, "edges": EDGES})

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    path, cost = get_dijkstra(int(data['start']), int(data['end']))
    return jsonify({"path": path, "cost": cost})

if __name__ == '__main__':
    app.run(debug=True, port=5000)