
import tkinter as tk
from mambo_gui import MamboGUI


def main():
    # Create the main window
    root = tk.Tk()

    # Create the Mambo graphical interface
    gui = MamboGUI(root)

    # Display sample calendar events
    gui.update_calendar([
        "10:00 AM - Project Meeting",
        "2:00 PM - Engineering Class",
        "4:30 PM - Study Session"
    ])

    # Set initial assistant status
    gui.set_listening(False)

    # Start the graphical interface
    root.mainloop()


if __name__ == "__main__":
    main()
