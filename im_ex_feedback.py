import os
import django
import pandas as pd

# -------------------------------------------------------------------
# 步驟 0: 初始化 Django 環境
# -------------------------------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

from django.contrib.auth.models import User
from feedbacks.models import Feedback  # 請將 myapp 替換為您的 app 名稱

# -------------------------------------------------------------------
# 步驟 a & b: 資料清理與格式化 (Data Cleaning & Formatting)
# -------------------------------------------------------------------
def process_data(raw_data_list):

    cleaned_records = []
    
    default_user = User.objects.first()
    if not default_user:
        raise ValueError("Please create User ")

    for row in raw_data_list:
        
        title = str(row.get('title', '')).strip()                        # 1. 處理 Title：去除前後空白、限制最大字數 200 字
        if not title:
            title = "no title"                                          # 預設值
        title = title[:200]


        content = str(row.get('content', '')).strip()                        # 2. 處理 Content：去除首尾空白

        username = row.get('username', '').strip()                          # 3. 處理 User 關聯：尋找指定 username，若不存在則使用預設 User
        user_obj = User.objects.filter(username=username).first() if username else None
        if not user_obj:
            user_obj = default_user

        cleaned_records.append({
            'user': user_obj,
            'title': title,
            'content': content
        })
        
    return cleaned_records



def import_to_django(cleaned_data):
    
    feedbacks_to_create = [
        Feedback(
            user=item['user'],
            title=item['title'],
            content=item['content']
        )
        for item in cleaned_data
    ]
    
    created_objects = Feedback.objects.bulk_create(feedbacks_to_create)
    print(f"success import {len(created_objects)}  Feedback data into database！")





def export_from_django(output_filepath="exported_feedbacks.csv"):

    queryset = Feedback.objects.select_related('user').values(      
        'id', 'user__username', 'title', 'content', 'date'              # 使用 select_related 抓取關聯 User 的 username
    )
    
    df = pd.DataFrame(list(queryset))
    df.rename(columns={'user__username': 'username'}, inplace=True)
    
    df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
    print(f"成功從資料庫匯出 {len(df)} 筆資料至 '{output_filepath}'！")



# -------------------------------------------------------------------
# 主程式執行點
# -------------------------------------------------------------------
if __name__ == '__main__':

    raw_dataset = [
        {'username': 'admin', 'title': '  介面問題  ', 'content': '  按鈕太小了，不好點擊。 '},
        {'username': 'non_existent_user', 'title': '', 'content': '這是一條沒有標題的反饋。'},
        {'username': '', 'title': '系統很棒！' * 50, 'content': 'hihi'}, 
    ]

    print("=== Start data cleaning and formatting ===")
    formatted_dataset = process_data(raw_dataset)
    
    print("===import data into Django databade ===")
    import_to_django(formatted_dataset)
    
    print("=== from Django export data ===")
    export_from_django()