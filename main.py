import threading
import time
import tkinter as tk

from voice_listener import VoiceListener
from dashboard_ui import DashboardApp

# --- STATE VARIABLES & TIMER LOGIC ---
trigger_active = False
timer_lock = threading.Lock()
cancel_event = threading.Event()


def get_trigger_status():
    with timer_lock:
        return trigger_active


def activate_timer():
    global trigger_active
    with timer_lock:
        if trigger_active:
            return
        trigger_active = True
        cancel_event.clear()

    print("\n[EVENT]: 'mambo' detected! Variable is TRUE for 30 seconds.")

    for _ in range(300):
        if cancel_event.is_set():
            break
        time.sleep(0.1)

    with timer_lock:
        trigger_active = False
    print("\n[EVENT]: Timer ended. Variable is FALSE.")


def main():
    # Reference to GUI app (will be assigned once initialized)
    app_ref = {"ui": None}

    def handle_voice_command(text):
        text_lower = text.lower()

        if "mambo" in text_lower:
            threading.Thread(target=activate_timer, daemon=True).start()
        elif "news" in text_lower or "one" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("news")
        elif "pills" in text_lower or "two" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("pills")
        elif "schedule" in text_lower or "three" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("schedule")
        elif "weather" in text_lower or "four" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("weather")
        elif "number five" in text_lower or "five" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("five")
        elif "home" in text_lower or "main" in text_lower:
            if app_ref["ui"]: app_ref["ui"].switch_screen("home")

    # Initialize Voice Listener
    listener = VoiceListener(on_command_callback=handle_voice_command)

    # Start listener in a background thread
    listener_thread = threading.Thread(target=listener.start_listening, daemon=True)
    listener_thread.start()

    # Start Tkinter GUI on the main thread
    root = tk.Tk()
    app = DashboardApp(root, get_trigger_status_func=get_trigger_status)
    app_ref["ui"] = app

    root.mainloop()


if __name__ == "__main__":
    main()