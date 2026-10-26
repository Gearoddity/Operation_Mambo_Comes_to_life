import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer


class SimpleListener:
    def __init__(self, model_path="model", callback=None):
        self.model_path = model_path
        self.callback = callback
        self.is_running = False

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Error: '{self.model_path}' folder not found. Make sure your Vosk model is here.")

        print("Loading model...")
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        """Starts the microphone stream and listening loop."""
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()
        self.is_running = True

        print("\n--- LISTENING --- (Speak into your mic, press Ctrl+C to exit)")

        try:
            while self.is_running:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        # If a callback function was provided, pass the text to it!
                        if self.callback:
                            self.callback(text)
                        else:
                            print(f"Heard (no callback): {text}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()

    def stop(self):
        self.is_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        print("Listener stopped.")