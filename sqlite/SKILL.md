---
name: sqlite
description: Query and manage SQLite databases directly. Execute SQL queries, inspect schemas, create tables, and analyze data in local .db files. Use when working with SQLite databases for data exploration, journal entries, analytics, or any structured local data.
tags: [database, sqlite, sql, data, productivity]
created_from: mcp-server
version: 1.0.0
---

# SQLite - Local Database Operations

Query and manage SQLite databases directly from Claude Code. Based on the official @modelcontextprotocol/server-sqlite.

## When to Use

- Querying local SQLite databases (e.g., treegarden.db, app databases)
- Exploring database schemas and table structures
- Running analytical queries on structured data
- Creating or modifying tables for new data storage
- Extracting insights from journal entries, logs, or captured data

## Tools

### read_query

Execute read-only SQL queries against a SQLite database.

**Parameters:**
- `db_path` (string, required): Path to the SQLite database file
- `query` (string, required): SQL SELECT query to execute

**Returns:** Query results as rows with column names.

**Example:**
```python
read_query(db_path="C:/data/projects/treegarden/treegarden.db", query="SELECT date, type, plant, description FROM journal ORDER BY date DESC LIMIT 10")
```

**Supported statements:** SELECT, PRAGMA, EXPLAIN

### write_query

Execute write operations on a SQLite database.

**Parameters:**
- `db_path` (string, required): Path to the SQLite database file
- `query` (string, required): SQL INSERT, UPDATE, or DELETE statement

**Returns:** Number of rows affected.

**Example:**
```python
write_query(db_path="treegarden.db", query="INSERT INTO journal (date, type, plant, description) VALUES ('2026-03-08', 'observation', 'tomato', 'First flowers appearing')")
```

### list_tables

List all tables and views in a SQLite database.

**Parameters:**
- `db_path` (string, required): Path to the SQLite database file

**Returns:** List of table and view names.

**Example:**
```python
list_tables(db_path="treegarden.db")
```

### describe_table

Get detailed schema information for a specific table.

**Parameters:**
- `db_path` (string, required): Path to the SQLite database file
- `table_name` (string, required): Name of the table to describe

**Returns:** Column names, types, nullability, defaults, and primary key info.

**Example:**
```python
describe_table(db_path="treegarden.db", table_name="journal")
```

### create_table

Create a new table in a SQLite database.

**Parameters:**
- `db_path` (string, required): Path to the SQLite database file
- `query` (string, required): CREATE TABLE SQL statement

**Returns:** Confirmation of table creation.

**Example:**
```python
create_table(db_path="treegarden.db", query="CREATE TABLE IF NOT EXISTS harvests (id INTEGER PRIMARY KEY, date TEXT, plant TEXT, quantity REAL, unit TEXT)")
```

## Best Practices

- Use `list_tables` and `describe_table` to understand schema before querying
- Prefer `read_query` for exploration; use `write_query` only when explicitly needed
- Always use parameterized-style values to avoid SQL injection in dynamic queries
- Back up databases before running write operations on important data
- Use PRAGMA statements via `read_query` for database metadata (e.g., `PRAGMA table_info(tablename)`)
