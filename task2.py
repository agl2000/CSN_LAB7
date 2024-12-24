import matplotlib.pyplot as plt
#import lab7.py
from lab7 import create_graphs, sis_simulation, default_n, default_gamma, default_p0, default_timesteps, leading_eigenvalue

# Task 2: Epidemic Threshold Analysis
def task2(graphs, gamma, timesteps):
    """
    Analyze the epidemic threshold for each network type.
    
    Args:
        graphs: Dictionary of graph types.
        gamma: Recovery probability.
        timesteps: Number of time steps to simulate.
    """
    for name, G in graphs.items():
        print(f"\nAnalyzing Epidemic Threshold for {name}...")

        # Compute the leading eigenvalue
        eigenvalue = leading_eigenvalue(G)

        # Compute the epidemic threshold
        critical_beta = gamma / eigenvalue
        print(f"Critical β for {name}: {critical_beta:.4f}")

        # Choose β values slightly below and above the threshold
        beta_below = critical_beta * 0.9
        beta_above = critical_beta * 1.1

        print(f"Testing β below threshold: {beta_below:.4f}")
        print(f"Testing β above threshold: {beta_above:.4f}")

        # Simulate with β below the threshold
        infected_below = sis_simulation(G, beta_below, gamma, default_p0, timesteps)
        # Simulate with β above the threshold
        infected_above = sis_simulation(G, beta_above, gamma, default_p0, timesteps)

        # Plot results
        plt.plot(range(timesteps + 1), infected_below, label=f"{name} (β below)")
        plt.plot(range(timesteps + 1), infected_above, label=f"{name} (β above)")

        print("Summary of results:")
        print(f"  Final proportion of infected nodes (β below): {infected_below[-1]:.4f}")
        print(f"  Final proportion of infected nodes (β above): {infected_above[-1]:.4f}")

    # Finalize the plot
    plt.xlabel("Time Step")
    plt.ylabel("Proportion of Infected Nodes")
    plt.title("Epidemic Threshold Analysis")
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()

# Run Task 2 if this script is executed directly
if __name__ == "__main__":
    # Create graphs
    graphs = create_graphs(default_n)
    # Perform Task 2
    task2(graphs, default_gamma, default_timesteps)
