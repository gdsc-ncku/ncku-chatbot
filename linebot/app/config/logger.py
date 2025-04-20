"""
日誌管理模組 - 為應用程式提供統一的日誌處理功能
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# 日誌格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# 日期格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日誌檔案路徑
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日誌等級對應表
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# 預設日誌等級
DEFAULT_LOG_LEVEL = "info"


def get_logger(name: str, level: str = None) -> logging.Logger:
    """
    取得設定好的日誌記錄器

    Args:
        name: 日誌記錄器名稱，通常使用模組名稱 __name__
        level: 日誌等級，可選 debug、info、warning、error、critical，預設為 info

    Returns:
        logging.Logger: 設定好的日誌記錄器
    """
    # 如果未指定層級，使用預設的
    if level is None:
        level = DEFAULT_LOG_LEVEL

    # 取得日誌層級
    log_level = LOG_LEVELS.get(level.lower(), logging.INFO)

    # 建立 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 禁用日誌傳播，避免重複輸出
    logger.propagate = False

    # 避免重複設定 handler
    if not logger.handlers:
        # 建立輸出到控制台的 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 建立輸出到檔案的 handler
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, f"{name.split('.')[-1]}.log"),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# 建立全域日誌記錄器
app_logger = get_logger("app")
