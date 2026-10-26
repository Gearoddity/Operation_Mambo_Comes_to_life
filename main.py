from voice_listener import SimpleListener
from Active_Variable import wake

wake_word = wake()





def handle_spoken_text(text):
    print(f"[MAIN RECEIVED]: {text}")

    if "main" in text.lower() or "mambo" in text.lower():
        print("[MAIN RECEIVED]")
        wake_word.active_timer()
    elif "whether" in text.lower() and wake_word.check_active():
        print("[WEATHER RECEIVED]")
        wake_word.force_stop()
    elif "hills" in text.lower() and wake_word.check_active():
        print("[PILLS RECEIVED]")
        wake_word.force_stop()
    elif "news" in text.lower() and wake_word.check_active():
        print("[NEWS RECEIVED]")
        wake_word.force_stop()
    elif "schedule" in text.lower() and wake_word.check_active():
        print("[SCHEDULE RECEIVED]")
        wake_word.force_stop()
    elif "number five" in text.lower() and wake_word.check_active():
        print("[NUMBER FIVE RECEIVED]")
        wake_word.force_stop()

def main():
    listener = SimpleListener(model_path="model", callback=handle_spoken_text)

    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()


if __name__ == "__main__":
    main()