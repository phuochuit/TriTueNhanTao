import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import turtle
import math
import sys

# --- LOGIC TSP (BACKTRACKING) ---
class TSPSolver:
    def __init__(self, matrix):
        self.graph = matrix
        self.n = len(matrix)
        self.min_cost = sys.maxsize
        self.best_path = []

    def solve(self):
        # Reset
        self.min_cost = sys.maxsize
        self.best_path = []
        
        visited = [False] * self.n
        visited[0] = True
        
        self._backtrack(0, 1, 0, [0], visited)
        
        # Chuyển index thành tên (A, B, C...) để hiển thị
        named_path = [chr(65 + i) for i in self.best_path]
        return self.min_cost, named_path

    def _backtrack(self, curr_pos, count, cost, path, visited):
        # Nhánh cận
        if cost >= self.min_cost and self.min_cost != sys.maxsize:
            return

        # Base case: Đã đi hết các thành phố
        if count == self.n:
            if self.graph[curr_pos][0] > 0: # Có đường về
                total = cost + self.graph[curr_pos][0]
                if total < self.min_cost:
                    self.min_cost = total
                    self.best_path = path + [0] # Khép vòng
            return

        # Thử các thành phố tiếp theo
        for i in range(self.n):
            if not visited[i] and self.graph[curr_pos][i] > 0:
                visited[i] = True
                self._backtrack(i, count + 1, cost + self.graph[curr_pos][i], path + [i], visited)
                visited[i] = False

