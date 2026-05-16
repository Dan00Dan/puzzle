# A* Puzzle Solver 🧩

Đây là một chương trình Python giải quyết bài toán N-Puzzle (ví dụ: 8-puzzle, 15-puzzle) bằng cách sử dụng thuật toán tìm kiếm **A*** (A-Star) với hàm heuristic là khoảng cách Manhattan (Manhattan distance).

## Tính năng chính
- Giải quyết bài toán N-Puzzle với kích thước lưới tùy ý (ví dụ: 3x3, 4x4, v.v.).
- Kiểm tra trước tính khả thi của trạng thái ban đầu và đích (Is Solvable) dựa trên số lượng nghịch thế (inversions).
- Tự động hiển thị các bước giải một cách trực quan qua giao diện dòng lệnh (CLI).
- Trực quan hóa các bước giải bằng biểu đồ đồ họa thông qua `matplotlib` (hiển thị từng trạng thái di chuyển kèm chỉ số `g`, `h`, `f`).

## Yêu cầu hệ thống
- Python 3.x
- Thư viện cần thiết: `matplotlib`, `numpy`

## Cài đặt thư viện
Bạn có thể cài đặt các thư viện yêu cầu bằng cách chạy lệnh:
```bash
pip install matplotlib numpy
```

## Cách sử dụng
1. Chạy tệp `astar_puzzle_solver.py`:
```bash
python astar_puzzle_solver.py
```
2. Nhập kích thước của puzzle (ví dụ `3` cho 3x3 hoặc `4` cho 4x4).
3. Nhập lần lượt từng dòng cho **trạng thái bắt đầu** (dùng số `0` cho ô trống). Các số được phân tách bằng khoảng trắng.
4. Nhập lần lượt từng dòng cho **trạng thái kết thúc** (đích).
5. Chương trình sẽ kiểm tra xem bài toán có thể giải được hay không. Nếu có, nó sẽ bắt đầu tìm đường đi ngắn nhất và hiển thị chi tiết các bước.

## Tác giả
- **Trần Thị Như Quỳnh – 2374802010428 Khoa Công Nghệ Thông Tin, Trường Đại học Văn Lang**
