import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import sys
import os
import webbrowser
from urllib import request
from bs4 import BeautifulSoup

hash_algorithms = ['md5', 'sha1', 'sha256', 'sha512']

copy_in_progress = False

current_version = "1.0"
update_available = False  

def calculate_hashes(filepath):
    if os.path.isfile(filepath):
        hash_values.clear()

        with open(filepath, 'rb') as f:
            data = f.read()

            for algorithm in hash_algorithms:
                hash_object = hashlib.new(algorithm)
                hash_object.update(data)
                hash_values[algorithm] = hash_object.hexdigest()

def compare_hashes():
    if file_path:
        compare_window = tk.Toplevel(root)
        compare_window.title("Compare Hashes")
        compare_window.geometry("300x200")

        compare_frame = ttk.LabelFrame(compare_window, text="Compare Hashes")
        compare_frame.pack(fill="both", expand="true", padx=20, pady=10)

        path_label = ttk.Label(compare_frame, text=f"File Path: {file_path}")
        path_label.pack()

        algorithm_var = tk.StringVar(compare_frame)
        algorithm_var.set("Select")
        algorithm_menu = ttk.OptionMenu(compare_frame, algorithm_var, *["Select"] + hash_algorithms)
        algorithm_menu.pack()

        hash_entry_label = ttk.Label(compare_frame, text="Enter Hash:")
        hash_entry_label.pack()

        hash_entry = ttk.Entry(compare_frame, width=40)
        hash_entry.pack()

        compare_button = ttk.Button(compare_frame, text="Compare", command=lambda: compare_selected_hash(compare_window, algorithm_var.get(), hash_entry.get()))
        compare_button.pack()

        close_button = ttk.Button(compare_frame, text="Close", command=compare_window.destroy)
        close_button.pack()

    else:
        messagebox.showerror("File Not Found", "Please provide a valid file path first.")

def compare_selected_hash(compare_window, selected_algorithm, input_hash):
    if selected_algorithm == "Select":
        messagebox.showerror("Invalid Selection", "Please select a valid hash algorithm.")
        return

    if file_path:
        input_hash = input_hash.strip()
        if input_hash:
            input_hash_lower = input_hash.lower()
            hash_object = hashlib.new(selected_algorithm.lower())
            hash_object.update(input_hash_lower.encode())
            entered_hash_lower = hash_object.hexdigest()

            if entered_hash_lower == hash_values[selected_algorithm].lower():
                messagebox.showinfo("Comparison Result", "Hashes match!")
            elif input_hash == hash_values[selected_algorithm]:
                messagebox.showinfo("Comparison Result", "Hashes match!")
            else:
                messagebox.showerror("Comparison Result", "Hashes do not match.")
    else:
        messagebox.showerror("File Not Found", "Please provide a valid file path first.")

def open_latest_release_page():
    github_url = "https://github.com/conontron/showmyhash"
    latest_release_url = f"{github_url}/releases/latest"

    try:
        webbrowser.open(latest_release_url) 
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the latest release page: {str(e)}")

def update_check():
    global update_available
    github_url = "https://github.com/conontron/showmyhash"

    try:
        response = request.urlopen(github_url + "/releases")
        soup = BeautifulSoup(response.read(), 'html.parser')

        latest_version_tag = soup.select_one('a[href*="/releases/tag/"]')
        latest_version = latest_version_tag.text.strip()

        if latest_version != current_version:
            update_available = True
            update_message = f"Newer version {latest_version} is available. Do you want to open the latest release page on GitHub?"
            open_github_page = messagebox.askyesno("Update Available", update_message)
            if open_github_page:
                open_latest_release_page()
        else:
            messagebox.showinfo("No Updates", "No updates are available.")

    except Exception as e:
        messagebox.showerror("Update Error", f"Error checking for updates: {str(e)}")

