import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Define the nodes (components)
components = [
    "Main Window (Tkinter)",
    "Input: Target URL",
    "Input: Wordlist Selection",
    "Input: Proxy Settings",
    "Input: Threads Number",
    "Input: Status Code Filter",
    "Input: Custom User-Agent",
    "Buttons: Run, Stop, Clear, Save",
    "Output: Colored Results Display",
    "Threading",
    "Enumeration Logic",
    "File Handling (Save/Load)"
]

# Add nodes to the graph
G.add_nodes_from(components)

# Define the edges (connections between components)
edges = [
    ("Main Window (Tkinter)", "Input: Target URL"),
    ("Main Window (Tkinter)", "Input: Wordlist Selection"),
    ("Main Window (Tkinter)", "Input: Proxy Settings"),
    ("Main Window (Tkinter)", "Input: Threads Number"),
    ("Main Window (Tkinter)", "Input: Status Code Filter"),
    ("Main Window (Tkinter)", "Input: Custom User-Agent"),
    ("Main Window (Tkinter)", "Buttons: Run, Stop, Clear, Save"),
    ("Buttons: Run, Stop, Clear, Save", "Enumeration Logic"),
    ("Enumeration Logic", "Threading"),
    ("Enumeration Logic", "Output: Colored Results Display"),
    ("Enumeration Logic", "File Handling (Save/Load)"),
    ("Threading", "Enumeration Logic")
]

# Add edges to the graph
G.add_edges_from(edges)

# Set the layout of the graph
pos = nx.spring_layout(G)

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', node_shape='o')

# Draw the edges
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black')

# Draw the labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Set the title
plt.title("Concept Diagram: Web Enumeration Tool", fontsize=16)

# Display the diagram
plt.axis('off')  # Turn off the axis
plt.show()
