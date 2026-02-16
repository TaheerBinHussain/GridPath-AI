# GridPath-AI
This project has BFS, DFS, UCS, DLS, IDDFS, and Bidirectional searches implemented to find a set goal in the grid visually shown using python GUI library (tkinter).


A GUI-based tool to visualize uninformed search algorithms in a 2D grid.

Implemented Algorithms:-

Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform-Cost Search (UCS).
Depth-Limited Search (DLS), Iterative Deepening DFS (IDDFS), and Bidirectional Search.

Expansion Order: All algorithms follow a strict clockwise sequence: Up, Right, Bottom, Bottom-Right (Diagonal), Left, and Top-Left (Diagonal).

Constraints: Top-Right and Bottom-Left diagonals are strictly ignored.

Setup and Installation:-

Prerequisites: Ensure Python 3.x is installed.
Libraries: This tool uses Tkinter.
Windows: Included by default.
macOS: brew install python-tk
Linux: sudo apt-get install python3-tk
Run: Execute python main.py in your terminal.

Visual Key:-

🟠 Orange: Frontier nodes waiting in the queue or stack.
🔵 Blue: Explored nodes already visited by the algorithm.
🟡 Yellow: The final successful path from Start to Target.