def update_sorted_hashes(hash_values):
    sorted_hashes = sorted(hash_values.items(), key=lambda x: x[0])
    sorted_text = "\n".join([f"{algorithm.upper()} Hash: {value}" for algorithm, value in sorted_hashes])

    result_label.config(text=sorted_text)

def show_sorted_hashes(hash_values):
    global result_window, result_label

    result_window = tk.Toplevel(root)
    result_window.title("ShowMyHash")
    result_window.geometry("900x350")

    result_frame = ttk.LabelFrame(result_window, text="Hash Values")
    result_frame.pack(fill="both", expand="true", padx=20, pady=10)

    sorted_hashes = sorted(hash_values.items(), key=lambda x: x[0])
    sorted_text = "\n".join([f"{algorithm.upper()} Hash: {value}" for algorithm, value in sorted_hashes])

    file_path_label = ttk.Label(result_frame, text=f"File Path: {file_path}")
    file_path_label.pack(pady=5)

    result_label = tk.Label(result_frame, text=sorted_text, font=("Helvetica", 8))
    result_label.pack(padx=10, pady=5)

    compare_button = ttk.Button(result_frame, text="Compare Hashes", command=compare_hashes)
    compare_button.pack(pady=5)

    copy_button = ttk.Button(result_frame, text="Copy Hashes", command=lambda: copy_hashes(hash_values))
    copy_button.pack(pady=5)
    
    update_button = ttk.Button(result_frame, text="Check for Updates", command=update_check)
    update_button.pack(pady=5)

    about_button = ttk.Button(result_frame, text="About", command=open_about_window)
    about_button.pack(pady=5)
    
    close_button = ttk.Button(result_frame, text="Close", command=close_application)
    close_button.pack(pady=5)

    result_window.protocol("WM_DELETE_WINDOW", close_show_hashes)
    result_window.mainloop()

def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x256")

    about_frame = ttk.LabelFrame(about_window, text="About")
    about_frame.pack(fill="both", expand="true", padx=20, pady=10)

    creator_label = ttk.Label(about_frame, text="Made by Conontron", font=("Helvetica", 12))
    creator_label.pack(pady=5)

    version_label = ttk.Label(about_frame, text=f"Version: {current_version}", font=("Helvetica", 10))
    version_label.pack(pady=5)

    twitter_button = ttk.Button(about_frame, text="Twitter", command=open_twitter)
    twitter_button.pack(pady=5)

    github_button = ttk.Button(about_frame, text="GitHub", command=open_github)
    github_button.pack(pady=5)

    license_button = ttk.Button(about_frame, text="License", command=open_license)
    license_button.pack(pady=5)

    close_button = ttk.Button(about_frame, text="Close", command=about_window.destroy)
    close_button.pack(pady=10)

def open_twitter():
    webbrowser.open('https://twitter.com/conontron')

def open_github():
    webbrowser.open('https://github.com/conontron')

def open_license():
    webbrowser.open('https://github.com/Conontron/ShowMyHash/blob/main/LICENSE')    

def close_application():
    root.destroy()
    sys.exit(0)

def close_show_hashes():
    global result_window
    result_window.destroy()
    close_application()

def copy_hashes(hash_values):
    global copy_in_progress

    if copy_in_progress:
        return

    copy_in_progress = True

    hashes_text = "\n".join([f"{algorithm.upper()} Hash: {value}" for algorithm, value in hash_values.items()])
    root.clipboard_clear()
    root.clipboard_append(hashes_text)
    root.update()

    success_message = "Hashes have been copied to the clipboard."
    messagebox.showinfo("Hashes Copied", success_message)

    copy_in_progress = False

hash_values = {}
file_path = ""

def close_main_window():
    root.destroy()
    sys.exit(0)

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    calculate_hashes(file_path)
else:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if not file_path:
        sys.exit(0)

calculate_hashes(file_path)
root = tk.Tk()
root.withdraw()
show_sorted_hashes(hash_values)

root.protocol("WM_DELETE_WINDOW", close_main_window)

tk.mainloop()
