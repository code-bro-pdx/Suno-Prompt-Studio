package com.example.sunopromptstudio

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.util.Log
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import com.example.sunopromptstudio.theme.SunoPromptStudioTheme
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject
import java.util.UUID

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            SunoPromptStudioTheme {
                MainScreen()
            }
        }
    }
}

class AndroidBridge(
    private val db: DatabaseHelper,
    private val llm: LlmService,
    private val webView: WebView,
    private val scope: CoroutineScope
) {
    @JavascriptInterface
    fun makeApiCall(requestId: String, method: String, path: String, body: String?) {
        scope.launch(Dispatchers.IO) {
            try {
                Log.d("AndroidBridge", "API Call: $method $path")
                var responseBody = "{}"
                var statusCode = 200

                when {
                    path.endsWith("/api/jobs") && method == "GET" -> {
                        responseBody = db.getJobs().toString()
                    }
                    path.endsWith("/api/jobs") && method == "POST" -> {
                        val payload = JSONObject(body ?: "{}")
                        // Generate a job ID
                        val jobId = UUID.randomUUID().toString()
                        val jobDoc = JSONObject().apply {
                            put("id", jobId)
                            put("kind", payload.optString("kind", "generate_prompt"))
                            put("status", "pending")
                            put("request", payload)
                            put("result", JSONObject.NULL)
                            put("error", JSONObject.NULL)
                            put("created_at", System.currentTimeMillis().toString())
                            put("updated_at", System.currentTimeMillis().toString())
                        }
                        db.insertJob(jobDoc)
                        responseBody = jobDoc.toString()
                        
                        // Kick off background LLM process
                        processJob(jobId, payload)
                    }
                    path.endsWith("/api/library") && method == "GET" -> {
                        responseBody = db.getLibraryItems().toString()
                    }
                    path.endsWith("/api/library") && method == "POST" -> {
                        val item = JSONObject(body ?: "{}")
                        item.put("id", UUID.randomUUID().toString())
                        item.put("created_at", System.currentTimeMillis().toString())
                        db.insertLibraryItem(item)
                        responseBody = item.toString()
                    }
                    path.contains("/api/jobs/") && method == "GET" -> {
                        val id = path.substringAfterLast("/")
                        val job = db.getJob(id)
                        if (job != null) {
                            responseBody = job.toString()
                        } else {
                            statusCode = 404
                            responseBody = "{\"detail\":\"Job not found\"}"
                        }
                    }
                    path.contains("/api/library/") && method == "DELETE" -> {
                        val id = path.substringAfterLast("/")
                        db.deleteLibraryItem(id)
                        responseBody = "{\"status\":\"ok\"}"
                    }
                    else -> {
                        statusCode = 404
                        responseBody = "{\"detail\":\"Not found\"}"
                    }
                }

                respondToJs(requestId, statusCode, responseBody)
            } catch (e: Exception) {
                Log.e("AndroidBridge", "Error in API Call", e)
                respondToJs(requestId, 500, "{\"detail\":\"${e.message}\"}")
            }
        }
    }

    private suspend fun processJob(jobId: String, requestPayload: JSONObject) {
        val concept = requestPayload.optString("concept", "")
        val mode = requestPayload.optString("mode", "Standard")
        
        db.updateJob(jobId, JSONObject().apply {
            put("status", "running")
            put("updated_at", System.currentTimeMillis().toString())
        })

        try {
            val systemMsg = "You are a prompt generator expert. Produce a JSON matching this concept: $concept"
            val llmResponse = llm.generateCompletion(systemMsg, "Generate prompt for: $concept")
            
            // Assume we can extract JSON
            val resultJson = JSONObject(llmResponse)
            
            db.updateJob(jobId, JSONObject().apply {
                put("status", "completed")
                put("result", resultJson)
                put("updated_at", System.currentTimeMillis().toString())
            })
        } catch (e: Exception) {
            db.updateJob(jobId, JSONObject().apply {
                put("status", "failed")
                put("error", e.message)
                put("updated_at", System.currentTimeMillis().toString())
            })
        }
    }

    private fun respondToJs(requestId: String, statusCode: Int, body: String) {
        val escapedBody = body.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
        val js = "window.handleAndroidResponse('$requestId', $statusCode, \"$escapedBody\");"
        scope.launch(Dispatchers.Main) {
            webView.evaluateJavascript(js, null)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@SuppressLint("SetJavaScriptEnabled")
@Composable
fun MainScreen() {
    val context = LocalContext.current
    val sharedPrefs = context.getSharedPreferences("SunoPrefs", Context.MODE_PRIVATE)
    var apiKey by remember { mutableStateOf(sharedPrefs.getString("EMERGENT_LLM_KEY", "") ?: "") }
    var showSettings by remember { mutableStateOf(false) }

    val databaseHelper = remember { DatabaseHelper(context) }
    val llmService = remember(apiKey) { LlmService(apiKey) }
    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Suno Prompt Studio") },
                actions = {
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
            )
        }
    ) { paddingValues ->
        if (showSettings) {
            AlertDialog(
                onDismissRequest = { showSettings = false },
                title = { Text("Settings") },
                text = {
                    OutlinedTextField(
                        value = apiKey,
                        onValueChange = { apiKey = it },
                        label = { Text("Anthropic API Key") }
                    )
                },
                confirmButton = {
                    Button(onClick = {
                        sharedPrefs.edit().putString("EMERGENT_LLM_KEY", apiKey).apply()
                        showSettings = false
                    }) {
                        Text("Save")
                    }
                }
            )
        }

        Box(modifier = Modifier.padding(paddingValues).fillMaxSize()) {
            AndroidView(
                factory = { ctx ->
                    WebView(ctx).apply {
                        settings.javaScriptEnabled = true
                        settings.allowFileAccess = true
                        settings.allowFileAccessFromFileURLs = true
                        settings.allowUniversalAccessFromFileURLs = true
                        settings.domStorageEnabled = true

                        val bridge = AndroidBridge(databaseHelper, llmService, this, coroutineScope)
                        addJavascriptInterface(bridge, "Android")

                        webViewClient = object : WebViewClient() {
                            override fun onPageFinished(view: WebView?, url: String?) {
                                super.onPageFinished(view, url)
                                val jsOverride = """
                                    (function() {
                                        if (window.androidXhrInitialized) return;
                                        window.androidXhrInitialized = true;
                                        
                                        window.pendingAndroidRequests = {};
                                        
                                        window.handleAndroidResponse = function(requestId, status, body) {
                                            const req = window.pendingAndroidRequests[requestId];
                                            if (req) {
                                                req.resolve(status, body);
                                                delete window.pendingAndroidRequests[requestId];
                                            }
                                        };

                                        const OriginalXHR = window.XMLHttpRequest;
                                        function PatchedXHR() {
                                            const xhr = new OriginalXHR();
                                            let requestMethod = 'GET';
                                            let requestUrl = '';
                                            
                                            xhr.open = function(method, url, async, user, password) {
                                                requestMethod = method;
                                                requestUrl = url;
                                                // Call original open just to set state, but we'll prevent send if it's an API call
                                                return OriginalXHR.prototype.open.apply(this, arguments);
                                            };
                                            
                                            xhr.send = function(body) {
                                                if (requestUrl.includes('/api/')) {
                                                    const requestId = Math.random().toString(36).substring(7);
                                                    
                                                    // Define resolve callback
                                                    window.pendingAndroidRequests[requestId] = {
                                                        resolve: (status, resBody) => {
                                                            Object.defineProperty(xhr, 'readyState', { value: 4, configurable: true });
                                                            Object.defineProperty(xhr, 'status', { value: status, configurable: true });
                                                            Object.defineProperty(xhr, 'responseText', { value: resBody, configurable: true });
                                                            Object.defineProperty(xhr, 'response', { value: resBody, configurable: true });
                                                            if (xhr.onreadystatechange) xhr.onreadystatechange();
                                                            if (xhr.onload) xhr.onload();
                                                        }
                                                    };
                                                    
                                                    let path = requestUrl;
                                                    if (requestUrl.startsWith('http')) {
                                                        path = new URL(requestUrl).pathname;
                                                    }
                                                    
                                                    window.Android.makeApiCall(requestId, requestMethod, path, body || null);
                                                } else {
                                                    return OriginalXHR.prototype.send.apply(this, arguments);
                                                }
                                            };
                                            return xhr;
                                        }
                                        window.XMLHttpRequest = PatchedXHR;
                                    })();
                                """.trimIndent()
                                view?.evaluateJavascript(jsOverride, null)
                            }
                        }
                        loadUrl("file:///android_asset/index.html")
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}
