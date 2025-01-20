import pandas as pd
from flask import Flask, render_template_string

# Cai dat thu vien flask: pip install flask

# Đọc dữ liệu từ file CSV
data1 = pd.read_csv('info-car1.csv')
data2 = pd.read_csv('info-car2.csv')
feedback_data = pd.read_csv('feedbacks.csv')


# Chuẩn hóa giá
def clean_price(price_str):
    return int(price_str.replace('.', ''))


# Chuẩn hóa giá cho cả hai file
data1['Giá'] = data1['Giá'].apply(clean_price)
data2['Giá'] = data2['Giá'].apply(clean_price)

# So sánh giá
comparison = pd.merge(data1, data2, on='Tên xe', how='inner', suffixes=('_file1', '_file2'))

# Tính chênh lệch giá
comparison['Chênh lệch giá'] = comparison['Giá_file1'] - comparison['Giá_file2']
comparison_results = comparison[['Tên xe', 'Giá_file1', 'Giá_file2', 'Chênh lệch giá']]

# Từ khóa cho phân loại feedback
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


# Phân loại feedback
feedback_data['Phân loại'] = feedback_data['Nội dung feedback'].apply(classify_feedback)

# Tạo Flask app
app = Flask(__name__)


# Route chính
@app.route('/')
def index():
    # Chuyển cả hai bảng dữ liệu thành HTML
    comparison_table_html = comparison_results.to_html(classes='table table-bordered', index=False, escape=False)
    feedback_table_html = feedback_data.to_html(classes='table table-bordered', index=False, escape=False)

    return render_template_string('''
        <html>
            <head>
                <title>So sánh Giá và Phân loại Feedback</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container">
                    <h1 class="mt-4">Kết quả So sánh Giá Xe</h1>
                    {{ comparison_table_html | safe }}
                    <h1 class="mt-4">Kết quả Phân loại Feedback</h1>
                    {{ feedback_table_html | safe }}
                </div>
            </body>
        </html>
    ''', comparison_table_html=comparison_table_html, feedback_table_html=feedback_table_html)


if __name__ == '__main__':
    app.run(debug=True)