import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os


VERSION = "1.0.0"

def process(input_files, output_file):
    raise NotImplementedError("You must implement the process() function")

def runGUI():
    input_files = []
    output_file = None
    last_dir = os.getcwd()

    def update_display():
        display.config(state=tk.NORMAL)
        display.delete("1.0", tk.END)
        if input_files:
            display.insert(tk.END, "Input files:\n")
            for f in input_files:
                display.insert(tk.END, f"  {f}\n")
        else:
            display.insert(tk.END, "Input files: (none selected)\n")
        display.insert(tk.END, "\n")
        display.insert(tk.END, f"Output file:\n  {output_file if output_file else '(none selected)'}\n")
        display.config(state=tk.DISABLED)

    def select_inputs():
        nonlocal input_files, last_dir
        selected = filedialog.askopenfilenames(
            title="Select input files",
            initialdir=last_dir,
            filetypes=[("Excel files", "*.xlsm *.xlsx *.xls"), ("All files", "*.*")]
        )
        if selected:
            input_files[:] = list(selected)
            last_dir = os.path.dirname(input_files[0])
            update_display()

    def select_output():
        nonlocal output_file, last_dir
        selected = filedialog.asksaveasfilename(
            title="Select output file",
            initialdir=last_dir,
            defaultextension=".xlsm",
            filetypes=[("Excel files", "*.xlsm *.xlsx *.xls"), ("All files", "*.*")]
        )
        if selected:
            output_file = selected
            last_dir = os.path.dirname(output_file)
            update_display()

    def on_ok():
        if not input_files or not output_file:
            messagebox.showerror("Missing files", "Please select both input files and an output file.")
            return
        root.destroy()
        process(input_files, output_file)

    def on_cancel():
        root.destroy()
        sys.exit(0)

    def handle_drop(event):
        nonlocal input_files, last_dir
        files = root.tk.splitlist(event.data)
        # Filter only files (skip folders), and Excel file types
        input_files[:] = [f for f in files if os.path.isfile(f) and f.lower().endswith(('.xls', '.xlsx', '.xlsm'))]
        if input_files:
            last_dir = os.path.dirname(input_files[0])
        update_display()

    # GUI setup
    root = tk.Tk()
    root.title("Select Files")
    root.geometry("700x500")

    # Enable drop on Windows/Linux with tkinterDnD2 if available
    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        root.destroy()
        root = TkinterDnD.Tk()
        root.title("Select Files")
        root.geometry("700x500")
        drag_and_drop_available = True
    except ImportError:
        drag_and_drop_available = False

    tk.Button(root, text="Select Input Files", width=20, command=select_inputs).pack(pady=5)
    tk.Button(root, text="Select Output File", width=20, command=select_output).pack(pady=5)

    display = tk.Text(root, height=20, width=90, state=tk.DISABLED)
    display.pack(pady=10)

    if drag_and_drop_available:
        display.drop_target_register(DND_FILES)
        display.dnd_bind('<<Drop>>', handle_drop)
        display.config(state=tk.NORMAL)
        display.insert(tk.END, "💡 Drag and drop Excel files here...\n\n")
        display.config(state=tk.DISABLED)

    tk.Button(root, text="OK", width=10, command=on_ok).pack(side=tk.LEFT, padx=40, pady=10)
    tk.Button(root, text="Cancel", width=10, command=on_cancel).pack(side=tk.RIGHT, padx=40, pady=10)

    update_display()
    root.mainloop()

