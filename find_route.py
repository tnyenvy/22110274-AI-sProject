import osmnx as ox
import networkx as nx
import folium
import tkinter as tk
from tkinter import simpledialog, messagebox

# Hàm tìm đường và hiển thị trên bản đồ
def find_route_on_map(start_location, end_location):
    try:
        # Geocoding để lấy tọa độ
        start_point = ox.geocode(start_location)
        end_point = ox.geocode(end_location)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không tìm thấy địa điểm: {e}")
        return

    # Tải bản đồ Việt Nam
    G = ox.graph_from_place("Vietnam", network_type="drive")

    # Tìm các node gần nhất
    start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])  # (lon, lat)
    end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

    # Tính toán đường đi ngắn nhất
    route = nx.shortest_path(G, start_node, end_node, weight="length")

    # Chuyển đổi đường đi thành danh sách tọa độ
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    # Tạo bản đồ tương tác với folium
    map_center = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]
    route_map = folium.Map(location=map_center, zoom_start=6)

    # Thêm tuyến đường lên bản đồ
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(route_map)

    # Đánh dấu điểm bắt đầu và kết thúc
    folium.Marker(location=start_point, popup="Điểm bắt đầu", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(location=end_point, popup="Điểm kết thúc", icon=folium.Icon(color="red")).add_to(route_map)

    # Lưu bản đồ thành file HTML
    route_map.save("route_map.html")
    messagebox.showinfo("Thành công", "Bản đồ đã được tạo! Mở file 'route_map.html' để xem.")

# Giao diện người dùng với Tkinter
def main():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính

    try:
        start_location = simpledialog.askstring("Địa điểm", "Nhập địa chỉ hoặc tên nơi bắt đầu:")
        end_location = simpledialog.askstring("Địa điểm", "Nhập địa chỉ hoặc tên nơi kết thúc:")

        if not start_location or not end_location:
            messagebox.showwarning("Cảnh báo", "Bạn phải nhập cả hai địa điểm!")
            return

        find_route_on_map(start_location, end_location)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()
