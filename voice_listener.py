import os
import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class VoiceListener:
    def __init__(self, on_command_callback):
        self.q = queue.Queue()
        self.on_command_callback = on_command_callback  # Function to call when text is recognized

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def start_listening(self):
        model_path = "model"
        if not os.path.exists(model_path):
            print(f"Error: Could not find the offline model folder ('{model_path}').")
            sys.exit(1)

        print("Loading offline Vosk model... Please wait.")
        model = Model(model_path)
        samplerate = 16000

        print("\n==============================================")
        print(" Microphone is LIVE. Speak your commands!")
        print("==============================================\n")

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                               channels=1, callback=self._audio_callback):
            rec = KaldiRecognizer(model, samplerate)

            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()

                    if text:
                        sys.stdout.write("\r\033[K")
                        print(f"[Transcribed]: {text}")
                        # Send text to main handler
                        self.on_command_callback(text)
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        sys.stdout.write(f"\r[Listening...]: {partial_text}")
                        sys.stdout.flush()