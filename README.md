# NCKU Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A smart chatbot assistant designed specifically for National Cheng Kung University (NCKU) students, powered by Dify and integrated with LINE messaging platform.

Line ID: @283aixtg

![QR code](https://github.com/user-attachments/assets/5aae324f-57a4-45ce-9452-d8743b0fb99b)

## Overview

NCKU Chatbot aims to simplify student campus life by providing instant, accurate responses to inquiries about course selection, dormitory information, and campus activities. Built on Dify's powerful LLM development platform, it delivers a natural conversational experience similar to talking with a senior student familiar with campus affairs.

## Project Structure

```
ncku-chatbot/
├── linebot/        # LINE bot integration service
├── crawler/        # Web crawling scripts and n8n templates (In Development)
├── richmenu/       # LINE rich menu configuration files 
└── dify/           # DSL files, including prompts, LLM models, etc. (In Development)
```

## 💡 Install pre-commit before development

Pre-commit will automatically run black formatting checks and fixes on each commit.

```bash
pip install pre-commit
pre-commit install
```

Use pre-commit to automatically format your code, ensuring consistent code style.

```bash
pre-commit run --all-files
```
