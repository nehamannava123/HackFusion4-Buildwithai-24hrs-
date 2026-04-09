<div align="center">

# 🤖 CodeNav AI

## AI-Powered GitHub Repository Analyzer

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**Understand any GitHub repository in seconds — with AI-powered insights**

[Features](#✨-features) • [Quick Start](#🚀-quick-start) • [AI Setup](#🤖-ai-setup) • [Architecture](#🏗️-architecture) • [Demo](#🎬-demo)

</div>

---

## 📌 Overview

**CodeNav AI** is an intelligent codebase navigation assistant that analyzes any public GitHub repository and answers questions about its structure, files, and functionality. It uses **Ollama** (local AI) to provide intelligent responses and features a beautiful, modern web interface.

### 🎯 Problem We Solve

Developers and students struggle to understand large, unfamiliar codebases due to:
- Poor or missing documentation
- Complex architecture
- No guided exploration

**Result:** Slow onboarding, reduced productivity, and difficulty learning from real-world projects.

### 💡 Our Solution

CodeNav AI provides:
- 🔍 **Instant GitHub repository analysis**
- 🤖 **AI-powered Q&A** about any codebase
- 📁 **Visual file structure exploration**
- 🎯 **Smart entry point detection**
- 🔄 **Execution flow visualization**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| <img src="https://img.icons8.com/color/24/000000/github--v1.png"/> **GitHub Analysis** | Analyze any public GitHub repository by URL |
| <img src="https://img.icons8.com/color/24/000000/artificial-intelligence.png"/> **AI-Powered Q&A** | Ask questions about the codebase (Ollama integration) |
| <img src="https://img.icons8.com/color/24/000000/folder-inspector.png"/> **File Explorer** | View repository structure with file sizes and metadata |
| <img src="https://img.icons8.com/color/24/000000/statistics--v1.png"/> **Statistics Dashboard** | See files, lines, language at a glance |
| <img src="https://img.icons8.com/color/24/000000/play--v1.png"/> **Entry Point Detection** | Automatically finds where to start exploring |
| <img src="https://img.icons8.com/color/24/000000/flow-chart.png"/> **Flow Visualization** | See execution flow diagrams for authentication, API, database |
| <img src="https://img.icons8.com/color/24/000000/comments.png"/> **Interactive Chat** | Natural language Q&A interface |
| <img src="https://img.icons8.com/color/24/000000/docker.png"/> **Docker Ready** | One-command deployment |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git (for cloning repositories)
- (Optional) Ollama for AI features

### Local Development

```bash
# Clone the repository
git clone https://github.com/nehamannava123/HackFusion4-Buildwithai-24hrs-.git
cd HackFusion4-Buildwithai-24hrs-

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

AI setup - 
# Download from https://ollama.ai
ollama pull llama3.2:1b

architecture - 
┌─────────────────────────────────────────────────────────────┐
│                    CodeNav AI Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Browser   │◄──►│   Flask     │◄──►│  GitHub     │     │
│  │   (HTML/CSS)│    │   Backend   │    │  API Clone  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         ▲                  ▲                  ▲            │
│         │                  │                  │            │
│         ▼                  ▼                  ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Chat UI   │    │   AI/QA     │    │  Ollama     │     │
│  │  Interface  │    │   Engine    │    │  (Local AI) │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

project structure - 
codenav-ai/
├── 📁 codenav/                 # Core Python modules
│   ├── analyzer.py             # Repository analysis
│   ├── ai_qa.py               # AI integration (Ollama)
│   ├── hybrid_qa.py           # Smart router (AI vs Rules)
│   ├── detector.py            # Entry point detection
│   ├── visualizer.py          # Flow diagrams
│   └── qa.py                  # Rule-based fallback
├── 📁 templates/               # HTML templates
│   └── index.html             # Main web interface
├── 📁 static/                  # CSS styles
├── 📁 api/                     # Serverless entry (Vercel)
├── app.py                      # Main Flask application
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-container setup
└── requirements.txt            # Python dependencies