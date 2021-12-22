Cấu trúc file input_BrFS_DFS.txt: (tìm kiếm chiều rộng - tìm kiếm chiều sâu)
- Dòng đầu tiên: "Tên đỉnh đầu" + "Tên đỉnh kết thúc"
- Các dòng tiếp theo:
    + "Tên đỉnh cha" + "Tên đỉnh con"

Cấu trúc file input_Astar.txt, input_BranchBound.txt: (tìm kiếm A*), (tìm kiếm nhánh và cận)
- Dòng đầu tiên: "Tên đỉnh đầu", "Tên đỉnh kết thúc"
- Các dòng tiếp theo:
    + "Tên đỉnh cha", "Trọng số đỉnh cha", "Tên đỉnh con", "Trọng số đỉnh con", "Khoảng cách"

Cấu trúc file input_BFS_HCS.txt: (tìm kiếm tốt nhất đầu tiên - tìm kiếm leo đồi)
- Dòng đầu tiên: "Tên đỉnh đầu" + "Tên đỉnh kết thúc"
- Các dòng tiếp theo (có 3 ký tự):
    + "Tên đỉnh cha" + "Tên đỉnh con" + "Trọng số của đỉnh con"
- fist_value (trong BFS_HCS.py): trọng số của đỉnh đầu