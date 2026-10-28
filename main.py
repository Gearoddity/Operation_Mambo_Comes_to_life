from voice_listener import SimpleListener
from Active_Variable import wake
from Graphics_processing import MamboScreens
wake_word = wake()
mambo = MamboScreens()




def handle_spoken_text(text):
    print(f"[MAIN RECEIVED]: {text}")

    if "main" in text.lower() or "mambo" in text.lower():
        print("[MAIN RECEIVED]")
        wake_word.active_timer()
        if mambo.get_current_screen() != "Home":
            mambo.show_screen("Home")
    elif "whether" in text.lower() and wake_word.check_active():
        print("[WEATHER RECEIVED]")
        wake_word.force_stop()
        if mambo.get_current_screen() != "Weather":
            mambo.show_screen("Weather")
    elif "hills" in text.lower() and wake_word.check_active():
        print("[PILLS RECEIVED]")
        wake_word.force_stop()
        if mambo.get_current_screen() != "Pills":
            mambo.show_screen("Pills")
    elif "news" in text.lower() and wake_word.check_active():
        print("[NEWS RECEIVED]")
        wake_word.force_stop()
        if mambo.get_current_screen() != "News":
            mambo.show_screen("News")
    elif "schedule" in text.lower() and wake_word.check_active():
        print("[SCHEDULE RECEIVED]")
        wake_word.force_stop()
        if mambo.get_current_screen() != "Schedule":
            mambo.show_screen("Schedule")
    elif "number five" in text.lower() and wake_word.check_active():
        print("[NUMBER FIVE RECEIVED]")
        wake_word.force_stop()
        if mambo.get_current_screen() != "Number5":
            mambo.show_screen("Number5")

def main():
    listener = SimpleListener(model_path="model", callback=handle_spoken_text)

    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()


if __name__ == "__main__":
    main()