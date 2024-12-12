#!/bin/bash

# 記錄文件路徑
LOG_FILE="/tmp/task_switch.log"

# 如果記錄文件不存在，初始化為 0
if [ ! -f "$LOG_FILE" ]; then
    echo 0 > "$LOG_FILE"
fi

# 讀取當前狀態
CURRENT_STATE=$(cat "$LOG_FILE")

if [ "$CURRENT_STATE" -eq 0 ]; then
    # 執行第一個指令
    docker exec tw_news_clawer_app_1 python3 app.py --weeks_limit=1 >> /tmp/craw_logs.log 2>&1
    # 切換狀態
    echo 1 > "$LOG_FILE"
else
    # 執行第二個指令
    docker exec tw_news_clawer_app_1 python3 src/upload/upload_google_drive.py />> /tmp/upload_logs.log 2>&1
    # 切換狀態
    echo 0 > "$LOG_FILE"
fi

