from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re

# Khởi động trình duyệt
driver = webdriver.Chrome()
driver.get('https://business.google.com/v/spice-viet-hanoi-restaurant/09765530579215403246/8a4f/_/rev/?gclid=Cj0KCQiA1p28BhCBARIsADP9HrNM5yPTXcZvJKBr9M1mFtrrjlcZnzlgklspOPiwI51c6-q_5Kdi3YgaAhlVEALw_wcB&caid=21745318942&agid=173555579251')

# Cuộn trang để tải thêm dữ liệu
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Lấy các feedback
feedbacks = driver.find_elements(By.CLASS_NAME, 'yNsZUe')  # Cập nhật class chính xác

# Hàm lọc feedback để lấy phần gốc (tiếng Việt) và loại bỏ feedback không phải tiếng Việt
def clean_feedback(text):
    # Nếu có "(Original)", lấy nội dung sau nó
    if "(Original)" in text:
        text = text.split("(Original)", 1)[1].strip()
    # Gộp các dòng xuống dòng bất quy tắc thành một dòng
    text = re.sub(r'\s+', ' ', text)
    # Kiểm tra nếu không có ký tự tiếng Việt, loại bỏ feedback
    if not re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', text, re.IGNORECASE):
        return None
    return text.strip()

# Ghi dữ liệu vào file CSV
filename = 'feedbacks.csv'
with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Số thứ tự', 'Nội dung feedback'])  # Tên cột

    index = 1
    for feedback in feedbacks:
        cleaned_feedback = clean_feedback(feedback.text.strip())
        if cleaned_feedback:  # Chỉ ghi nếu feedback là tiếng Việt
            writer.writerow([index, cleaned_feedback])
            index += 1
# In thông báo hoàn thành
print(f"Quá trình lưu vào file CSV '{filename}' đã hoàn thành.")

driver.quit()
