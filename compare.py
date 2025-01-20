import pandas as pd

data1 = pd.read_csv('info-car1.csv')
data2 = pd.read_csv('info-car2.csv')

# Hàm chuẩn hóa giá
def clean_price(price_str):
    return int(price_str.replace('.', ''))

# Chuẩn hóa giá
data1['Giá'] = data1['Giá'].apply(clean_price)
data2['Giá'] = data2['Giá'].apply(clean_price)

# So sánh giá
comparison = pd.merge(data1, data2, on='Tên xe', how='inner', suffixes=('_file1', '_file2'))

# Chênh lệch giá
comparison['Chênh lệch giá'] = comparison['Giá_file1'] - comparison['Giá_file2']
comparison_results = comparison[['Tên xe', 'Giá_file1', 'Giá_file2', 'Chênh lệch giá']]

# Xuất file CSV
comparison_results.to_csv('comparison_results.csv', index=False, encoding='utf-8-sig')

print(comparison_results)
