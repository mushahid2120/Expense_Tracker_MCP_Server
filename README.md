# Expense Tracker MCP Server

An MCP (Model Context Protocol) server that turns an AI assistant into an interface for logging and querying personal expenses — built with [FastMCP](https://github.com/jlowin/fastmcp) and SQLAlchemy.

---

## 🚀 Overview

This server exposes expense-tracking tools over MCP so that any MCP-compatible client (Claude, Claude Desktop, etc.) can add and retrieve expense records through natural language, without a separate UI. Data is persisted via SQLAlchemy to a SQL database (MySQL, via `pymysql`).

## ✨ Features

- **`add_expense` tool** — logs a new expense with date, amount, a fixed category (`Education`, `Clothes`, `Shoes`, `Accesories`, `Ration`, `Bills`), and a free-text note
- **`list_expenses` tool** — retrieves all expenses, or filters by a `start_date`/`end_date` range, sorted oldest to newest
- **`expense://category` resource** — exposes the valid category list as JSON so a client can validate input before calling `add_expense`
- Auto-creates the database schema on startup (`init_db()`)
- Runs as an HTTP-transport MCP server

## 🛠️ Tech Stack

| Layer        | Technology |
|--------------|------------|
| MCP framework | [FastMCP](https://github.com/jlowin/fastmcp) (`fastmcp[apps]`) |
| ORM          | SQLAlchemy 2.x (declarative models, typed `Mapped` columns) |
| Database     | MySQL (via `pymysql`) |
| Config       | `python-dotenv` for environment variables |
| Runtime      | Python ≥ 3.13 |

## 📂 Project Structure

```
Expense_Tracker_MCP_Server/
├─ main.py           # MCP server, DB model, and tool/resource definitions
├─ mydatabase.db      # local dev database
├─ pyproject.toml
└─ .python-version
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.13+
- A MySQL database (or adjust `DB_URL` for another SQLAlchemy-supported engine)

### Installation

```bash
git clone https://github.com/mushahid2120/Expense_Tracker_MCP_Server.git
cd Expense_Tracker_MCP_Server
pip install -e .
```

### Environment Variables

Create a `.env` file:

```
DB_URL=mysql+pymysql://user:password@host:3306/dbname
```

### Running the Server

```bash
python main.py
```

This starts the MCP server over HTTP on `0.0.0.0:8000` and creates the `expense` table if it doesn't exist.

### Connecting to an MCP Client

Point your MCP client (Claude Desktop's `claude_desktop_config.json`, or a Claude.ai custom connector) at `http://<host>:8000` so `add_expense` and `list_expenses` appear as available tools.

## 🧰 Available Tools & Resources

| Name | Type | Description |
|------|------|-------------|
| `add_expense` | tool | Add an expense (`date`, `amount`, `category`, `note`) |
| `list_expenses` | tool | List expenses, optionally filtered by date range |
| `expense://category` | resource | Returns valid category values as JSON |

## 🗺️ Roadmap

- [ ] Support custom/user-defined categories instead of a fixed list
- [ ] Add a monthly-summary or spend-by-category tool
- [ ] Add authentication for multi-user use

## 📄 License

MIT
