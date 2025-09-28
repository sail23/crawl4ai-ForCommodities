@echo off
echo 正在启动网页爬虫定时服务...
echo 服务将在每天上午8点自动运行爬虫任务
echo 按 Ctrl+C 可以停止服务
echo.
cd /d "C:\Users\cf\Desktop\crawl - 副本"
python scheduled_crawler.py
pause