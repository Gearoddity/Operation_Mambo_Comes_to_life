import tkinter as tk
import time
import threading


class DashboardApp:
    def __init__(self, root, get_trigger_status_func):
        self.root = root
        self.root.title("Multi-Screen Voice Dashboard")
        self.root.geometry("800x480")

        self.get_trigger_status_func = get_trigger_status_func

        # Container frame to hold all screens
        # Container frame to hold all screens (with aura border support)
        self.container = tk.Frame(root, highlightbackground="#1e1e1e", highlightthickness=0)
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.screens = {}

        # Build views
        self.create_home_screen()
        self.create_news_screen()
        self.create_pills_screen()
        self.create_schedule_screen()
        self.create_weather_screen()
        self.create_

        # Start on home screen
        self.switch_screen("home")

        # Start loops
        self.update_clock()
        self.update_status()

    def create_home_screen(self):
        frame = tk.Frame(self.container, bg="#1e1e1e")
        frame.grid(row=0, column=0, sticky="nsew")

        # Clock label
        self.home_clock = tk.Label(frame, text="", font=("Helvetica", 64, "bold"), fg="white", bg="#1e1e1e")
        self.home_clock.pack(pady=(60, 0))  # Packed with top padding

        # --- ADD DATE LABEL HERE ---
        self.home_date = tk.Label(frame, text="", font=("Helvetica", 20), fg="#bbbbbb", bg="#1e1e1e")
        self.home_date.pack(pady=(0, 20))

        # Status labels...
        self.home_status = tk.Label(frame, text="Status: Waiting for trigger...", font=("Helvetica", 22), fg="#aaaaaa",
                                    bg="#1e1e1e")
        self.home_status.pack(pady=10)

        self.home_detail = tk.Label(frame, text="Say 'News', 'Pills', 'Schedule', 'Weather', or 'Mambo'",
                                    font=("Helvetica", 14), fg="#666666", bg="#1e1e1e")
        self.home_detail.pack(pady=10)

        self.screens["home"] = frame

    def create_news_screen(self):
        frame = tk.Frame(self.container, bg="#0f172a")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="📰 LATEST NEWS", font=("Helvetica", 32, "bold"), fg="#38bdf8", bg="#0f172a").pack(pady=40)
        tk.Label(frame, text="• Local headline placeholder 1\n• Global tech update placeholder 2",
                 font=("Helvetica", 20), fg="white", bg="#0f172a", justify="left").pack(pady=20)
        self.screens["news"] = frame

    def create_pills_screen(self):
        frame = tk.Frame(self.container, bg="#451a03")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="💊 MEDICATION REMINDERS", font=("Helvetica", 32, "bold"), fg="#fb923c", bg="#451a03").pack(
            pady=40)
        tk.Label(frame, text="Next Dose: Vitamin D & Omega-3\nTime: 08:00 PM (Status: Pending)", font=("Helvetica", 20),
                 fg="white", bg="#451a03").pack(pady=20)
        self.screens["pills"] = frame

    def create_schedule_screen(self):
        frame = tk.Frame(self.container, bg="#064e3b")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="📅 TODAY'S SCHEDULE", font=("Helvetica", 32, "bold"), fg="#34d399", bg="#064e3b").pack(
            pady=40)
        tk.Label(frame, text="10:00 AM - Team Sync\n02:30 PM - Doctor Appointment", font=("Helvetica", 20), fg="white",
                 bg="#064e3b").pack(pady=20)
        self.screens["schedule"] = frame

    def create_weather_screen(self):
        frame = tk.Frame(self.container, bg="#1e3a8a")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="🌤️ WEATHER FORECAST", font=("Helvetica", 32, "bold"), fg="#60a5fa", bg="#1e3a8a").pack(
            pady=40)
        tk.Label(frame, text="72°F - Partly Cloudy\nHumidity: 45% | Wind: 8 mph NW", font=("Helvetica", 20), fg="white",
                 bg="#1e3a8a").pack(pady=20)
        self.screens["weather"] = frame

    def switch_screen(self, screen_name):
        if screen_name in self.screens:
            self.root.after(0, lambda: self.screens[screen_name].tkraise())

            detail_messages = {
                "home": "Say 'News', 'Pills', 'Schedule', 'Weather', or 'Mambo'",
                "news": "Currently displaying: News Feed",
                "pills": "Currently displaying: Medication Reminders",
                "schedule": "Currently displaying: Daily Schedule",
                "weather": "Currently displaying: Weather Forecast"
            }
            if screen_name in detail_messages:
                self.home_detail.config(text=detail_messages[screen_name])

            print(f"\n[UI EVENT]: Switched screen to -> {screen_name}")

    def update_clock(self):
        # Update both time and date formats
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%A, %B %d, %Y")  # Example: Monday, October 19, 2026

        self.home_clock.config(text=current_time)
        self.home_date.config(text=current_date)

        self.root.after(1000, self.update_clock)

    def update_status(self):
        if not hasattr(self, "_last_active_state"):
            self._last_active_state = False

        is_active = self.get_trigger_status_func()

        if is_active:
            self.home_status.config(text="Status: MAMBO ACTIVE (30s countdown)", fg="#2ecc71")
            # Turn ON the glowing neon aura border around the screen
            self.container.config(highlightbackground="#00ffcc", highlightthickness=10)
        else:
            self.home_status.config(text="Status: IDLE / Ready", fg="#e74c3c")
            # Turn OFF the aura border when the timer ends
            self.container.config(highlightthickness=0)

            if self._last_active_state and not is_active:
                self.switch_screen("home")

        self._last_active_state = is_active
        self.root.after(100, self.update_status)