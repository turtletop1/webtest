import psycopg2
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'database': os.getenv('DB_NAME', 'webstestdb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'hkhkhk'),  # 如果 .env 冇設定就用預設值
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

TABLE_NAME =''

def table_select(num):
    global TABLE_NAME           # global

    if num == '1':
        TABLE_NAME = 'feedbacks_feedback'
    elif num == '2':
        TABLE_NAME = 'posts_post'
    else:
        return

    print(f"\n select: {TABLE_NAME}")


def import_feedback(csv_path='feedback.csv'):    
    try:
        print("checking CSV...")
        if not os.path.exists(csv_path):
            print(f"❌ error file is not exist '{csv_path}'")
            return
        
        file_size = os.path.getsize(csv_path)
        print(f"find file: {csv_path} ({file_size} bytes)")
        
        print("\n CSV check:")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i < 5:
                    print(f"   行 {i}: {row}")
                else:
                    break
        
        print("\n check csv title...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            print(f"   title: {headers}")
            required_fields = ['user_id', 'content', 'title']
            missing_fields = [f for f in required_fields if f not in headers]
            if missing_fields:
                print(f"  lack of fields: {missing_fields}")
                return
        

        print("\n connect database...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        print("connect success")
        
    
        print(f"\n confirm form '{TABLE_NAME}' exist...")
        sql_create = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (              
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
            content TEXT,
            date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            title VARCHAR(200) NOT NULL
        );
        '''
        cursor.execute(sql_create)
        print("finish \'w\'")
        
        print("\n import data...")
        success_count = 0
        error_count = 0
        error_rows = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                try:

                    user_id = str(row['user_id']).strip()
                    title = str(row['title']).strip()
                    content = str(row.get('content', '')).strip() if row.get('content') else None
                    date_str = str(row.get('date', '')).strip() if row.get('date') else None
                    

                    if not user_id:
                        raise ValueError("user_id must not empty")
                    if not title:
                        raise ValueError("title no empty")
                    
                    try:
                        user_id = int(user_id)
                    except ValueError:
                        raise ValueError(f"user_id must be number, but '{user_id}'")
                    
                    if date_str:
                        try:
                            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
                                try:
                                    date_obj = datetime.strptime(date_str, fmt)
                                    date_str = date_obj.isoformat()
                                    break
                                except ValueError:
                                    continue
                        except Exception as e:
                            print(f"  {row_num}: date forrmat '{date_str}'，using default time")
                            date_str = None
                    
                    sql_insert = f'''
                    INSERT INTO {TABLE_NAME} (user_id, content, date, title)
                    VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert, (user_id, content, date_str, title))
                    success_count += 1
                    
                    if success_count % 10 == 0:
                        print(f"   ✓ import {success_count} row...")
                    
                except psycopg2.IntegrityError as e:
                    error_count += 1
                    error_rows.append((row_num, str(e), row))
                    conn.rollback()
                    print(f"  {row_num}: integrated error - {str(e)[:60]}")
                    
                except ValueError as e:
                    error_count += 1
                    error_rows.append((row_num, str(e), row))
                    print(f" {row_num}: data verify error - {str(e)}")
                    
                except Exception as e:
                    error_count += 1
                    error_rows.append((row_num, str(e), row))
                    print(f"   {row_num}: unknow error - {str(e)[:60]}")

        print("\n success")
        print(f"   success: {success_count} row")
        print(f"   fail: {error_count} row")
        
        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME};')
        total_in_db = cursor.fetchone()[0]
        print(f"   now database have {total_in_db} reccord")
        
        

        if error_rows:
            print(f"\n error info:")
            for row_num, error, data in error_rows[:5]:
                print(f"\n   行 {row_num}:")
                print(f"   error: {error}")
                print(f"   data: {data}")
            if len(error_rows) > 5:
                print(f"\n   ... also have {len(error_rows) - 5} row error")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"database connect error: {e}")
        
    except psycopg2.ProgrammingError as e:
        print(f"SQL error: {e}")
        print("please check auth_user is exist ?")
        
    except Exception as e:
        print(f"unknow erre: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


def export_feedback(output_path='feedback_export.csv'):
    try:
        print("connect database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("success")
        

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (TABLE_NAME,))
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print(f" '{TABLE_NAME}' doesnt exist")
            conn.close()
            return
        
        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME};')
        row_count = cursor.fetchone()[0]
        print(f"{row_count} reccord")
        
        if row_count == 0:
            print("row is empty!。")
            conn.close()
            return
        

        print("query data ...")
        sql_select = f'''
        SELECT id, user_id, title, content, date 
        FROM {TABLE_NAME}
        ORDER BY date DESC;
        '''
        cursor.execute(sql_select)
        rows = cursor.fetchall()
        print(f"it have {len(rows)} row")
        
        
        print(f"\nmaking CSV {output_path}")
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'user_id', 'title', 'content', 'date'])
            writer.writerows(rows)

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"success")
            print(f" path: {os.path.abspath(output_path)}")
            print(f" size: {file_size} bytes")
        else:
            print("CSV doesnt create！")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"database error: {e}")

    except psycopg2.ProgrammingError as e:
        print(f" SQL error: {e}")

    except Exception as e:
        print(f"nuknow error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()




def main_menu():

    print("==============================================================");
    print("||......................................____...............|| ");
    print("||.7.\\^v.^............................./    \\ .............|| ");
    print("||vN:Y:/:|>>..........................| | |  |.............|| ");
    print("||7:|.Y:://r..........................|l W  r| ............|| ");
    print("||.K.l;|:///>...................... _-||    ||--__  .......|| ");
    print("L|_V_wi/LV_l..................... / \\====  ====y  \\........|| ");
    print("___________]=====================/   \\---Y----/    \\=========");
    print("    |  |  /                     |     \\  |   /     |l         ");
    print("    |  | |              _________\\____ \\-+--/    ,/|l         ");
    print("_________|______________\\             \\__V_/    /__|l_________");
    print("_________________________\\    c[]-     \\++/__-/`_______________");
    print("__________________________\\_____________V_____________________");
    print("______________________________________________________________");

    print("Please select table you want import/export")
    print("1. feedback  2.post  3.stuff  4.comment  5.user")
    num = input()
    table_select(num)

    
    print("------------------------------------------------------------")
    print("1.  import CSV to database")
    print("2.  export csv")
    print("3.  exit")
    print("------------------------------------------------------------")

    
    choice = input("select (1/2/3): ").strip()
    
    
    if choice == '1':
        csv_path = input("please import CSV path ").strip()

        if not csv_path:
            csv_path = 'feedback.csv'
        import_feedback(csv_path)
    
    elif choice == '2':
        output_path = input("please export CSV path ").strip()
        if not output_path:
            output_path = 'feedback_export.csv'
        export_feedback(output_path)
    
    elif choice == '3':
        return
    
    else:
        print("no work , try again")
    
    again = input("\n conunite? (y/n): ").strip().lower()
    if again == 'y':
        main_menu()


if __name__ == '__main__':
    main_menu()