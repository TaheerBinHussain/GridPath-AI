import tkinter as tk
from collections import deque
import heapq
import time


moves = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]

class App:
    def __init__(self, win):
        self.win = win
        self.win.title("Search Algo GUI")
        
        self.rows = 10
        
        self.cols = 10
        self.size = 40
        
        self.map = [] 
        for i in range(self.rows):
            temp = []
        
            for j in range(self.cols):
                temp.append(0)
        
            self.map.append(temp)
            
        
        self.boxes = {} 
        self.start = (1, 1) 
        
        self.end = (8, 8)
        
        self.walls = []
        
        for i in range(2, 8):
            self.walls.append((5, i))
        
        self.choice = tk.StringVar(value="BFS")
        
        self.running = False
        
        self.depth_lim = 1 
        
        self.make_gui()

    def make_gui(self):
        
        w = self.rows * self.size
        h = self.cols * self.size
        self.canvas = tk.Canvas(self.win, width=w, height=h, bg="white")
        
        self.canvas.pack() 
        
        frame = tk.Frame(self.win)
        frame.pack()
        
        
        opts = ["BFS", "DFS", "UCS", "DLS", "IDDFS", "Bidirectional"]
        
        tk.Label(frame, text="Algo:").pack(side=tk.LEFT)
        
        tk.OptionMenu(frame, self.choice, *opts).pack(side=tk.LEFT)
        tk.Button(frame, text="GO", command=self.run).pack(side=tk.LEFT)
        tk.Button(frame, text="RESET", command=self.restart).pack(side=tk.LEFT)

        
        self.draw_boxes()

    def draw_boxes(self):
        
        for r in range(self.rows):
            for c in range(self.cols):
                c_color = "white"


                if (r,c) == self.start:
        
                    c_color = "green"
                elif (r,c) == self.end:
                    c_color = "blue"
        
                elif (r,c) in self.walls: 
                    c_color = "red"
        
                    self.map[r][c] = 1 

        
                x1 = c * self.size
                y1 = r * self.size
        
                x2 = x1 + self.size
                y2 = y1 + self.size


                b = self.canvas.create_rectangle(x1, y1, x2, y2, fill=c_color, outline="gray")
                self.boxes[(r, c)] = b

    def run(self):
        if self.running == True: 
            return
            
        self.running = True

        alg = self.choice.get()
        
        self.visited = {self.start}
        
        if alg == "BFS":
        
            self.q = deque([[self.start]])
            self.do_bfs()
            
        elif alg == "DFS":
            self.stk = [[self.start]]
        
            self.do_dfs()
            
        elif alg == "UCS":
            self.pq = [(0, [self.start])]
            self.do_ucs()
            
        elif alg == "DLS":
            self.stk = [[self.start]]
        
            self.lim = 5 
            self.do_dls()
            
        elif alg == "IDDFS":
            self.depth_lim = 1
        
            self.visited = set()
            self.stk = [[self.start]]
        
            self.do_iddfs()
            
        elif alg == "Bidirectional":
            self.q1 = deque([[self.start]])
        
            self.q2 = deque([[self.end]])
            
            self.v1 = {self.start: [self.start]}
            self.v2 = {self.end: [self.end]}
            
            self.do_bidir()

    def do_bfs(self):

        if not self.q: 
            return
        
        if self.running == False: 
            return
        
        
        path = self.q.popleft()
        curr = path[len(path) - 1]
        
        if self.check(curr, path): 
            return
        
        for n in self.get_adj(curr):
            if n not in self.visited:
                self.visited.add(n)
                new_p = list(path)
        
                new_p.append(n)
        
                self.q.append(new_p)
                self.mark(n)
        
        self.win.after(50, self.do_bfs)

    def do_dfs(self):
        if not self.stk: 
            return
        
        if not self.running: 
            return
        
        path = self.stk.pop()
        
        curr = path[len(path) - 1]
        
        if self.check(curr, path): 
            return
        
        if curr not in self.visited:
            self.visited.add(curr)
        
        for n in self.get_adj(curr):
            if n not in path: 
        
                self.stk.append(path + [n])
                self.mark(n)
        
        self.win.after(50, self.do_dfs)

    def do_ucs(self):
        if not self.pq: 
            return
        if not self.running: 
            return
        
        c, path = heapq.heappop(self.pq)
        curr = path[len(path) - 1]
        
        if self.check(curr, path): 
            return
        
        if curr not in self.visited:
            self.visited.add(curr)
            
            for n in self.get_adj(curr):
                if n not in self.visited:
                    nc = c + 1
                    heapq.heappush(self.pq, (nc, path + [n]))
                    self.mark(n)
        
        self.win.after(50, self.do_ucs)

    def do_dls(self):
        if not self.stk: 
            return
        if not self.running: 
            return
        

        path = self.stk.pop()
        curr = path[len(path) - 1]
        
        if self.check(curr, path): 
            return
        
        if len(path) <= self.lim:
            if curr not in self.visited: 
                self.visited.add(curr)
                
            for n in self.get_adj(curr):
                if n not in path:
                    self.stk.append(path + [n])
                    self.mark(n)
        
        
        self.win.after(50, self.do_dls)

    def do_iddfs(self):
        if self.running == False: 
            return
        
        if len(self.stk) == 0:
            self.depth_lim += 1
            if self.depth_lim > 25: 
                self.running = False
        
                return
            
            self.visited = set()
            self.stk = [[self.start]]
            self.clear_color()
            
        
        path = self.stk.pop()
        curr = path[len(path) - 1]



        if curr != self.start and curr != self.end:

             self.canvas.itemconfig(self.boxes[curr], fill="lightblue")

        if curr == self.end:

            self.found(path)
            self.running = False

            return

        if len(path) <= self.depth_lim:
            for n in self.get_adj(curr):
                if n not in path:
                    self.stk.append(path + [n])
                    self.mark(n)

        self.win.after(20, self.do_iddfs)

    def do_bidir(self):
        if not self.running: 
            return
        
        if not self.q1 or not self.q2: 
            return

        if self.q1:

            p1 = self.q1.popleft()
            c1 = p1[len(p1) - 1]
            self.v1[c1] = p1
            
            if c1 in self.v2:
                p2 = self.v2[c1]
                
                path2_reversed = list(reversed(p2))
                path2_reversed.pop(0) 
                
                total = p1 + path2_reversed
                
                self.found(total)
                self.running = False
                return
            
            if c1 != self.start:
                self.canvas.itemconfig(self.boxes[c1], fill="lightblue")
            
            for n in self.get_adj(c1):
                if n not in self.v1:

                    self.v1[n] = p1 + [n]
                    
                    self.q1.append(p1 + [n])
                    self.mark(n)

        if self.q2:
            p2 = self.q2.popleft()
            c2 = p2[len(p2) - 1]
            self.v2[c2] = p2

            if c2 in self.v1:
                p1 = self.v1[c2]
                
                path2_reversed = list(reversed(p2))
                path2_reversed.pop(0)
                
                total = p1 + path2_reversed
                
                self.found(total)
                self.running = False
                return
                
            if c2 != self.end:
                self.canvas.itemconfig(self.boxes[c2], fill="pink")

            for n in self.get_adj(c2):
                if n not in self.v2:

                    self.v2[n] = p2 + [n]
                    
                    self.q2.append(p2 + [n])
                    self.mark(n)

        self.win.after(50, self.do_bidir)

    def get_adj(self, node):
        r, c = node

        res = []
        for dr, dc in moves:
            nr = r + dr
            nc = c + dc
            
            if nr >= 0 and nr < self.rows and nc >= 0 and nc < self.cols:
                if self.map[nr][nc] == 0:
                    res.append((nr, nc))
        return res

    def check(self, node, path):
        if node == self.end:
            self.found(path)

            self.running = False
            return True
        if node != self.start:

            self.canvas.itemconfig(self.boxes[node], fill="lightblue")
        return False

    def mark(self, node):
        if node != self.end and node != self.start:
            
            self.canvas.itemconfig(self.boxes[node], fill="orange")

    def found(self, path):
        for n in path:
            if n != self.start and n != self.end:

                self.canvas.itemconfig(self.boxes[n], fill="yellow")

    def clear_color(self):
        for r in range(self.rows):
            for c in range(self.cols):
            
                if (r,c) != self.start and (r,c) != self.end and self.map[r][c] == 0:
            
                    self.canvas.itemconfig(self.boxes[(r,c)], fill="white")

    def restart(self):
        self.running = False
        
        self.canvas.destroy()
        self.make_gui()

root = tk.Tk()

app = App(root)

root.mainloop()
