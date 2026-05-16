import heapq
from itertools import chain
import matplotlib.pyplot as plt
import numpy as np
import time 

def to_tuple(state):
    return tuple(tuple(row) for row in state)

def find_zero(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    row, col = find_zero(state) 
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(state) and 0 <= c < len(state[0]):
            new_state = [list(row) for row in state]
            new_state[row][col], new_state[r][c] = new_state[r][c], new_state[row][col]
            neighbors.append(to_tuple(new_state)) 
    return neighbors

def manhattan(state, goal):
    value_pos = {}
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            value_pos[goal[i][j]] = (i, j) 

    dist = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            val = state[i][j]
            if val != 0: 
                gi, gj = value_pos[val] 
                dist += abs(i - gi) + abs(j - gj) 
    return dist

def count_misplaced_tiles(state, goal):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

def is_solvable(state, goal):
    n = len(state) 

    def inversions(flat_list):
        inv = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] != 0 and flat_list[j] != 0 and flat_list[i] > flat_list[j]:
                    inv += 1
        return inv

    start_flat = list(chain.from_iterable(state))
    goal_flat = list(chain.from_iterable(goal))

    goal_pos = {val: i for i, val in enumerate(goal_flat)}
    mapped_start_flat = [goal_pos[val] for val in start_flat]
    inv_count = inversions(mapped_start_flat) 

    zero_row = find_zero(state)[0] 

    if n % 2 == 1: 
        return inv_count % 2 == 0
    else: 
        distance_from_bottom_row = n - zero_row 
        return (inv_count + distance_from_bottom_row) % 2 == 1

def input_state(n, name="trạng thái"):
    print(f"\nHãy nhập {name} của puzzle (gồm {n} dòng, mỗi dòng {n} số, dùng số 0 cho ô trống):")
    state = []
    for i in range(n):
        while True:
            try:
                row_input = input(f"Dòng {i + 1}: ").split()
                row = [int(x) for x in row_input] 

                if len(row) != n:
                    raise ValueError(f"Ối! Dòng này phải có chính xác {n} số. Bạn đã nhập {len(row)} số.")
                
                state.append(row)
                break 
            except ValueError as e:
                print(f"Lỗi nhập liệu: {e} Xin hãy thử lại.")
            except Exception as e:
                print(f"Có lỗi không mong muốn xảy ra: {e} Xin hãy thử lại.")
    return state

def print_state(state):
    n = len(state)
    print("+" + "---+" * n) 
    for row in state:
        print("|", end="")
        for val in row:
            print(f"{val: >2}", end=" |") 
        print()
        print("+" + "---+" * n) 
    print()

def draw_puzzle_state_on_subplot(ax, state, title_info=""):
    n = len(state)
    ax.clear() 
    
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(np.arange(0, n + 1, 1))
    ax.set_yticks(np.arange(0, n + 1, 1))
    ax.grid(True, which='major', color='black', linestyle='-', linewidth=2)
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    ax.invert_yaxis()

    for r in range(n):
        for c in range(n):
            val = state[r][c] 
            if val != 0: 
                ax.text(c + 0.5, r + 0.5, str(val), 
                        fontsize=12, ha='center', va='center', color='black') 

    ax.set_title(title_info, fontsize=8) 
    
def a_star_verbose(start, goal):
    
    open_list = [] 
    heapq.heappush(open_list, (manhattan(start, goal), 0, to_tuple(start), []))
    
    visited = set()


    iteration = 0 
    while open_list:
        iteration += 1
        f, g, current_tuple, path = heapq.heappop(open_list)
        current = [list(row) for row in current_tuple] 

        if current_tuple == to_tuple(goal):
            print("\n🎉 CHÚC MỪNG! Đã tìm thấy lời giải cho puzzle của bạn! 🎉")
            return path + [current] 

        if current_tuple in visited:
            continue

        visited.add(current_tuple) 
        
        neighbors = get_neighbors(current) 

        for neighbor_tuple in neighbors:
            if neighbor_tuple not in visited: 
                g_new = g + 1 
                h = manhattan([list(row) for row in neighbor_tuple], goal) 
                f_new = g_new + h 

                heapq.heappush(open_list, (f_new, g_new, neighbor_tuple, path + [current]))

    print("\n😞 Rất tiếc, không tìm thấy lời giải. Có vẻ như có điều gì đó không ổn.")
    return None

