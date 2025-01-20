import requests
from bs4 import BeautifulSoup
import csv

# Gửi yêu cầu HTTP tới trang web
response = requests.get("https://mercedes-vietnamstar.com.vn/bang-gia-xe/")

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    # Tạo đối tượng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm tất cả các container chứa thông tin xe
    products = soup.select(".box-text.box-text-products")

    # Chuẩn bị dữ liệu để ghi vào file CSV
    data = [["Tên xe", "Giá"]]  # Tiêu đề cột
    for product in products:
        # Lấy tên xe
        name = product.select_one(".name.product-title.woocommerce-loop-product__title a")
        name_text = name.get_text(strip=True) if name else "Không có tên xe"

        # Lấy giá xe
        price = product.select_one(".woocommerce-Price-amount bdi")
        price_text = price.get_text(strip=True).replace("₫", "").strip() if price else "Không có giá"

        # Thêm vào danh sách dữ liệu
        data.append([name_text, price_text])

    # Ghi dữ liệu ra file CSV
    with open('info-car1.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("Dữ liệu đã được lưu vào file info-car1.csv")
else:
    print("Không thể truy cập trang web.")
