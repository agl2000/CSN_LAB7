import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
default_n = 1000  # Number of nodes
default_beta = 0.05  # Infection probability
default_gamma = 0.2  # Recovery probability
default_p0 = 0.1  # Initial infection fraction
default_timesteps = 200  # Number of simulation steps

# SIS Simulation Function
def sis_simulation(G, beta, gamma, p0, timesteps):
    """
    Simulate the SIS model on a graph.

    Args:
        G: NetworkX graph.
        beta: Infection probability.
        gamma: Recovery probability.
        p0: Initial infection probability.
        timesteps: Number of time steps to simulate.

    Returns:
        infected_over_time: List of proportions of infected nodes over time.
    """
    n = len(G.nodes())
    infected = set(random.sample(list(G.nodes()), int(p0 * n)))  # Initial infected nodes
    infected_over_time = [len(infected) / n]

    for t in range(timesteps):
        new_infected = set()
        recovered = set()

        # Infection step
        for node in infected:
            for neighbor in G.neighbors(node):
                if neighbor not in infected and random.random() < beta:
                    new_infected.add(neighbor)

        # Recovery step
        for node in infected:
            if random.random() < gamma:
                recovered.add(node)

        # Update infected list
        infected.update(new_infected)
        infected.difference_update(recovered)

        # Record proportion of infected nodes
        infected_over_time.append(len(infected) / n)

    return infected_over_time

# Graph Models
def create_graphs(n):
    """Create various network models."""
    graphs = {
        "Erdos-Renyi": nx.erdos_renyi_graph(n, 0.05),
        "Barabasi-Albert": nx.barabasi_albert_graph(n, 5),
        "Watts-Strogatz": nx.watts_strogatz_graph(n, 10, 0.1),
        "Complete Graph": nx.complete_graph(n),
        "Tree": nx.random_tree(n),
        "Regular Lattice": nx.grid_2d_graph(int(np.sqrt(n)), int(np.sqrt(n))),
        "Star": nx.star_graph(n - 1),
    }
    return graphs


# Compute Leading Eigenvalue
def leading_eigenvalue(G):
    """Calculate the leading eigenvalue of the adjacency matrix of a graph."""
    adjacency_matrix = nx.adjacency_matrix(G).todense()
    eigenvalues = np.linalg.eigvals(adjacency_matrix)
    return max(np.abs(eigenvalues))



# Task 1: Simulation and Plotting
def task1(beta, gamma, p0, timesteps):
    graphs = create_graphs(default_n)

    # #make a graphical plot of the created graphs
    # plt.figure(figsize=(12, 8))
    # plt.suptitle("Graph Models")
    # for i, (name, G) in enumerate(graphs.items(), start=1):
    #     plt.subplot(2, 4, i)
    #     plt.title(name)
    #     nx.draw(G, node_size=10)
    # plt.tight_layout()
    # plt.show()


    results = {}



    for name, G in graphs.items():
        print(f"\n Simulating SIS model on {name}...")
        infected_over_time = sis_simulation(G, beta, gamma, p0, timesteps)
        results[name] = infected_over_time

        # Plot
        plt.plot(range(timesteps + 1), infected_over_time, label=name)

        # Compute and display leading eigenvalue
        eigenvalue = leading_eigenvalue(G)
        print(f"Leading eigenvalue of {name}: {eigenvalue:.4f}")
        print(f"Epidemic threshold for {name}: {gamma / beta:.4f}")
        #now print beta*lambda
        print(f"beta*lambda for {name}: {beta*eigenvalue:.4f}")
        print("Is",beta,"*",eigenvalue,">",gamma,"?")
        if(beta*eigenvalue>gamma):
            print(f"YES, Graph {name} is epidemic")
        else:
            print(f"NO, Graph {name} is not epidemic")
        
        print("Critical value for beta is",1/eigenvalue)

    plt.xlabel("Time Step")
    plt.ylabel("Proportion of Infected Nodes")
    plt.title("SIS Model Simulation")
    #legend on the bottom right
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()

    return results

# Run Task 1 if this script is executed directly
if __name__ == "__main__":
    task1_results = task1(default_beta, default_gamma, default_p0, default_timesteps)
