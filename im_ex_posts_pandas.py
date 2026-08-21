import os
import django
import pandas as pd
from django.utils import timezone

# -------------------------------------------------------------------
# 步驟 0: 初始化 Django 環境 (允許獨立腳本存取 Django ORM)
# -------------------------------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stuffs.models import Stuff
from posts.models import Post
from posts.choices_post import type as TYPE_CHOICES, status as STATUS_CHOICES


# 開啟 Pandas 未來版本的轉型模式，避免警告
pd.set_option('future.no_silent_downcasting', True)

# -------------------------------------------------------------------
# 步驟 a & b: 資料清理與格式化 (Data Cleaning & Formatting)
# -------------------------------------------------------------------
def process_data_with_pandas(df):
    """
    使用 Pandas 進行資料清理與型態格式化
    """

    df['title'] = df['title'].fillna('Untitled Post').astype(str).str.strip().str.slice(0, 200)
    df['content'] = df['content'].fillna('').astype(str).str.strip()
    df['status'] = df['status'].fillna('').astype(str).str.strip()
    df['status'] = df['status'].apply(lambda x: x if x in STATUS_CHOICES else '')

    df['type'] = df['type'].fillna('').astype(str).str.strip()
    df['type'] = df['type'].apply(lambda x: x if x in TYPE_CHOICES else '')


    reward_map = {'true': True, '1': True, 'yes': True, 'y': True, True: True}
    df['reward'] = df['reward'].astype(str).str.strip().str.lower().map(reward_map).fillna(False).astype(bool)

    if 'due_date' in df.columns:
        df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
        df['due_date'] = df['due_date'].dt.tz_localize(
            timezone.get_current_timezone(),
            ambiguous='NaT',
            nonexistent='NaT'
        )
    else:
        df['due_date'] = pd.NaT

    return df




# -------------------------------------------------------------------
# 步驟 c: 資料匯入 (Import) 與 匯出 (Export) 到 Django 資料庫
# -------------------------------------------------------------------
def import_to_django(df):

    default_user = User.objects.first()
    if not default_user:
        raise ValueError("Please create User database")

    posts_to_create = []

    for _, row in df.iterrows():
        username = str(row.get('username', '')).strip()                 # 外鍵 1: 處理 User
        user_obj = User.objects.filter(username=username).first() if username else None
        if not user_obj:
            user_obj = default_user

        
        stuff_name = str(row.get('stuff_name', '')).strip()         # 外鍵 2: 處理 Stuff (若不存在則帶入必要預設值自動建立)
        stuff_obj = None
        if stuff_name and stuff_name.lower() != 'nan':
            stuff_obj, _ = Stuff.objects.get_or_create(
                name=stuff_name,
                defaults={
                    'user': user_obj,
                    'missing_date': timezone.now()
                }
            )

        due_date_val = row['due_date']          # 處理日期空值 (Pandas NaT 轉為 Python None)
        if pd.isna(due_date_val):
            due_date_val = None

        posts_to_create.append(
            Post(
                user=user_obj,
                title=row['title'],
                content=row['content'],
                status=row['status'],
                stuff=stuff_obj,
                type=row['type'],
                due_date=due_date_val,
                reward=row['reward']
            )
        )


    created_objects = Post.objects.bulk_create(posts_to_create)              # 批次寫入資料庫
    print(f"success import {len(created_objects)} data to Django ddatabase")




def export_from_django(output_filepath="exported_posts.csv"):
    
    queryset = Post.objects.select_related('user', 'stuff').values(     #從 Django 資料庫讀取資料，並使用 Pandas 匯出至 CSV 檔案
        'id',
        'user__username',
        'title',
        'content',
        'status',
        'stuff__name',
        'type',
        'due_date',
        'reward',
        'issue_date'
    )

    df = pd.DataFrame(list(queryset))
    
    df.rename(columns={                     # 重新命名關聯欄位名稱
        'user__username': 'username',
        'stuff__name': 'stuff_name'
    }, inplace=True)

    df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
    print(f"成功從資料庫匯出 {len(df)} 筆資料至 '{output_filepath}'")




# -------------------------------------------------------------------
# 主程式執行邏輯
# -------------------------------------------------------------------

if __name__ == '__main__':
    # 模擬原始髒資料 (Raw Dataset)
    raw_dataset = [
        {
            'username': 'tom123',
            'title': '  black wallet   ',
            'content': 'find it in restaurant',
            'status': 'active',
            'stuff_name': ' Wallet ',
            'type': 'found',
            'due_date': '2026-09-01 18:00:00',
            'reward': 'YES'
        },
        {
            'username': 'nmany104723',
            'title': '',  # 無標題
            'content': '測試無效欄位清理',
            'status': 'invalid_status',
            'stuff_name': '',
            'type': 'invalid_type',
            'due_date': 'invalid-date-format', # 格式錯誤日期
            'reward': '0'
        }
    ]

    print("=== start to clearing and formatting ===")
    raw_df = pd.DataFrame(raw_dataset)
    cleaned_df = process_data_with_pandas(raw_df)

    print("=== write Django database ===")
    import_to_django(cleaned_df)

    print("=== import CSV to Django Database ===")
    export_from_django()