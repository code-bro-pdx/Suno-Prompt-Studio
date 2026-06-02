package com.example.sunopromptstudio

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class LlmService(private val apiKey: String) {

    suspend fun generateCompletion(systemMessage: String, userMessage: String, model: String = "claude-3-5-sonnet-20241022", maxTokens: Int = 4000): String {
        return withContext(Dispatchers.IO) {
            val url = URL("https://api.anthropic.com/v1/messages")
            val connection = url.openConnection() as HttpURLConnection
            try {
                connection.requestMethod = "POST"
                connection.setRequestProperty("x-api-key", apiKey)
                connection.setRequestProperty("anthropic-version", "2023-06-01")
                connection.setRequestProperty("content-type", "application/json")
                connection.doOutput = true

                val messagesArray = JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", userMessage)
                    })
                }

                val payload = JSONObject().apply {
                    put("model", model)
                    put("max_tokens", maxTokens)
                    put("system", systemMessage)
                    put("messages", messagesArray)
                }

                val writer = OutputStreamWriter(connection.outputStream)
                writer.write(payload.toString())
                writer.flush()
                writer.close()

                val responseCode = connection.responseCode
                if (responseCode == 200) {
                    val responseStr = connection.inputStream.bufferedReader().use { it.readText() }
                    val responseJson = JSONObject(responseStr)
                    val contentArray = responseJson.getJSONArray("content")
                    if (contentArray.length() > 0) {
                        contentArray.getJSONObject(0).getString("text")
                    } else {
                        throw Exception("Empty content in Anthropic response")
                    }
                } else {
                    val errorStr = connection.errorStream?.bufferedReader()?.use { it.readText() } ?: "Unknown error"
                    throw Exception("Anthropic API failed with status $responseCode: $errorStr")
                }
            } finally {
                connection.disconnect()
            }
        }
    }
}
