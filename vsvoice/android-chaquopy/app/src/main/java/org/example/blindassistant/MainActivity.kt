package org.example.blindassistant

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.util.Locale

class MainActivity : AppCompatActivity(), TextToSpeech.OnInitListener {

    private lateinit var input: EditText
    private lateinit var status: TextView
    private lateinit var tts: TextToSpeech
    private lateinit var pyModule: PyObject

    private val speechLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            val text = result.data
                ?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                ?.firstOrNull()
                .orEmpty()
            input.setText(text)
            handleCommand(text)
        } else {
            updateStatus("Could not understand voice command.")
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        input = findViewById(R.id.commandInput)
        status = findViewById(R.id.statusText)
        val runButton: Button = findViewById(R.id.runButton)
        val listenButton: Button = findViewById(R.id.listenButton)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        pyModule = Python.getInstance().getModule("assistant_core")

        tts = TextToSpeech(this, this)

        runButton.setOnClickListener {
            handleCommand(input.text.toString())
        }

        listenButton.setOnClickListener {
            startSpeechInput()
        }

        ensureAudioPermission()
    }

    override fun onDestroy() {
        tts.stop()
        tts.shutdown()
        super.onDestroy()
    }

    override fun onInit(statusCode: Int) {
        if (statusCode == TextToSpeech.SUCCESS) {
            tts.language = Locale.getDefault()
        }
    }

    private fun ensureAudioPermission() {
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.RECORD_AUDIO
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                1001
            )
        }
    }

    private fun startSpeechInput() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
            putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak command")
        }
        speechLauncher.launch(intent)
    }

    private fun handleCommand(raw: String) {
        val response = pyModule.callAttr("process_command", raw).toString()
        val parts = response.split("|", limit = 3)

        val action = parts.getOrElse(0) { "say" }
        val payload = parts.getOrElse(1) { "" }
        val message = parts.getOrElse(2) { "Done" }

        when (action) {
            "open_app" -> openApp(payload)
            "navigate" -> navigateTo(payload)
            else -> {}
        }

        updateStatus(message)
    }

    private fun openApp(packageName: String) {
        val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
        if (launchIntent != null) {
            startActivity(launchIntent)
        } else {
            updateStatus("App is not installed.")
        }
    }

    private fun navigateTo(place: String) {
        val uri = Uri.parse("google.navigation:q=${Uri.encode(place)}")
        val navIntent = Intent(Intent.ACTION_VIEW, uri).apply {
            setPackage("com.google.android.apps.maps")
        }
        startActivity(navIntent)
    }

    private fun updateStatus(msg: String) {
        status.text = msg
        tts.speak(msg, TextToSpeech.QUEUE_FLUSH, null, "assistant")
    }
}