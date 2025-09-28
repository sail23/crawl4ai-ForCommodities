# 网页爬虫定时服务

这个项目将网页爬虫代码改造成了一个定时服务，每天下午3点自动运行。

## 文件说明

- `basic_crawl_example_backup.py`: 原始的网页爬虫代码
- `database_manager.py`: 数据库管理模块
- `scheduled_crawler.py`: 定时执行的爬虫脚本
- `run_crawler.bat`: 运行爬虫的批处理文件
- `setup_scheduled_task.ps1`: 设置 Windows 任务计划程序的 PowerShell 脚本
- `start_service.bat`: 启动定时服务的批处理文件
- `simple_crawler.py`: 独立的网页爬虫脚本，用于爬取指定网址的信息

## 安装和设置

1. 确保已安装所需的 Python 库：
   ```
   pip install crawl4ai schedule pytz psycopg2
   ```

2. 修改 `database_manager.py` 中的数据库连接信息（如果需要）：
   ```python
   self.connection = psycopg2.connect(
       host="localhost",
       port=5432,
       dbname="postgres",
       user="postgres",
       password="your_password"
   )
   ```

3. 设置 Windows 任务计划程序：
   - 以管理员身份打开 PowerShell
   - 导航到项目目录：
     ```powershell
     cd "C:\Users\cf\Desktop\crawl - 副本"
     ```
   - 运行以下命令创建定时任务：
     ```powershell
     .\setup_scheduled_task.ps1
     ```

## 手动运行

如果需要手动运行爬虫，可以执行以下任一命令：

1. 运行 Python 脚本：
   ```
   python scheduled_crawler.py
   ```

2. 运行批处理文件：
   ```
   run_crawler.bat
   ```

3. 使用启动脚本：
   ```
   start_service.bat
   ```

## 测试

首次运行时，脚本会立即执行一次爬虫任务作为测试，然后设置定时任务。

## 查看任务计划程序

可以通过以下方式查看和管理任务计划程序：

1. 打开"任务计划程序"（Task Scheduler）
2. 在左侧面板中导航到"任务计划程序库"
3. 查找名为"DailyCrawlerTask"的任务

## 停止定时任务

如果需要停止定时任务，可以：

1. 打开"任务计划程序"
2. 找到"DailyCrawlerTask"任务
3. 右键点击任务并选择"禁用"或"删除"

## 注意事项

1. 确保系统在上午8点时处于开机状态，否则任务将不会执行
2. 如果需要修改执行时间，可以编辑任务计划程序中的触发器设置
3. 确保 Python 环境和所需的库已正确安装
4. 数据库事务错误已修复，现在可以正确处理插入失败的情况
5. 数据库表结构问题已修复，create_time 字段现在使用正确的 TIMESTAMP 类型
6. 日期比较查询已修复，现在可以正确比较日期
7. 数据插入逻辑已恢复为正确的逻辑：
   - 如果当天已有相同名称的数据则更新该记录
   - 如果当天没有相同名称的数据则插入新记录
   - 确保每个商品每天只有一条记录，保存的是当天最后一次运行的结果
   - 不同日期的数据会共存（例如9月26日和9月28日的数据都会存在）
8. 为 name 和 create_time 字段创建了联合索引，以加快查询速度