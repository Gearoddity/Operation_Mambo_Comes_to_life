import os
import queue
import sys
import json
import threading
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Thread-safe queue for audio chunks from the microphone
q = queue.Queue()

trigger_active = False
timer_lock = threading.Lock()
cancel_event = threading.Event()


def activate_timer():
    global trigger_active
    with timer_lock:
        if trigger_active:
            return  # Already running
        trigger_active = True
        cancel_event.clear()  # Reset the cancel signal for this new session


    # Wait for 30 seconds, but check every 0.1 seconds if we were told to cancel
    for _ in range(300):  # 300 * 0.1 seconds = 30 seconds
        if cancel_event.is_set():
            break
        time.sleep(0.1)

    with timer_lock:
        trigger_active = False



def cancel_timer():
    """Call this function anytime you want to force the timer to stop immediately."""
    cancel_event.set()

def callback(indata, frames, time, status):
    """Callback function for the sounddevice input stream."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def main():
    # Verify model directory exists
    model_path = "model"
    if not os.path.exists(model_path):
        print(f"Error: Could not find the offline model folder ('{model_path}').")
        print("Please download a model from https://alphacephei.com/vosk/models and place it here.")
        sys.exit(1)

    print("Loading offline Vosk model... Please wait.")
    model = Model(model_path)

    # Vosk typically expects 16kHz mono audio
    samplerate = 16000

    print("\n==============================================")
    print(" Microphone is LIVE. Start speaking!")
    print(" Press Ctrl+C in the terminal to stop.")
    print("==============================================\n")

    try:
        # Open microphone stream using sounddevice
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            rec = KaldiRecognizer(model, samplerate)

            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    # Finalized sentence/phrase chunk
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        # Clear the partial line and print finalized text clearly
                        sys.stdout.write("\r\033[K")
                        print(f"[Transcribed]: {text}")
                        # --- ADD THIS CHECK ---
                        if "mambo" in text.lower():
                            threading.Thread(target=activate_timer, daemon=True).start()
                        if ("one" in text.lower() or "pills" in text.lower()) and trigger_active:
                            cancel_timer()
                            print("\n\n")
                        elif ("two" in text or "whether" in text.lower()) and trigger_active:
                            cancel_timer()
                            print("\n\n")
                        elif ("three" in text or "news" in text.lower()) and trigger_active:
                            cancel_timer()
                            print("\n\n")
                        elif ("for" in text or "schedule" in text.lower()) and trigger_active:
                            cancel_timer()
                            print("\n\n")
                        elif ("five" in text or "number five" in text.lower()) and trigger_active:
                            cancel_timer()
                            print("\n\n")
                else:
                    # Live partial results as you speak
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        sys.stdout.write(f"\r[Listening...]: {partial_text}")
                        sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\nStopping script. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()