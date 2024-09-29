import tkinter as tk
import time
from datetime import time as datetime_time
import winsound  # to import system sound

paused = False
remtime = 0
reset_fn = False
animate_hourglass = True  # Control flag for animation

def countdown(ti):
    global paused, remtime, animate_hourglass
    if not reset_fn:
        if not paused and ti >= 0:
            displaytime = timeconvert(ti)
            remtime = ti
            display_time.configure(text=f"{displaytime}")
            root.after(1000, countdown, ti - 1)
            ti = ti - 1
        elif ti < 0:
            display_time.configure(text="Time up!")
            animate_hourglass = False  # Stop the hourglass animation
            for i in range(4):
                winsound.Beep(875, 250)  # System sound
                winsound.Beep(1000, 400)
            restore_start_button()
            remove_stopbutton_buttons()
            remove_resume_buttons()
            remove_reset_buttons()
        else:
            remtime = ti
            display_time.configure(text=f"{timeconvert(remtime)}")

def convert(h, m, s):
    seconds = (h * 3600) + (m * 60) + s
    return seconds

def timeconvert(ti):
    Hr, remainder = divmod(ti, 3600)  # Calculate hours, remainder seconds
    Min, Sec = divmod(remainder, 60)  # Calculate minutes, seconds
    timeformat = datetime_time(Hr, Min, Sec)
    return timeformat

def funct():
    global paused, remtime, reset_fn, animate_hourglass
    reset_fn = False
    paused=False
    hr = int(hour_spin.get())
    min = int(min_spin.get())   # to take the input from the user
    sec = int(sec_spin.get())

    ti = convert(hr, min, sec)
    remove_start_button()
    animate_hourglass = True               # Allow hourglass animation
    update_hourglass()                     # Start the hourglass animation
    restore_stopbutton_buttons()           # to hide buttons
    restore_reset_buttons()
    countdown(ti)

def pause():
    remove_stopbutton_buttons()
    restore_resume_buttons()
    global paused
    paused = True  # Set the paused state to True

def resume():
    restore_stopbutton_buttons()
    remove_resume_buttons()
    global paused, remtime
    paused = False      # Resume countdown by unsetting paused
    update_hourglass()  # Resume the hourglass animation
    countdown(remtime)  # Continue from the remaining time

def reset():
    global remtime, paused, reset_fn, animate_hourglass
    paused = True
    reset_fn = True
    remtime = 0
    timeformat = datetime_time(00, 00, 00)                   # to reset time to 00:00:00
    display_time.configure(text=f"{timeformat}")
    restore_start_button()
    remove_stopbutton_buttons()
    remove_resume_buttons()
    remove_reset_buttons()
    animate_hourglass = False                            # Stop the hourglass animation
    hourglass_label.configure(image=hourglass_frames[0])  # Reset hourglass to the first frame

def remove_start_button():
    button.grid_forget()  # to hide the start button

def restore_start_button():
    button.grid(row=3, column=2, columnspan=2, pady=10)  # to bring back the start button

def remove_stopbutton_buttons():
    stopbutton.grid_forget()

def restore_stopbutton_buttons():
    stopbutton.grid(row=4, column=1, columnspan=2, pady=10)  # to bring back the pause button

def remove_resume_buttons():
    resumebutton.grid_forget()

def restore_resume_buttons():
    resumebutton.grid(row=4, column=1, columnspan=2, pady=10)  # to bring back the resume button

def remove_reset_buttons():
    resetbutton.grid_forget()

def restore_reset_buttons():
    resetbutton.grid(row=4, column=3, columnspan=2, pady=10)  # to bring back the reset button

root = tk.Tk()
root.geometry("500x400")
root.title("TIMER")
root.configure(bg="ghost white")  # Set background to white

# Configure the grid layout
for i in range(6):
    root.columnconfigure(i, weight=1)
for i in range(5):
    root.rowconfigure(i, weight=1)

# Load the hourglass gif and its frames
try:
    hourglass_frames = [tk.PhotoImage(file="icons8-hourglass.gif", format=f'gif -index {i}') for i in range(10)]         # Load first 10 frames
except tk.TclError:
    print("Error: Unable to load the hourglass image. Check the file path and extension.")

current_frame = 0

def update_hourglass():                                              #to move hour glass animation      
    global current_frame, animate_hourglass
    if not paused and animate_hourglass and hourglass_frames:
        hourglass_label.configure(image=hourglass_frames[current_frame])
        current_frame = (current_frame + 1) % len(hourglass_frames)                           # Loop back to the first frame
        root.after(100, update_hourglass)          # Update every 100 milliseconds

# Title
label = tk.Label(root, text="TIMER", font=("Courier", 24, "bold"), bg="ghost white")           # Large bold title
label.grid(row=0, column=2, columnspan=2, pady=10)

# Spinbox and labels for hours, minutes, and seconds
hour_label = tk.Label(root, text="Hour:", font=("Arial", 12), bg="ghost white")
hour_label.grid(row=1, column=0, padx=(10,2), pady=10, sticky="e")

hour_spin = tk.Spinbox(root, from_=00, to=100, width=5, font=("Arial", 12))
hour_spin.grid(row=1, column=1, padx=(0,10), pady=10, sticky="w")

min_label = tk.Label(root, text="Minutes:", font=("Arial", 12), bg="ghost white")
min_label.grid(row=1, column=2, padx=(10,0), pady=10, sticky="e")

min_spin = tk.Spinbox(root, from_=00, to=60, width=5, font=("Arial", 12))
min_spin.grid(row=1, column=3, padx=(0,10), pady=10, sticky="w")

sec_label = tk.Label(root, text="Seconds:", font=("Arial", 12), bg="ghost white")
sec_label.grid(row=1, column=4, padx=(10,0), pady=10, sticky="e")

sec_spin = tk.Spinbox(root, from_=00, to=60, width=5, font=("Arial", 12))
sec_spin.grid(row=1, column=5, padx=(0,10), pady=10, sticky="w")

# Timer display
display_time = tk.Label(root, text="00:00:00", fg="white", font=("Courier", 24, "bold"), width=8, bg="gray14")  # digital-style font for timer
display_time.grid(row=2, column=2, columnspan=2, pady=10)

# Hourglass animation
hourglass_label = tk.Label(root, image=hourglass_frames[0])  # Set initial frame
hourglass_label.grid(row=3, column=2, columnspan=2, pady=10)

# Buttons with color styling
button = tk.Button(root, text="Start", command=funct, bg="RoyalBlue2", fg="white", font=("Arial", 12), width=10)  # Blue Start button
button.grid(row=3, column=2, columnspan=2, pady=10)

stopbutton = tk.Button(root, text="Pause", command=pause, bg="orange", fg="white", font=("Arial", 12), width=10)  # Orange Pause button
stopbutton.grid(row=4, column=1, columnspan=2, pady=10)

resumebutton = tk.Button(root, text="Resume", command=resume, bg="green", fg="white", font=("Arial", 12), width=10)  # Green Resume button
resumebutton.grid(row=4, column=1, columnspan=2, pady=10)

resetbutton = tk.Button(root, text="Reset", command=reset, bg="red", fg="white", font=("Arial", 12), width=10)      # Red Reset button
resetbutton.grid(row=4, column=3, columnspan=2, pady=10)

# Initial button states
remove_stopbutton_buttons()
remove_resume_buttons()
remove_reset_buttons()

root.mainloop()
