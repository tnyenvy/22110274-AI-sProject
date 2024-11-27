import osmnx as ox
import networkx as nx
import folium
import streamlit as st
from streamlit.components.v1 import html

# Hàm tìm đường và hiển thị trên bản đồ
def find_route_on_map(start_location, end_location):
    try:
        # Geocoding để lấy tọa độ
        start_point = ox.geocode(start_location)
        end_point = ox.geocode(end_location)
    except Exception as e:
        st.error(f"Không tìm thấy địa điểm: {e}")
        return None

    # Tải bản đồ của Việt Nam
    try:
        G = ox.graph_from_place("Vietnam", network_type="drive")
    except Exception as e:
        st.error(f"Lỗi tải bản đồ: {e}")
        return None

    try:
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

        return route_map

    except Exception as e:
        st.error(f"Lỗi tính toán đường đi: {e}")
        return None

# Giao diện người dùng với Streamlit
st.title("Tìm Đường và Hiển Thị Bản Đồ")

start_location = st.text_input("Nhập địa chỉ hoặc tên nơi bắt đầu:")
end_location = st.text_input("Nhập địa chỉ hoặc tên nơi kết thúc:")

if st.button("Tìm Đường"):
    if not start_location or not end_location:
        st.warning("Bạn phải nhập cả hai địa điểm!")
    else:
        route_map = find_route_on_map(start_location, end_location)
        if route_map:
            # Kết xuất bản đồ Folium thành HTML để nhúng vào Streamlit
            route_map_html = route_map._repr_html_()
            html(route_map_html, height=500)
