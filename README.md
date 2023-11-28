# quantum-tsp

Made as part of my dissertation research.

This program allows you to benchmark and visualise the differences between 4 methods for solving the travelling salesman problem (TSP).

These methods are:
* Classical bruteforce
* Greedy convex hull (heuristic)
* Simulated quantum anneal
* Quantum anneal

The quantum computation relies on using D-Wave Systems Quantum Annealers.

# Install instructions (Linux)

1. `git clone https://github.com/Aurux/quantum-tsp.git`
2. `cd quantum-tsp`
3. `python3.11 -m venv ./venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `export DWAVE_API_KEY="YOUR_API_KEY"` You must get this from D-Wave systems in order to utilise their solvers.
7. `python main.py`

If all goes well you should be greeted by a window like the one below.


![image](https://github.com/Aurux/quantum-tsp/assets/38943986/6eb25e68-2036-41a1-9b16-042f566d8665)
