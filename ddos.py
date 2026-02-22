import random
import threading
import time
from collections import defaultdict
import matplotlib.pyplot as plt

RATE_LIMIT_ENABLED = True
RATE_LIMIT = 10
NODE_BANDWIDTH_CAPACITY = 50
SIMULATION_REQUESTS = 200

nodes = {
    "Node-A (US)": {"requests_per_ip": defaultdict(int), "total_requests": 0, "allowed": 0, "blocked": 0, "bandwidth_used": 0, "overloaded": False},
    "Node-B (EU)": {"requests_per_ip": defaultdict(int), "total_requests": 0, "allowed": 0, "blocked": 0, "bandwidth_used": 0, "overloaded": False},
    "Node-C (Asia)": {"requests_per_ip": defaultdict(int), "total_requests": 0, "allowed": 0, "blocked": 0, "bandwidth_used": 0, "overloaded": False},
}

ips = ["192.168.1.10", "10.0.0.5", "172.16.0.3", "203.0.113.99"]

allowed_history = []
blocked_history = []

def handle_request(ip):
    node_name = random.choice(list(nodes.keys()))
    node = nodes[node_name]

    if node["overloaded"]:
        return

    node["total_requests"] += 1
    node["bandwidth_used"] += 1

    if node["bandwidth_used"] >= NODE_BANDWIDTH_CAPACITY:
        node["overloaded"] = True
        return

    if RATE_LIMIT_ENABLED:
        node["requests_per_ip"][ip] += 1
        if node["requests_per_ip"][ip] > RATE_LIMIT:
            node["blocked"] += 1
            return

    node["allowed"] += 1

def simulate():
    for _ in range(SIMULATION_REQUESTS):
        ip = random.choices(ips, weights=[1,1,1,8], k=1)[0]
        handle_request(ip)

        total_allowed = sum(n["allowed"] for n in nodes.values())
        total_blocked = sum(n["blocked"] for n in nodes.values())

        allowed_history.append(total_allowed)
        blocked_history.append(total_blocked)

        time.sleep(0.01)

print("\n=== Simulating Distributed Traffic ===\n")

simulate()

total_allowed = sum(n["allowed"] for n in nodes.values())
total_blocked = sum(n["blocked"] for n in nodes.values())

print("\n=== PER NODE STATISTICS ===\n")

for name, node in nodes.items():
    print(name)
    print(f"  Total Requests: {node['total_requests']}")
    print(f"  Allowed: {node['allowed']}")
    print(f"  Blocked: {node['blocked']}")
    print(f"  Bandwidth Used: {node['bandwidth_used']}")
    print(f"  Overloaded: {node['overloaded']}\n")

print("=== GLOBAL SUMMARY ===")
print(f"Total Allowed Requests: {total_allowed}")
print(f"Total Blocked Requests: {total_blocked}")
print(f"Rate Limiting Enabled: {RATE_LIMIT_ENABLED}")
print("\nSimulation Complete.\n")

plt.plot(allowed_history)
plt.plot(blocked_history)
plt.xlabel("Requests Over Time")
plt.ylabel("Count")
plt.title("DDoS Defense Simulation")
plt.show()