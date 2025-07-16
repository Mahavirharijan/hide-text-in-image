from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import stepic
import os
import pathlib

def browse_file():
    file = filedialog.askopenfilename(filetypes=[
        ("All Supported Images", "*.png *.jpg *.jpeg *.bmp"),
        ("PNG Images", "*.png"),
        ("JPEG Images", "*.jpg *.jpeg"),
        ("Bitmap Images", "*.bmp")
    ])
    if file:
        file_path.set(file)
        drop_label.config(text=os.path.basename(file))
        check_inputs()

def drop_file(event):
    file = event.data.strip("{}")
    if os.path.isfile(file):
        file_path.set(file)
        drop_label.config(text=os.path.basename(file))
        check_inputs()

def check_inputs():
    if mode.get() == "hide":
        if file_path.get() and message_entry.get():
            action_btn.config(state="normal")
        else:
            action_btn.config(state="disabled")
    elif mode.get() == "extract":
        if file_path.get():
            action_btn.config(state="normal")
        else:
            action_btn.config(state="disabled")

def switch_mode():
    clear_all()
    if mode.get() == "hide":
        message_frame.pack(pady=5)
        action_btn.config(text="🔐 Hide Message")
    else:
        message_frame.forget()
        action_btn.config(text="🔓 Extract Message")
    check_inputs()

def clear_all():
    file_path.set("")
    drop_label.config(text="Drag & Drop Image Here or Click Browse")
    message_entry.delete(0, tk.END)
    action_btn.config(state="disabled")

def perform_action():
    filepath = file_path.get()
    ext = filepath.split('.')[-1].lower()

    try:
        if mode.get() == "hide":
            msg = message_entry.get()
            if ext in ['jpg', 'jpeg', 'bmp']:
                image = Image.open(filepath).convert('RGB')
            else:
                image = Image.open(filepath)

            encoded_img = stepic.encode(image, msg.encode())

            # Save output in Downloads folder
            downloads_path = str(pathlib.Path.home() / "Downloads")
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            output_file = os.path.join(downloads_path, f"{base_name}_hidden.png")
            encoded_img.save(output_file)

            messagebox.showinfo("Success", f"Message hidden in '{output_file}' successfully!")

        elif mode.get() == "extract":
            image = Image.open(filepath)
            decoded = stepic.decode(image)
            messagebox.showinfo("Hidden Message Found", decoded)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# This code id on GUI 
root = TkinterDnD.Tk()
root.title("Steganography Tool")
root.geometry("520x370")
root.config(bg="white")

try:
    root.tk.call('tkdnd::drag-and-drop', 'register', root)
except:
    pass

mode = tk.StringVar(value="hide")
file_path = tk.StringVar()

# Mode Selection
tk.Label(root, text="Select Mode:", bg="white", font=("Arial", 11)).pack(pady=5)
mode_frame = tk.Frame(root, bg="white")
mode_frame.pack()
tk.Radiobutton(mode_frame, text="Hide Message", variable=mode, value="hide", command=switch_mode, bg="white").pack(side="left", padx=10)
tk.Radiobutton(mode_frame, text="Extract Message", variable=mode, value="extract", command=switch_mode, bg="white").pack(side="left", padx=10)

# Drag-and-Drop Area + Browse
browse_frame = tk.Frame(root, bg="white")
browse_frame.pack(pady=10)

drop_label = tk.Label(browse_frame, text="Drag & Drop Image Here or Click Browse", bg="#f0f0f0", width=50, height=2, relief="groove")
drop_label.pack(pady=5)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_file)

tk.Button(browse_frame, text="Browse", command=browse_file).pack()

# Message Entry (only for hide mode)
message_frame = tk.Frame(root, bg="white")
tk.Label(message_frame, text="Enter Message to Hide:", bg="white").pack()
message_entry = tk.Entry(message_frame, width=50)
message_entry.pack()
message_entry.bind("<KeyRelease>", lambda e: check_inputs())

# Action Button
action_btn = tk.Button(root, text="🔐 Hide Message", command=perform_action, bg="lightgreen", state="disabled")
action_btn.pack(pady=15)

switch_mode()  # initialize layout
root.mainloop()
