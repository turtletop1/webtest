import os
import django
import pandas as pd
from django.utils import timezone

# -------------------------------------------------------------------
# 初始化 Django 環境
# -------------------------------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

from django.contrib.auth.models import User
from stuffs.models import Stuff
from stuffs.choices_stuff import type as TYPE_CHOICES, district_choices as DISTRICT_CHOICES

pd.set_option('future.no_silent_downcasting', True)


# -------------------------------------------------------------------
# 資料清理與格式化 (Data Cleaning & Formatting)
# -------------------------------------------------------------------

def process_data_with_pandas(df):
    
    df['name'] = df['name'].fillna('Unidentified Item').astype(str).str.strip().str.slice(0, 100)       # 處理 Name：去除首尾空格、無名稱者設為預設值

    
    df['description'] = df['description'].fillna('').astype(str).str.strip()        # 處理 Description & Location：去除首尾空格
    df['location'] = df['location'].fillna('Unknown Location').astype(str).str.strip().str.slice(0, 100)


    df['type'] = df['type'].fillna('').astype(str).str.strip()                   # 處理Choices(type & district)：驗證合法 Key，無效者設為預設空字串
    df['type'] = df['type'].apply(lambda x: x if x in TYPE_CHOICES else '')

    df['district'] = df['district'].fillna('').astype(str).str.strip()
    df['district'] = df['district'].apply(lambda x: x if x in DISTRICT_CHOICES else '')

    if 'missing_date' in df.columns:
        df['missing_date'] = pd.to_datetime(df['missing_date'], errors='coerce')        # 日期無效時預設為目前時間，確保滿足 NOT NULL 限制
        df['missing_date'] = df['missing_date'].fillna(pd.Timestamp.now())
        df['missing_date'] = df['missing_date'].dt.tz_localize(
            timezone.get_current_timezone(),
            ambiguous='NaT',
            nonexistent='NaT'
        )
    else:
        df['missing_date'] = timezone.now()

    df['photo_main'] = df['photo_main'].fillna('').astype(str).str.strip()

    return df



# -------------------------------------------------------------------
# 資料匯入 (Import) 與 匯出 (Export) 到 Django 資料庫
# -------------------------------------------------------------------

def import_to_django(df):

    default_user = User.objects.first()
    if not default_user:
        raise ValueError("Please create User in 。")

    stuffs_to_create = []

    for _, row in df.iterrows():
        username = str(row.get('username', '')).strip()                 # 外鍵: User 處理
        user_obj = User.objects.filter(username=username).first() if username else None
        if not user_obj:
            user_obj = default_user

        photo_val = row['photo_main'] if row['photo_main'] and row['photo_main'].lower() != 'nan' else None     # 圖片路徑空值處理

        stuffs_to_create.append(
            Stuff(
                user=user_obj,
                name=row['name'],
                type=row['type'],
                description=row['description'],
                location=row['location'],
                district=row['district'],
                missing_date=row['missing_date'],
                photo_main=photo_val
            )
        )

    created_objects = Stuff.objects.bulk_create(stuffs_to_create)           # 批次匯入資料庫
    print(f"success to import {len(created_objects)}  Stuff！")



def export_from_django(output_filepath="exported_stuffs.csv"):          # from django read stuff and import CSV

    queryset = Stuff.objects.select_related('user').values(
        'id',
        'user__username',
        'name',
        'type',
        'description',
        'location',
        'district',
        'missing_date',
        'photo_main'
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
        {
            'username': 'abc',
            'name': '  iPhone 15 Pro ',
            'type': 'object',
            'description': 'black ',
            'location': ' Yuen Long MTR ',
            'district': 'Yuen Long',
            'missing_date': '2026-08-20 14:30:00',
            'photo_main': 'photos/2026/08/20/iphone.jpg'
        },
        {
            'username': 'Ma123',
            'name': 'black umbrella',  
            'type': 'object', 
            'description': 'lost umbrella',
            'location': 'AB road , Tuen Mung',
            'district': 'Tuen Mung', 
            'missing_date': '2026-08-20 11:30:00', 
            'photo_main': ''
        },
        {
            'username': 'aaa',
            'name': 'black tortoise',  
            'type': 'pet', 
            'description': 'lost tortoise',
            'location': 'ABC road,Tuen Mung',
            'district': 'Tuen Mung', 
            'missing_date': '2026-08-20 10:30:00', 
            'photo_main': ''
        }
    ]

    print("=== start clear Pandas  ===")
    raw_df = pd.DataFrame(raw_dataset)
    cleaned_df = process_data_with_pandas(raw_df)

    print("=== write Django database ===")
    import_to_django(cleaned_df)

    print("=== import  CSV to Django===")
    export_from_django()