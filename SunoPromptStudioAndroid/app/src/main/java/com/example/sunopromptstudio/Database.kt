package com.example.sunopromptstudio

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import org.json.JSONArray
import org.json.JSONObject

class DatabaseHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        const val DATABASE_NAME = "suno_prompt_studio.db"
        const val DATABASE_VERSION = 1
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """
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
            """.trimIndent()
        )
        db.execSQL(
            """
            CREATE TABLE IF NOT EXISTS library (
                id TEXT PRIMARY KEY,
                title TEXT,
                concept TEXT,
                mode TEXT,
                payload TEXT,
                validation TEXT,
                created_at TEXT
            )
            """.trimIndent()
        )
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Handle upgrades if needed
    }

    fun insertJob(job: JSONObject) {
        val db = writableDatabase
        val values = ContentValues().apply {
            put("id", job.optString("id"))
            put("kind", job.optString("kind"))
            put("status", job.optString("status"))
            put("request", job.optJSONObject("request")?.toString())
            put("result", job.optJSONObject("result")?.toString())
            put("error", if (job.has("error") && !job.isNull("error")) job.getString("error") else null)
            put("created_at", job.optString("created_at"))
            put("updated_at", job.optString("updated_at"))
        }
        db.insertWithOnConflict("jobs", null, values, SQLiteDatabase.CONFLICT_REPLACE)
        db.close()
    }

    fun updateJob(id: String, setFields: JSONObject) {
        val db = writableDatabase
        val values = ContentValues()
        
        val keys = setFields.keys()
        while (keys.hasNext()) {
            val key = keys.next()
            when (key) {
                "status", "error", "updated_at" -> values.put(key, if (setFields.isNull(key)) null else setFields.getString(key))
                "result" -> values.put(key, if (setFields.isNull(key)) null else setFields.getJSONObject(key).toString())
            }
        }
        
        if (values.size() > 0) {
            db.update("jobs", values, "id = ?", arrayOf(id))
        }
        db.close()
    }

    fun getJob(id: String): JSONObject? {
        val db = readableDatabase
        val cursor = db.query("jobs", null, "id = ?", arrayOf(id), null, null, null)
        var job: JSONObject? = null
        if (cursor.moveToFirst()) {
            job = JSONObject().apply {
                put("id", cursor.getString(cursor.getColumnIndexOrThrow("id")))
                put("kind", cursor.getString(cursor.getColumnIndexOrThrow("kind")))
                put("status", cursor.getString(cursor.getColumnIndexOrThrow("status")))
                val requestStr = cursor.getString(cursor.getColumnIndexOrThrow("request"))
                put("request", if (requestStr != null) JSONObject(requestStr) else null)
                val resultStr = cursor.getString(cursor.getColumnIndexOrThrow("result"))
                put("result", if (resultStr != null) JSONObject(resultStr) else null)
                put("error", cursor.getString(cursor.getColumnIndexOrThrow("error")))
                put("created_at", cursor.getString(cursor.getColumnIndexOrThrow("created_at")))
                put("updated_at", cursor.getString(cursor.getColumnIndexOrThrow("updated_at")))
            }
        }
        cursor.close()
        db.close()
        return job
    }

    fun getJobs(): JSONArray {
        val db = readableDatabase
        val cursor = db.query("jobs", null, null, null, null, null, null)
        val jobs = JSONArray()
        while (cursor.moveToNext()) {
            val job = JSONObject().apply {
                put("id", cursor.getString(cursor.getColumnIndexOrThrow("id")))
                put("kind", cursor.getString(cursor.getColumnIndexOrThrow("kind")))
                put("status", cursor.getString(cursor.getColumnIndexOrThrow("status")))
                val requestStr = cursor.getString(cursor.getColumnIndexOrThrow("request"))
                put("request", if (requestStr != null) JSONObject(requestStr) else null)
                val resultStr = cursor.getString(cursor.getColumnIndexOrThrow("result"))
                put("result", if (resultStr != null) JSONObject(resultStr) else null)
                put("error", cursor.getString(cursor.getColumnIndexOrThrow("error")))
                put("created_at", cursor.getString(cursor.getColumnIndexOrThrow("created_at")))
                put("updated_at", cursor.getString(cursor.getColumnIndexOrThrow("updated_at")))
            }
            jobs.put(job)
        }
        cursor.close()
        db.close()
        return jobs
    }

    fun insertLibraryItem(item: JSONObject) {
        val db = writableDatabase
        val values = ContentValues().apply {
            put("id", item.optString("id"))
            put("title", item.optString("title"))
            put("concept", if (item.has("concept") && !item.isNull("concept")) item.getString("concept") else null)
            put("mode", item.optString("mode"))
            put("payload", item.optJSONObject("payload")?.toString())
            put("validation", item.optJSONObject("validation")?.toString())
            put("created_at", item.optString("created_at"))
        }
        db.insertWithOnConflict("library", null, values, SQLiteDatabase.CONFLICT_REPLACE)
        db.close()
    }

    fun getLibraryItems(): JSONArray {
        val db = readableDatabase
        val cursor = db.query("library", null, null, null, null, null, null)
        val items = JSONArray()
        while (cursor.moveToNext()) {
            val item = JSONObject().apply {
                put("id", cursor.getString(cursor.getColumnIndexOrThrow("id")))
                put("title", cursor.getString(cursor.getColumnIndexOrThrow("title")))
                put("concept", cursor.getString(cursor.getColumnIndexOrThrow("concept")))
                put("mode", cursor.getString(cursor.getColumnIndexOrThrow("mode")))
                val payloadStr = cursor.getString(cursor.getColumnIndexOrThrow("payload"))
                put("payload", if (payloadStr != null) JSONObject(payloadStr) else null)
                val validationStr = cursor.getString(cursor.getColumnIndexOrThrow("validation"))
                put("validation", if (validationStr != null) JSONObject(validationStr) else null)
                put("created_at", cursor.getString(cursor.getColumnIndexOrThrow("created_at")))
            }
            items.put(item)
        }
        cursor.close()
        db.close()
        return items
    }

    fun deleteLibraryItem(id: String) {
        val db = writableDatabase
        db.delete("library", "id = ?", arrayOf(id))
        db.close()
    }
}
