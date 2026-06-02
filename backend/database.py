"""SQLite-backed lightweight database abstraction layer.

This provides the exact same async APIs as motor (MongoDB) for the Suno Prompt Studio app
when running in a local macOS app context.
"""
import json
import sqlite3
import asyncio
from pathlib import Path

DB_FILE = Path(__file__).parent / "suno_prompt_studio.db"

class SQLiteCursor:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def sort(self, key, direction=-1):
        # direction is -1 for DESC, 1 for ASC
        reverse = (direction == -1)
        self.items.sort(key=lambda x: x.get(key, ""), reverse=reverse)
        return self

    def limit(self, count):
        self.items = self.items[:count]
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item

class SQLiteCollection:
    def __init__(self, table_name):
        self.table_name = table_name
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        if self.table_name == "jobs":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    kind TEXT,
                    status TEXT,
                    request TEXT,
                    result TEXT,
                    error TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
        elif self.table_name == "library":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS library (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    concept TEXT,
                    mode TEXT,
                    payload TEXT,
                    validation TEXT,
                    created_at TEXT
                )
            """)
        conn.commit()
        conn.close()

    async def insert_one(self, doc):
        await asyncio.to_thread(self._insert_one_sync, doc)
        return doc

    def _insert_one_sync(self, doc):
        conn = self._get_conn()
        cursor = conn.cursor()
        if self.table_name == "jobs":
            cursor.execute(
                "INSERT INTO jobs (id, kind, status, request, result, error, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    doc["id"],
                    doc["kind"],
                    doc["status"],
                    json.dumps(doc["request"]),
                    json.dumps(doc["result"]) if doc["result"] is not None else None,
                    doc["error"],
                    doc["created_at"],
                    doc["updated_at"],
                )
            )
        elif self.table_name == "library":
            cursor.execute(
                "INSERT INTO library (id, title, concept, mode, payload, validation, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    doc["id"],
                    doc["title"],
                    doc.get("concept"),
                    doc["mode"],
                    json.dumps(doc["payload"]),
                    json.dumps(doc["validation"]) if doc.get("validation") is not None else None,
                    doc["created_at"],
                )
            )
        conn.commit()
        conn.close()

    async def update_one(self, query, update):
        await asyncio.to_thread(self._update_one_sync, query, update)

    def _update_one_sync(self, query, update):
        conn = self._get_conn()
        cursor = conn.cursor()
        if self.table_name == "jobs":
            job_id = query.get("id")
            if "$set" in update:
                set_fields = update["$set"]
                fields_to_update = []
                params = []
                for k, v in set_fields.items():
                    if k in ["status", "error", "updated_at"]:
                        fields_to_update.append(f"{k} = ?")
                        params.append(v)
                    elif k in ["result"]:
                        fields_to_update.append(f"{k} = ?")
                        params.append(json.dumps(v) if v is not None else None)
                if fields_to_update:
                    params.append(job_id)
                    sql = f"UPDATE jobs SET {', '.join(fields_to_update)} WHERE id = ?"
                    cursor.execute(sql, tuple(params))
        conn.commit()
        conn.close()

    async def find_one(self, query, projection=None):
        return await asyncio.to_thread(self._find_one_sync, query)

    def _find_one_sync(self, query):
        conn = self._get_conn()
        cursor = conn.cursor()
        doc_id = query.get("id")
        doc = None
        if self.table_name == "jobs":
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (doc_id,))
            row = cursor.fetchone()
            if row:
                doc = {
                    "id": row["id"],
                    "kind": row["kind"],
                    "status": row["status"],
                    "request": json.loads(row["request"]),
                    "result": json.loads(row["result"]) if row["result"] else None,
                    "error": row["error"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
        elif self.table_name == "library":
            cursor.execute("SELECT * FROM library WHERE id = ?", (doc_id,))
            row = cursor.fetchone()
            if row:
                doc = {
                    "id": row["id"],
                    "title": row["title"],
                    "concept": row["concept"],
                    "mode": row["mode"],
                    "payload": json.loads(row["payload"]),
                    "validation": json.loads(row["validation"]) if row["validation"] else None,
                    "created_at": row["created_at"],
                }
        conn.close()
        return doc

    async def find(self, query=None, projection=None):
        items = await asyncio.to_thread(self._find_all_sync)
        return SQLiteCursor(items)

    def _find_all_sync(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        items = []
        if self.table_name == "jobs":
            cursor.execute("SELECT * FROM jobs")
            for row in cursor.fetchall():
                items.append({
                    "id": row["id"],
                    "kind": row["kind"],
                    "status": row["status"],
                    "request": json.loads(row["request"]),
                    "result": json.loads(row["result"]) if row["result"] else None,
                    "error": row["error"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                })
        elif self.table_name == "library":
            cursor.execute("SELECT * FROM library")
            for row in cursor.fetchall():
                items.append({
                    "id": row["id"],
                    "title": row["title"],
                    "concept": row["concept"],
                    "mode": row["mode"],
                    "payload": json.loads(row["payload"]),
                    "validation": json.loads(row["validation"]) if row["validation"] else None,
                    "created_at": row["created_at"],
                })
        conn.close()
        return items

    async def delete_one(self, query):
        await asyncio.to_thread(self._delete_one_sync, query)

    def _delete_one_sync(self, query):
        conn = self._get_conn()
        cursor = conn.cursor()
        doc_id = query.get("id")
        if self.table_name == "library":
            cursor.execute("DELETE FROM library WHERE id = ?", (doc_id,))
        conn.commit()
        conn.close()

class SQLiteDatabase:
    def __init__(self):
        self.jobs = SQLiteCollection("jobs")
        self.library = SQLiteCollection("library")

def get_database():
    return SQLiteDatabase()
