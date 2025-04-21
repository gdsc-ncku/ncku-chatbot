# NCKU Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

專為成功大學（NCKU）學生設計的智慧對話助手，採用 Dify 技術打造，並整合 LINE 通訊平台。

## 專案概述

NCKU Chatbot 旨在透過即時、準確的回應來簡化學生的校園生活，解答有關選課、宿舍資訊和校園活動等問題。專案基於 Dify 強大的 LLM 開發平台建構，提供自然的對話體驗，就像在與熟悉校園事務的學長姊對話。

## 專案結構

```
ncku-chatbot/
├── linebot/        # LINE 機器人整合服務
├── crawler/        # 網頁爬蟲腳本與 n8n 模板（開發中）
└── dify/           # DSL 檔案，包含提示詞、LLM 模型等（開發中）
```

## 💡 開發前請安裝 pre-commit

每次 commit 時會自動執行 black 格式檢查與修正。

```bash
pip install pre-commit
pre-commit install
```

使用 pre-commit 來自動格式化程式碼，確保程式碼風格一致。

```base
pre-commit run --all-files
```

測試用