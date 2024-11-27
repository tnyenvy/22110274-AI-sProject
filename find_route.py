import osmnx as ox
import networkx as nx
import folium
import streamlit as st

# Hàm tìm đường và hiển thị trên bản đồ
def find_route_on_map(start_location, end_location):
    try:
        # Geocoding để lấy tọa độ
        start_point = ox.geocode(start_location)
        end_point = ox.geocode(end_location)

        # Kiểm tra xem tọa độ có hợp lệ không
        if not start_point or not end_point:
            st.error("Không thể xác định tọa độ từ địa chỉ. Vui lòng thử lại với địa chỉ khác.")
            return None

    except Exception as e:
        st.error(f"Không tìm thấy địa điểm: {e}")
        return None

    # Tải bản đồ Việt Nam
    try:
        G = ox.graph_from_place("Vietnam", network_type="drive")
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu bản đồ: {e}")
        return None

    # Tìm các node gần nhất
    try:
        start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])  # (lon, lat)
        end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])
    except Exception as e:
        st.error(f"Lỗi khi xác định các node gần nhất: {e}")
        return None

    # Tính toán đường đi ngắn nhất
    try:
        route = nx.shortest_path(G, start_node, end_node, weight="length")
    except Exception as e:
        st.error(f"Lỗi khi tính toán đường đi: {e}")
        return None

    # Chuyển đổi đường đi thành danh sách tọa độ
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    # Tạo bản đồ tương tác với folium
    map_center = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]
    route_map = folium.Map(location=map_center, zoom_start=12)

    # Thêm tuyến đường lên bản đồ
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(route_map)

    # Đánh dấu điểm bắt đầu và kết thúc
    folium.Marker(location=(start_point[0], start_point[1]), popup="Điểm bắt đầu", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(location=(end_point[0], end_point[1]), popup="Điểm kết thúc", icon=folium.Icon(color="red")).add_to(route_map)

    return route_map

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
            # Lưu bản đồ Folium thành file HTML
            map_file = "route_map.html"
            route_map.save(map_file)

            # Đọc nội dung file HTML và hiển thị trên Streamlit
            with open(map_file, "r", encoding="utf-8") as f:
                html_data = f.read()

            st.components.v1.html(html_data, height=600, scrolling=False)
