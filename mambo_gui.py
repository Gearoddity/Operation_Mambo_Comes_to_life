
import tkinter as tk
from datetime import datetime


class MamboGUI:
    def __init__(self, root):
        # Store main window
        self.root = root
        self.root.title("Mambo Smart Assistant")
        self.root.geometry("800x480")
        self.root.configure(bg="#101A27")

        # Title
        self.title = tk.Label(
            root,
            text="MAMBO",
            font=("Arial", 30, "bold"),
            fg="white",
            bg="#101A27"
        )
        self.title.pack(pady=15)

        # Clock display
        self.clock = tk.Label(
            root,
            font=("Arial", 32),
            fg="white",
            bg="#101A27"
        )
        self.clock.pack()

        # Date display
        self.date_label = tk.Label(
            root,
            font=("Arial", 14),
            fg="#A4B6CB",
            bg="#101A27"
        )
        self.date_label.pack(pady=5)

        # Assistant status
        self.status = tk.Label(
            root,
            text="Mambo is ready",
            font=("Arial", 18),
            fg="#63DCC1",
            bg="#101A27"
        )
        self.status.pack(pady=20)

        # Calendar section
        self.calendar = tk.Label(
            root,
            text="No calendar events loaded",
            font=("Arial", 14),
            fg="white",
            bg="#1E3042",
            width=45,
            height=5,
            justify="left"
        )
        self.calendar.pack(pady=10)

        # Buttons
        self.calendar_button = tk.Button(
            root,
            text="Show Calendar",
            font=("Arial", 14),
            command=self.show_calendar
        )
        self.calendar_button.pack(pady=10)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        self.clock.config(
            text=now.strftime("%I:%M:%S %p")
        )

        self.date_label.config(
            text=now.strftime("%A, %B %d, %Y")
        )

        # Refresh every second
        self.root.after(1000, self.update_clock)

    def set_listening(self, listening):
        if listening:
            self.status.config(
                text="Mambo is listening...",
                fg="#FFDD77"
            )
        else:
            self.status.config(
                text="Mambo is ready",
                fg="#63DCC1"
            )

    def update_calendar(self, events):
        if not events:
            self.calendar.config(
                text="No upcoming events"
            )
        else:
            self.calendar.config(
                text="\n".join(events)
            )

    def show_calendar(self):
        # Temporary sample data
        events = [
            "9:00 AM - Team Meeting",
            "1:30 PM - Engineering Lab",
            "5:00 PM - Study Session"
        ]

        self.update_calendar(events)


if __name__ == "__main__":
    root = tk.Tk()
    app = MamboGUI(root)
    root.mainloop()
