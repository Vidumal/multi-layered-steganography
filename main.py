import customtkinter as ctk
from tkinter import filedialog

class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberSteg - Multi-Layered Hidden Data")
        self.geometry("600x400")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Multi-Layered Image Steganography", font=("Arial", 20))
        self.label.pack(pady=20)

        self.btn_browse = ctk.CTkButton(self, text="Select Image", command=self.load_image)
        self.btn_browse.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, placeholder_text="Enter Secret Key", show="*")
        self.key_entry.pack(pady=10, fill="x", padx=50)

        self.msg_entry = ctk.CTkTextbox(self, height=100)
        self.msg_entry.pack(pady=10, fill="x", padx=50)

        self.btn_hide = ctk.CTkButton(self, text="Encrypt & Hide", fg_color="green")
        self.btn_hide.pack(pady=20)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        print(f"Selected: {file_path}")

if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()