# --- GIAO DIỆN NGƯỜI DÙNG ---
class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minh Họa Bài Toán Người Bán Hàng (TSP)")
        self.root.geometry("1100x700")

        # Layout
        left_frame = tk.Frame(root, width=350, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        right_frame = tk.Frame(root, bg="white", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Bảng điều khiển
        tk.Label(left_frame, text="BẢNG ĐIỀU KHIỂN TSP", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)
        
        btn_frame = tk.Frame(left_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, padx=20)
        
        self.btn_load = tk.Button(btn_frame, text="📂 Đọc File", command=self.load_file, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_run = tk.Button(btn_frame, text="▶ Tìm Đường", command=self.run_tsp, state=tk.DISABLED, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_run.pack(side=tk.RIGHT, padx=5)

        # Khu vực hiển thị kết quả
        self.result_frame = tk.LabelFrame(left_frame, text="Kết quả tối ưu", font=("Arial", 11, "bold"), bg="#f0f0f0")
        self.result_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.lbl_cost = tk.Label(self.result_frame, text="Chi phí: ---", font=("Arial", 12), bg="#f0f0f0", fg="red")
        self.lbl_cost.pack(pady=5, anchor="w")
        
        self.lbl_path = tk.Label(self.result_frame, text="Lộ trình: ---", font=("Arial", 11), bg="#f0f0f0", wraplength=300, justify="left")
        self.lbl_path.pack(pady=5, anchor="w")

        # Bảng ma trận
        tk.Label(left_frame, text="Ma trận khoảng cách:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(10,0))
        self.txt_matrix = tk.Text(left_frame, height=15, width=40, font=("Consolas", 10))
        self.txt_matrix.pack(pady=5, padx=10)

        # 2. Turtle Canvas
        self.canvas = tk.Canvas(right_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.bgcolor("white")
        self.t = turtle.RawTurtle(self.turtle_screen)
        self.t.speed(0)
        self.t.hideturtle()

        self.matrix = []
        self.nodes = []
        self.positions = {}

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path: return

        try:
            with open(file_path, 'r') as f:
                self.matrix = []
                content = ""
                for line in f:
                    parts = line.strip().replace(',', ' ').split()
                    row = [int(x) for x in parts]
                    if row: 
                        self.matrix.append(row)
                        content += line
            
            self.txt_matrix.delete("1.0", tk.END)
            self.txt_matrix.insert(tk.END, content)
            
            # Setup Nodes
            num_nodes = len(self.matrix)
            self.nodes = [chr(65 + i) for i in range(num_nodes)]
            
            self.draw_graph_structure()
            self.btn_run.config(state=tk.NORMAL)
            self.lbl_cost.config(text="Chi phí: ---")
            self.lbl_path.config(text="Lộ trình: ---")

        except Exception as e:
            messagebox.showerror("Lỗi", f"File không hợp lệ: {e}")

    def draw_graph_structure(self):
        self.t.clear()
        self.positions = {}
        n = len(self.nodes)
        radius = 180
        offset_y = -50
        
        # 1. Tính tọa độ
        for i, node in enumerate(self.nodes):
            angle = (2 * math.pi * i) / n
            x = radius * math.cos(angle)
            y = radius * math.sin(angle) + offset_y
            self.positions[node] = (x, y)

        # 2. Vẽ cạnh và trọng số
        self.t.pensize(1)
        for i in range(n):
            for j in range(i + 1, n):
                weight = self.matrix[i][j]
                if weight > 0: # Chỉ vẽ nếu có đường đi
                    u, v = self.nodes[i], self.nodes[j]
                    p1 = self.positions[u]
                    p2 = self.positions[v]
                    
                    # Vẽ dây
                    self.t.pencolor("lightgray")
                    self.t.penup(); self.t.goto(p1); self.t.pendown(); self.t.goto(p2)
                    
                    # Vẽ số (trọng số) ở giữa dây
                    mid_x = (p1[0] + p2[0]) / 2
                    mid_y = (p1[1] + p2[1]) / 2
                    self.t.penup(); self.t.goto(mid_x, mid_y); 
                    self.t.pencolor("blue")
                    self.t.write(str(weight), align="center", font=("Arial", 9, "normal"))

        # 3. Vẽ đỉnh
        for node in self.nodes:
            self.draw_node(node, "white", "black")

    def draw_node(self, name, bg_color, fg_color):
        x, y = self.positions[name]
        self.t.penup(); self.t.goto(x, y + 5); self.t.pendown()
        self.t.dot(40, bg_color) # Nền
        self.t.dot(44, "black") if bg_color == "white" else None # Viền nếu trắng
        self.t.dot(40, bg_color)
        
        self.t.penup(); self.t.goto(x, y - 7)
        self.t.color(fg_color)
        self.t.write(name, align="center", font=("Arial", 11, "bold"))

    def run_tsp(self):
        solver = TSPSolver(self.matrix)
        min_cost, path_names = solver.solve()
        
        if min_cost == sys.maxsize:
            messagebox.showwarning("Thông báo", "Không tìm thấy chu trình Hamilton (Đồ thị không liên thông?)")
            return

        # Hiển thị kết quả text
        self.lbl_cost.config(text=f"Chi phí: {min_cost}")
        self.lbl_path.config(text=f"Lộ trình: {' -> '.join(path_names)}")
        
        # Animation
        self.btn_run.config(state=tk.DISABLED)
        self.animate_path(path_names, 0)

    def animate_path(self, path_names, index):
        if index >= len(path_names) - 1:
            self.btn_run.config(state=tk.NORMAL)
            messagebox.showinfo("Xong", "Đã mô phỏng xong lộ trình!")
            return

        u_name = path_names[index]
        v_name = path_names[index+1]
        
        # 1. Tô màu đỉnh xuất phát
        self.draw_node(u_name, "#FFeb3b", "black") # Màu vàng
        
        # 2. Vẽ đường nối màu đỏ
        p1 = self.positions[u_name]
        p2 = self.positions[v_name]
        
        self.t.penup()
        self.t.goto(p1)
        self.t.pendown()
        self.t.pencolor("red")
        self.t.pensize(4)
        self.t.goto(p2)
        
        # 3. Tô màu đỉnh đích (tạm thời)
        self.draw_node(v_name, "#FF5722", "white") # Màu cam đậm

        # Đệ quy bước tiếp theo sau 1s
        self.root.after(1000, lambda: self.animate_path(path_names, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()