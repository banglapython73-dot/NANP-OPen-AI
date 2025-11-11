package com.example.superai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

// --- Data Classes for API communication ---
@Serializable
data class ApiResponse(
    val original_command: String? = null,
    val plan: ApiPlan? = null,
    val results: List<ApiResult>? = null,
    val error: String? = null,
    val message: String? = null
)

@Serializable
data class ApiPlan(
    val status: String,
    val plan: List<ApiTask>
)

@Serializable
data class ApiTask(
    val step: Int,
    val task: String,
    val params: Map<String, String>
)

@Serializable
data class ApiResult(
    val status: String,
    val result: String
)

// --- ViewModel to handle business logic ---
class MainViewModel : ViewModel() {
    private val _messages = mutableStateListOf<String>()
    val messages: List<String> = _messages

    private val _isLoading = mutableStateOf(false)
    val isLoading: State<Boolean> = _isLoading

    private val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
    }

    // IMPORTANT: Replace with your actual backend URL when deploying
    // For development, this points to the local server accessible from the Android emulator
    private val backendUrl = "http://10.0.2.2:8080/api/command"

    fun sendCommand(command: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _messages.add("You: $command")
            try {
                val response: ApiResponse = client.post(backendUrl) {
                    contentType(ContentType.Application.Json)
                    setBody(mapOf("command" to command))
                }.body()

                // Format and display the response
                val responseText = buildString {
                    append("AI:\n")
                    response.results?.forEach { result ->
                        if (result.status == "success") {
                            append("- ${result.result}\n")
                        } else {
                            append("- Error: ${result.result}\n")
                        }
                    }
                    if (response.error != null) {
                        append("Error: ${response.error}\n")
                    }
                    if (response.message != null) {
                        append("Info: ${response.message}\n")
                    }
                }
                _messages.add(responseText.trim())

            } catch (e: Exception) {
                _messages.add("AI: Error - Could not connect to the server or parse the response. Details: ${e.message}")
            } finally {
                _isLoading.value = false
            }
        }
    }
}

// --- Main Activity and Composable UI ---
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SuperAIChatScreen()
        }
    }
}

@Composable
fun SuperAIChatScreen(viewModel: MainViewModel = androidx.lifecycle.viewmodel.compose.viewModel()) {
    var text by remember { mutableStateOf("") }

    MaterialTheme {
        Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            LazyColumn(modifier = Modifier.weight(1f)) {
                items(viewModel.messages) { message ->
                    Text(text = message, modifier = Modifier.padding(vertical = 4.dp))
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(modifier = Modifier.fillMaxWidth()) {
                OutlinedTextField(
                    value = text,
                    onValueChange = { text = it },
                    modifier = Modifier.weight(1f),
                    label = { Text("Enter your command...") }
                )
                Spacer(modifier = Modifier.width(8.dp))
                Button(
                    onClick = {
                        if (text.isNotBlank()) {
                            viewModel.sendCommand(text)
                            text = ""
                        }
                    },
                    enabled = !viewModel.isLoading.value
                ) {
                    if (viewModel.isLoading.value) {
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                    } else {
                        Text("Send")
                    }
                }
            }
        }
    }
}
