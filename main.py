import customtkinter as ctk
from tkinter import filedialog, messagebox
from engine import hide_data  # Ensure engine.py is in the same folder

class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberSteg - Multi-Layered Hidden Data")
        self.geometry("600x500")
        
        self.selected_path = None  # To store the image path

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Multi-Layered Image Steganography", font=("Arial", 22, "bold"))
        self.label.pack(pady=20)

        self.btn_browse = ctk.CTkButton(self, text="1. Select Base Image", command=self.load_image)
        self.btn_browse.pack(pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="No file selected", font=("Arial", 10), text_color="gray")
        self.path_label.pack()

        self.key_entry = ctk.CTkEntry(self, placeholder_text="Enter Secret Key (Layer 1 & 2)", show="*")
        self.key_entry.pack(pady=10, fill="x", padx=50)

        self.msg_entry = ctk.CTkTextbox(self, height=100)
        self.msg_entry.insert("0.0", "Enter your secret message here...")
        self.msg_entry.pack(pady=10, fill="x", padx=50)

        self.btn_hide = ctk.CTkButton(self, text="2. Encrypt & Hide", fg_color="green", command=self.run_protection)
        self.btn_hide.pack(pady=20)

    def load_image(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.bmp")])
        if self.selected_path:
            self.path_label.configure(text=f"Selected: {self.selected_path.split('/')[-1]}")

    def run_protection(self):
        # Validation
        message = self.msg_entry.get("0.0", "end").strip()
        key = self.key_entry.get()
        
        if not self.selected_path or not key or not message:
            messagebox.showerror("Error", "Please provide an image, a key, and a message!")
            return

        # Save Location
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
        
        if output_path:
            try:
                # Calling your engine.py function
                success = hide_data(self.selected_path, message, key, output_path)
                if success:
                    messagebox.showinfo("Success", f"Data hidden securely in:\n{output_path}")
            except Exception as e:
                messagebox.showerror("System Error", f"An error occurred: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = SteganoApp()
    app.mainloop()