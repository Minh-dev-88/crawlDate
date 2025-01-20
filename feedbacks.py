import pandas as pd

data = pd.read_csv('feedbacks.csv')

# Dữ liệu mẫu
print("\nDữ liệu mẫu:")
print(data)

# Từ khóa
keywords_food = ["đồ ăn", "món ăn", "hương vị", "ngon", "bày biện", "phục vụ món"]
keywords_ambiance = ["không gian", "trang trí", "ấm áp", "thoải mái", "sang trọng", "lịch sự"]

# Hàm phân loại feedback
def classify_feedback(feedback):
    feedback_lower = feedback.lower()
    is_food = any(keyword in feedback_lower for keyword in keywords_food)
    is_ambiance = any(keyword in feedback_lower for keyword in keywords_ambiance)
    
    if is_food and is_ambiance:
        return "Cả hương vị và không gian"
    elif is_food:
        return "Hương vị đồ ăn"
    elif is_ambiance:
        return "Không gian nhà hàng"
    else:
        return "Khác"

# Cột phân loại vào DataFrame
data['Phân loại'] = data['Nội dung feedback'].apply(classify_feedback)

# Kết quả phân loại
print("\nKết quả phân loại:")
print(data)
