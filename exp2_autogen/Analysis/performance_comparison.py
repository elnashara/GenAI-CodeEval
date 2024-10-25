import matplotlib.pyplot as plt
import os

class PerformanceComparison:
    def __init__(self, systems, success_rates, error_counts):
        """
        Initialize the class with data for systems, success rates, and error counts.
        """
        self.systems = systems
        self.success_rates = success_rates
        self.error_counts = error_counts

    def plot_success_rate_comparison(self):
        """
        Plot and save a comparison chart for success rates with a font size of 20 for axes labels and values.
        """
        # Ensure the 'data' directory exists
        output_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        # Create the comparison chart for success rates
        plt.figure(figsize=(8, 6))
        plt.bar(self.systems, self.success_rates, color=['blue', 'orange'])
        plt.title('Comparison of Success Rates: AutoGen vs. GPT-4', fontsize=20)
        plt.xlabel('Systems', fontsize=20)
        plt.ylabel('Success Rate (%)', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(0, 100)

        # Save the comparison chart
        comparison_chart_path = os.path.join(output_dir, 'autogen_vs_GPT-4_success_rate_comparison.png')
        plt.savefig(comparison_chart_path)
        plt.close()

        # Return the saved chart path
        return comparison_chart_path

    def plot_success_and_error_comparison(self):
        """
        Plot side-by-side comparison charts for success rates and error counts with a font size of 20 for axes labels and values.
        """
        # Create subplots for success rates and error counts
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Plotting Success Rates
        axes[0].bar(self.systems, self.success_rates, color=['blue', 'green'])
        # axes[0].set_title('Success Rates Comparison', fontsize=20)
        axes[0].set_xlabel('Systems', fontsize=20)
        axes[0].set_ylabel('Success Rate (%)', fontsize=20)
        axes[0].set_xticklabels(self.systems, fontsize=20)
        axes[0].tick_params(axis='y', labelsize=20)
        axes[0].set_ylim(0, 100)

        # Plotting Error Counts
        axes[1].bar(self.systems, self.error_counts, color=['red', 'orange'])
        # axes[1].set_title('Error Counts Comparison', fontsize=20)
        axes[1].set_xlabel('Systems', fontsize=20)
        axes[1].set_ylabel('Number of Errors', fontsize=20)
        axes[1].set_xticklabels(self.systems, fontsize=20)
        axes[1].tick_params(axis='y', labelsize=20)
        axes[1].set_ylim(0, max(self.error_counts) + 10)

        # Adjust layout and display the plots
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    systems = ['AutoGen', 'GPT-4o']
    success_rates = [93.6, 92.8]
    error_counts = [21, 18]

    # Create an instance of the class
    comparison = PerformanceComparison(systems, success_rates, error_counts)

    # Plot and save the success rate comparison chart
    success_chart_path = comparison.plot_success_rate_comparison()
    print(f"Success rate comparison chart saved at: {success_chart_path}")

    # Plot success rates and error counts side by side
    comparison.plot_success_and_error_comparison()
