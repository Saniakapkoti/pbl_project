import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os

# Setting Up Files
PHASE_FILES = {
    "Tokens": "tokens.txt",
    "Symbol Table": "symbol_table.txt",
    "Intermediate Code": "intermediate_code.txt",
    "Optimized Code": "optimized_code.txt"
}

def run_icg():
    try:
        with open("test.cpp", "w") as f:
            f.write(code_input.get("1.0", tk.END))
        subprocess.run(["python", "icg.py"], check=True)
        messagebox.showinfo("Success", "Compilation complete.")
        load_outputs()
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Compilation failed. Check your code.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_outputs():
    for tab_name, file_name in PHASE_FILES.items():
        tab = output_tabs[tab_name]
        tab.config(state=tk.NORMAL)
        tab.delete("1.0", tk.END)
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                tab.insert(tk.END, f.read())
        else:
            tab.insert(tk.END, "File not generated.")
        tab.config(state=tk.DISABLED)

def load_test_file():
    # Open file dialog to select a C++ file
    file_path = filedialog.askopenfilename(filetypes=[("C++ Files", "*.cpp")])

    if file_path:  # Ensure file is selected
        try:
            with open(file_path, "r") as f:
                code_input.delete("1.0", tk.END)  # Clear any existing code
                code_input.insert(tk.END, f.read())  # Load the selected file content
            print(f"Successfully loaded file: {file_path}")
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading file: {e}")
            print(f"Error loading file: {e}")
    else:
        print("No file selected.")

# GUI Setup
root = tk.Tk()
root.title("Intermediate Code Generator (C++ → TAC)")
root.geometry("950x700")

style = ttk.Style(root)
style.theme_use("clam")

# Input Frame
input_frame = ttk.LabelFrame(root, text="C++ Code Input")
input_frame.pack(fill="both", expand=False, padx=10, pady=10)

code_input = tk.Text(input_frame, height=15, font=("Courier", 12))
code_input.pack(fill="both", expand=True, padx=5, pady=5)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=5)

ttk.Button(btn_frame, text="Load File", command=load_test_file).pack(side="left", padx=10)
ttk.Button(btn_frame, text="Compile", command=run_icg).pack(side="left", padx=10)

# Output Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

output_tabs = {}
for tab_name in PHASE_FILES:
    frame = tk.Text(notebook, wrap="none", font=("Courier", 11))
    frame.insert(tk.END, f"{tab_name} will appear here.")
    frame.config(state=tk.DISABLED)
    output_tabs[tab_name] = frame
    notebook.add(frame, text=tab_name)

root.mainloop()
