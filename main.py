import tkinter as tk
import sys
import TSPBruteforce
import TSPConvexHull
import TSPdwave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TSPSolver(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TSP Solver")

        self.mainframe = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.num_nodes = tk.StringVar(self)
        tk.Label(self.mainframe, text="Number of nodes:").grid(column=2, row=1, sticky=tk.E)
        self.node_entry = tk.Entry(self.mainframe, width=7, textvariable=self.num_nodes)
        self.node_entry.grid(column=3, row=1, sticky=tk.W)


        tk.Button(self.mainframe, text="Run Brute Force", command=self.run_bruteforce).grid(column=1, row=2, sticky=tk.W+tk.E)
        
        self.bruteforce_output_label = tk.Label(self.mainframe, text="")
        self.bruteforce_output_label.grid(column=1, row=6, sticky=tk.W+tk.E)

        tk.Button(self.mainframe, text="Run Greedy Insertion", command=self.run_greedy).grid(column=2, row=2, sticky=tk.W+tk.E)
        
        self.greedy_output_label = tk.Label(self.mainframe, text="", wraplength=800)
        self.greedy_output_label.grid(column=2, row=6, sticky=tk.W+tk.E)

        tk.Button(self.mainframe, text="Run Quantum Annealed", command=self.run_quantum).grid(column=3, row=2, sticky=tk.W+tk.E)
        
        self.quantum_output_label = tk.Label(self.mainframe, text="")
        self.quantum_output_label.grid(column=3, row=6, sticky=tk.W+tk.E)

        tk.Button(self.mainframe, text="Run Sim Quantum Annealed", command=self.run_quantum_sim).grid(column=4, row=2, sticky=tk.W+tk.E)

        self.quantum_sim_output_label = tk.Label(self.mainframe, text="")
        self.quantum_sim_output_label.grid(column=4, row=6, sticky=tk.W+tk.E)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(1, 4, figsize=(20, 5))
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.95)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        self.canvas.get_tk_widget().grid(column=1, row=4, columnspan=4, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.node_array = None
        self.last_num_nodes = None

    def create_and_get_nodes(self, num_nodes):
        if self.node_array is None or self.last_num_nodes != num_nodes:
            self.node_array = TSPBruteforce.create_nodes(num_nodes)
            self.last_num_nodes = num_nodes
        return self.node_array
    
    def run_bruteforce(self):
        try:
            nodes = int(self.num_nodes.get())
            print(f"Number of nodes: {nodes}")
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of nodes.")
            return
        self.bruteforce_output_label.config(text="")
        self.ax1.clear()
        self.canvas.draw()
        node_array = self.create_and_get_nodes(nodes)
        dist_mat = TSPBruteforce.create_distance_matrix(node_array)
        bestPerm, bestLength = TSPBruteforce.brute_force(node_array, dist_mat)

        
        TSPBruteforce.draw_graph(node_array, bestPerm, bestLength, True, self.fig, self.ax1)
        #self.bruteforce_canvas.draw()  # Redraw the canvas
        self.bruteforce_output_label.config(text=f"Tour: {bestPerm}")

    def run_greedy(self):
        try:
            nodes = int(self.num_nodes.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of nodes.")
            return
        self.greedy_output_label.config(text="")
        self.ax2.clear()
        self.canvas.draw()
        node_array = self.create_and_get_nodes(nodes)
        tour, tour_indices = TSPConvexHull.greedy_insertion(node_array)

        dist_mat = TSPBruteforce.create_distance_matrix(node_array)
        tourLength = TSPBruteforce.calculateLength(dist_mat, tour_indices)
        
        TSPConvexHull.draw_graph(node_array, tour, tourLength, True, self.fig, self.ax2)
        #self.greedy_canvas.draw()  # Redraw the canvas
        if len(tour_indices) > 150:
            tour_indices = tour_indices[:150]
            tour_indices.append("...")
        
        self.greedy_output_label.config(text=f"Tour: {tour_indices}")

    def run_quantum(self):
        try:
            nodes = int(self.num_nodes.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of nodes.")
            return
        self.quantum_output_label.config(text="")
        self.ax3.clear()
        self.canvas.draw()
        node_array = self.create_and_get_nodes(nodes)
        dist_mat = TSPBruteforce.create_distance_matrix(node_array)
        nodesNum = len(node_array)

        tourIndices = TSPdwave.solve(nodesNum, dist_mat, False)

        if tourIndices != None:
            tour = [node_array[i] for i in tourIndices]
            tourLength = TSPBruteforce.calculateLength(dist_mat, tourIndices)
            self.quantum_output_label.config(text=f"Tour: {tourIndices}")
            TSPConvexHull.draw_graph(node_array, tour, tourLength, True, self.fig, self.ax3)
        else:
            tourLength = "Null"
            self.quantum_output_label.config(text="No valid tour found")
            
    def run_quantum_sim(self):
        try:
            nodes = int(self.num_nodes.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of nodes.")
            return
        self.quantum_output_label.config(text="")
        self.ax3.clear()
        self.canvas.draw()
        node_array = self.create_and_get_nodes(nodes)
        dist_mat = TSPBruteforce.create_distance_matrix(node_array)
        nodesNum = len(node_array)

        tourIndices = TSPdwave.solve(nodesNum, dist_mat, True)


        if tourIndices != None:
            tour = [node_array[i] for i in tourIndices]
            tourLength = TSPBruteforce.calculateLength(dist_mat, tourIndices)
            self.quantum_sim_output_label.config(text=f"Tour: {tourIndices}")
            TSPConvexHull.draw_graph(node_array, tour, tourLength, True, self.fig, self.ax4)
        else:
            tourLength = "Null"
            self.quantum_output_label.config(text="No valid tour found")

        

        

    def on_closing(self):   
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = TSPSolver()
    app.mainloop()

