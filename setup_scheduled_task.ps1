# 设置定时任务的 PowerShell 脚本

# 定义任务名称
$TaskName = "DailyCrawlerTask"

# 定义批处理文件路径
$ScriptPath = "C:\Users\cf\Desktop\crawl - 副本\run_crawler.bat"

# 定义任务触发器（每天上午8点）
$Trigger = New-ScheduledTaskTrigger -Daily -At 8am

# 定义任务操作
$Action = New-ScheduledTaskAction -Execute $ScriptPath

# 定义任务设置
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 定义任务主体（使用系统账户运行）
$Principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# 注册任务
Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Settings $Settings -Principal $Principal -Description "每天上午8点运行网页爬虫"

Write-Host "定时任务 '$TaskName' 已成功创建！"
Write-Host "任务将在每天上午8点自动运行爬虫脚本。"