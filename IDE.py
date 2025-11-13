import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Mini IDE - Thari Edition")
root.geometry("900x600")

# ---------------- Menu Bar ----------------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def open_file():
    path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if path:
        with open(path, "r") as f:
            code_area.delete("1.0", tk.END)
            code_area.insert(tk.END, f.read())

def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if path:
        with open(path, "w") as f:
            f.write(code_area.get("1.0", tk.END))

def exit_app():
    root.destroy()

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# ---------------- Toolbar ----------------
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

def run_code():
    code = code_area.get("1.0", tk.END)
    try:
        with open("temp_code.py", "w") as f:
            f.write(code)
        output = subprocess.check_output(["python", "temp_code.py"], stderr=subprocess.STDOUT, text=True)
        console_area.config(state=tk.NORMAL)
        console_area.delete("1.0", tk.END)
        console_area.insert(tk.END, output)
        console_area.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        console_area.config(state=tk.NORMAL)
        console_area.delete("1.0", tk.END)
        console_area.insert(tk.END, e.output)
        console_area.config(state=tk.DISABLED)

def clear_console():
    console_area.config(state=tk.NORMAL)
    console_area.delete("1.0", tk.END)
    console_area.config(state=tk.DISABLED)

run_btn = tk.Button(toolbar, text="Run", command=run_code)
run_btn.pack(side=tk.LEFT, padx=2, pady=2)
clear_btn = tk.Button(toolbar, text="Clear Console", command=clear_console)
clear_btn.pack(side=tk.LEFT, padx=2, pady=2)

# ---------------- Code Editor ----------------
code_frame = tk.Frame(root)
code_frame.pack(fill=tk.BOTH, expand=True)

line_numbers = tk.Text(code_frame, width=4, padx=3, takefocus=0, border=0,
                       background='lightgrey', state='disabled')
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

code_area = tk.Text(code_frame, font=("Consolas", 12), undo=True)
code_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
scroll_bar = tk.Scrollbar(code_frame, command=code_area.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
code_area.config(yscrollcommand=scroll_bar.set)

# Add basic syntax highlighting
Percolator(code_area).insertfilter(ColorDelegator())

def auto_close_brace(event):
    # Define opening -> closing pairs
    pairs = {"(": ")", "[": "]", "{": "}", '"': '"', "'": "'"}
    char = event.char

    if char in pairs:
        # Insert the opening and closing brace
        code_area.insert(tk.INSERT, char + pairs[char])
        # Move cursor back between the braces
        code_area.mark_set(tk.INSERT, f"{code_area.index(tk.INSERT)}-1c")
        return "break"  # Prevent default insertion of the typed character

# Bind it to the code_area
code_area.bind("<Key>", auto_close_brace)

# ---------------- Console ----------------
console_label = tk.Label(root, text="Console Output")
console_label.pack()
console_area = scrolledtext.ScrolledText(root, height=10, font=("Consolas", 11), state=tk.DISABLED, background="black", foreground="white")
console_area.pack(fill=tk.BOTH, padx=5, pady=5)

# ---------------- Default Sample Code ----------------
sample_code = '''print("Hello, Thari IDE!")
for i in range(5):
    print("Line", i+1)
'''
code_area.insert(tk.END, sample_code)

# ---------------- Run App ----------------
root.mainloop()
