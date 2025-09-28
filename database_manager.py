import psycopg2
from psycopg2 import sql
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                port=5432,
                dbname="postgres",
                user="postgres",
                password="cf178025"
            )
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            self.connection = None
    
    def create_table(self):
        """创建数据表"""
        if not self.connection:
            print("数据库未连接")
            return
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS data_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            cn_name VARCHAR(255),
            time VARCHAR(255),
            summary TEXT,
            statistics TEXT,
            prediction TEXT,
            news TEXT,
            type VARCHAR(50),
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            
            # 创建联合索引以加快查询速度
            create_index_query = """
            CREATE INDEX IF NOT EXISTS idx_data_table_name_create_time
            ON data_table (name, create_time);
            """
            cursor.execute(create_index_query)
            
            self.connection.commit()
            cursor.close()
            print("数据表创建成功或已存在")
            print("联合索引创建成功或已存在")
        except Exception as e:
            print(f"创建数据表或索引失败: {e}")
    
    def insert_data(self, name, cn_name, time, summary, statistics, prediction, news, data_type):
        """插入新数据或更新现有数据"""
        if not self.connection:
            print("数据库未连接")
            return
        
        try:
            cursor = self.connection.cursor()
            
            # 查询是否已存在同一天内相同名称的记录
            check_query = """
            SELECT id FROM data_table
            WHERE name = %s AND DATE(create_time) = CURRENT_DATE
            """
            cursor.execute(check_query, (name,))
            result = cursor.fetchone()
            
            if result:
                # 更新现有记录
                update_query = """
                UPDATE data_table
                SET cn_name = %s, time = %s, summary = %s, statistics = %s, prediction = %s, news = %s, type = %s, create_time = %s
                WHERE id = %s
                """
                cursor.execute(update_query, (
                    cn_name,
                    time,
                    summary,
                    statistics,
                    prediction,
                    news,
                    data_type,
                    datetime.now(),
                    result[0]
                ))
                print("数据更新成功")
            else:
                # 插入新记录
                insert_query = """
                INSERT INTO data_table (name, cn_name, time, summary, statistics, prediction, news, type, create_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (
                    name,
                    cn_name,
                    time,
                    summary,
                    statistics,
                    prediction,
                    news,
                    data_type,
                    datetime.now()
                ))
                print("数据插入成功")
            
            self.connection.commit()
            cursor.close()
        except Exception as e:
            # 回滚事务以避免 "current transaction is aborted" 错误
            self.connection.rollback()
            print(f"数据操作失败: {e}")
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")