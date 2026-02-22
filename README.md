DDoS Defense Simulation : (What Happens Under Attack)

i built a Python model to simulate a distributed DDoS attack on multiple nodes:
* Multiple global nodes handle incoming traffic.
* Malicious IPs flood requests heavily, legitimate IPs continue normally.
* Per-node rate limiting blocks excessive requests.
* Bandwidth exhaustion triggers node overloads.

Simulation Results:
 90 malicious requests blocked
 Nodes eventually overloaded under sustained traffic
 Shows how defenses slow attacks but architecture determines survival.
