import asyncio
import schedule
import time
from datetime import datetime
import pytz

# 导入爬虫函数和商品列表
from basic_crawl_example_backup import crawl_example, energyList, metalList, agricultureList, industryList, livestockList
from simple_crawler import crawl_example as simple_crawl_example

def run_crawler():
    """运行爬虫任务"""
    print(f"开始执行爬虫任务 - {datetime.now()}")
    
    # 合并所有商品到一个列表
    commodities = energyList + metalList + agricultureList + industryList + livestockList
    
    # 调用simple_crawler获取数据字典
    urls = ["https://zh.tradingeconomics.com/commodities"]
    data_dict = asyncio.run(simple_crawl_example(urls))
    
    # 运行原有爬虫，并传递data_dict
    asyncio.run(crawl_example(commodities, data_dict))
    
    print(f"爬虫任务执行完成 - {datetime.now()}")

def schedule_job():
    """设置定时任务"""
    # 设置时区为上海时区
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    
    # 每天下午3点执行
    schedule.every().day.at("15:00").do(run_crawler)
    
    print("定时任务已设置，每天下午3点执行")
    print("程序正在运行，按 Ctrl+C 停止")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n定时任务已停止")

if __name__ == "__main__":

    print("开始定时任务循环...")
    schedule_job()