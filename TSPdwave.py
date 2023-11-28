import numpy as np
from dwave.system import DWaveSampler, FixedEmbeddingComposite
from minorminer import find_embedding
from dimod import BinaryQuadraticModel
from dwave.inspector import show
from neal import SimulatedAnnealingSampler
import time

def is_valid_tour(tour):
    visited = set()
    zero_count = 0
    for node in tour:
        if node in visited:
            return False
        visited.add(node)

        # Count the occurrences of point zero
        if node == 0:
            zero_count += 1

    # Check if the tour goes through point zero more than once
    if zero_count > 1:
        return False
    return True


def tour_distance(tour, D):
    distance = 0
    for i in range(len(tour) - 1):
        distance += D[tour[i], tour[i + 1]]
    return distance

def solve(n, D, simulate):
    # n = number of nodes
    # D = distance matrix
    
    # Create an empty QUBO matrix
    Q = np.zeros((n**2, n**2))

    # Define the objective function
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != k:
                    Q[n*i+j, n*i+k] += D[j, k]
                    Q[n*j+i, n*k+i] += D[j, k]

    # Add constraints to ensure that each node is visited exactly once
    A = 0.05 * n  # Constraint scaling factor
    #A = 1
    for i in range(n):
        for j in range(n):
            Q[n*i+j, n*i+j] -= 2 * A
            for k in range(n):
                if j != k:
                    Q[n*i+j, n*i+k] += 2 * A

    # Add constraints to ensure that there are no sub-tours
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                Q[n*i, n*j] += (n - 2) * A
                Q[n*j, n*i] += (n - 2) * A
                Q[n*i, n*j+1:n**2:1] -= 2 * A
                Q[n*j+1:n**2:n, n*i] -= 2 * A

    # Add constraint to ensure that the tour returns to the starting node
    for i in range(n):
        for j in range(n):
            if i != j:
                Q[n*i+j, n*(n-1)+i] += D[j, 0]

    # Add constraint to ensure that point 0 is visited only once
    #for i in range(n):
    #    if i != 0:
    #        Q[0, n*i] += A



   

    # Normalise the QUBO
    Q = Q / np.max(Q)

    # Convert the QUBO matrix to a symmetric QUBO matrix - needed to run on quantum annealer.
    Q = Q + Q.T - np.diag(np.diag(Q))
    

    annealStart = time.time()
    if simulate:
        sampler = SimulatedAnnealingSampler()
        response = sampler.sample_qubo(Q, num_reads=(200 * n))
        annealEnd = time.time()
    else:
        # Create a sampler
        
        #solver = 'DW_2000Q_6'
        #solver = 'Advantage_system6.1'
        solver = 'Advantage2_prototype1.1'
        sampler = DWaveSampler(solver=solver)
        
        # Create a BinaryQuadraticModel from the QUBO matrix
        bqm = BinaryQuadraticModel.from_qubo(Q)

        # Convert the BinaryQuadraticModel to a graph (dictionary representation)
        graph = bqm.to_networkx_graph()

        # Find an embedding
        embedding = find_embedding(graph, sampler.edgelist, tries=50, chainlength_patience=5)

        # Create the FixedEmbeddingComposite sampler
        sampler_embedded = FixedEmbeddingComposite(sampler, embedding)

        # Submit the QUBO matrix to the sampler
        task_label = "TSP Solver - "+str(n)+" nodes"
        response = sampler_embedded.sample_qubo(Q, label=task_label, num_reads=(2000), chain_strength=25)
        annealEnd = time.time()
        # Show solution explorer
        show(response)

    
    print("Quantum anneal took", (annealEnd-annealStart), "seconds!")

    postStart = time.time()
    # Initialize the shortest tour and its distance
    shortest_tour = None
    shortest_tour_distance = np.Infinity

    # Iterate over all solutions in the response
    for solution in response.samples():
        # Find first node
        start = None
        for i in range(n):
            if solution[n*i] == 1:
                start = i
                break
        
        # If start is not found, continue to the next solution
        if start is None:
            continue

        # Construct the tour starting from node 0
        tour = [0] * n
        for i in range(n):
            for j in range(n):
                if solution[n*((i+start)%n)+j] == 1: # Wrap around QUBO and if value if QUBO index = 1 then node was visited
                    tour[i] = j

        

        # Check if the tour is valid
        if is_valid_tour(tour):
            
            current_tour_distance = tour_distance(tour, D)

            # Update the shortest tour and its distance
            if current_tour_distance < shortest_tour_distance:
                shortest_tour = tour
                shortest_tour_distance = current_tour_distance
                

    
            

    postEnd = time.time()
    print("Solution checking took", (postEnd-postStart), "seconds!")

    return shortest_tour