def show_steps(path, goal):
    print("\n✨ CÁC BƯỚC GIẢI PHÁP ĐÃ TÌM THẤY! ✨")
    print("----------------------------------------------------------")
    num_steps = len(path)
    if num_steps == 0:
        print("Không có bước nào để hiển thị.")
        return

    cols = int(np.ceil(np.sqrt(num_steps)))
    rows = int(np.ceil(num_steps / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(2.5 * cols, 2.5 * rows)) 
    
    fig.suptitle("Các Bước Giải Puzzle", fontsize=14, fontname='Times New Roman') 
    
    if num_steps == 1: 
        axes = [axes] 
    else:
        axes = np.array(axes).flatten() 

    for i in range(num_steps):
        state = path[i]
        state_for_drawing = [list(row) for row in state] 
        
        g = i 
        h = manhattan(state_for_drawing, goal) 
        f = g + h 
        
        title_info = f"Bước {i}\ng={g}, h={h}, f={f}"

        draw_puzzle_state_on_subplot(axes[i], state_for_drawing, title_info)
        
        if i < min(num_steps, 4): 
            print(f"\n--- Bước {i}: (g={g}, h={h}, f={f}) ---")
            print_state(state_for_drawing)

    for j in range(num_steps, len(axes)):
        fig.delaxes(axes[j])
            
    plt.tight_layout(rect=[0, 0, 1, 0.96], pad=1.5) 
    plt.show() 

    print(f"\n👉 Tổng cộng cần {num_steps - 1} bước để giải puzzle này. Hoàn thành! 💪")


def compare_ini_goal(ini, goal):
    print("\n--- SO SÁNH TRẠNG THÁI BAN ĐẦU VÀ ĐÍCH ---")
    misplaced = count_misplaced_tiles(ini, goal)
    manhattan_dist = manhattan(ini, goal)
    print(f"🔹 Số ô đang sai vị trí: {misplaced}")
    print(f"🔹 Tổng khoảng cách Manhattan: {manhattan_dist}")
    print("----------------------------------------------------------")

if __name__ == "__main__":
    print("Chào mừng bạn đến với chương trình Giải Puzzle!!! 🧩")
    while True:
        try:
            n = int(input("Hãy nhập kích thước của puzzle (ví dụ: 3 cho 8-puzzle, 4 cho 15-puzzle): "))
            if n < 2:
                raise ValueError("Kích thước puzzle phải ít nhất là 2x2. Vui lòng thử lại.")
            break
        except ValueError as e:
            print(f"Lỗi nhập liệu: {e}")
        except Exception as e:
            print(f"Có lỗi không mong muốn: {e}")

    start = input_state(n, "trạng thái bắt đầu")
    goal = input_state(n, "trạng thái kết thúc")

    print("\n--- Puzzle của bạn đã sẵn sàng! ---")
    print("Trạng thái bắt đầu:")
    print_state(start)
    print("Trạng thái đích:")
    print_state(goal)

    compare_ini_goal(start, goal)

    print("\n🌟 BẮT ĐẦU HÀNH TRÌNH TÌM KIẾM A*! 🌟")
    print("----------------------------------------------------------")
    
    if not is_solvable(start, goal):
        print("\n💔 TRẠNG THÁI NÀY KHÔNG THỂ GIẢI ĐƯỢC! 💔")
        print("Rất tiếc, với trạng thái bắt đầu và trạng thái đích bạn đã nhập, puzzle này không có lời giải.")
        print("Hãy thử một trạng thái khác nhé!")
    else:
        print("\n🎉 TRẠNG THÁI NÀY CÓ THỂ GIẢI ĐƯỢC! 🎉")
        print("\n Đang bắt đầu tìm kiếm lời giải...")
        path = a_star_verbose(start, goal) 
        if path:
            show_steps(path, goal) 
        else:
            print("❗ Không tìm thấy lời giải. Có thể do lỗi trong quá trình tìm kiếm hoặc puzzle quá lớn.")