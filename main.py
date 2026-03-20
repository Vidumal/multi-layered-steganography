import customtkinter as ctk
from tkinter import filedialog, messagebox
import engine # Ensure engine.py is in the same folder

class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberSteg")
        self.geometry("600x600")
        self.selected_path = None

        self.label = ctk.CTkLabel(self, text="CyberSteg Pro", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.tabview = ctk.CTkTabview(self, width=550, height=480)
        self.tabview.pack(padx=20, pady=10)
        
        self.tab_hide = self.tabview.add("Encrypt & Hide")
        self.tab_extract = self.tabview.add("Decrypt & Extract")

        self.setup_hide_tab()
        self.setup_extract_tab()

    def setup_hide_tab(self):
        ctk.CTkButton(self.tab_hide, text="Select Image", command=self.load_image).pack(pady=10)
        self.lbl_hide = ctk.CTkLabel(self.tab_hide, text="No file selected", font=("Arial", 10))
        self.lbl_hide.pack()
        self.key_hide = ctk.CTkEntry(self.tab_hide, placeholder_text="Enter Secret Key", show="*", width=300)
        self.key_hide.pack(pady=10)
        self.msg_hide = ctk.CTkTextbox(self.tab_hide, height=150, width=400)
        self.msg_hide.insert("0.0", "")
        self.msg_hide.pack(pady=10)
        ctk.CTkButton(self.tab_hide, text="Hide & Save", fg_color="green", command=self.run_hide).pack(pady=20)

    def setup_extract_tab(self):
        ctk.CTkButton(self.tab_extract, text="Select Image", command=self.load_image).pack(pady=10)
        self.lbl_ext = ctk.CTkLabel(self.tab_extract, text="No file selected", font=("Arial", 10))
        self.lbl_ext.pack()
        self.key_ext = ctk.CTkEntry(self.tab_extract, placeholder_text="Enter Secret Key", show="*", width=300)
        self.key_ext.pack(pady=10)
        ctk.CTkButton(self.tab_extract, text="Decrypt Message", fg_color="#1f538d", command=self.run_extract).pack(pady=10)
        self.msg_ext = ctk.CTkTextbox(self.tab_extract, height=150, width=400)
        self.msg_ext.pack(pady=10)

    def load_image(self):
        # Open ANY image format for input
        path = filedialog.askopenfilename()
        if path:
            self.selected_path = path
            name = path.split('/')[-1]
            self.lbl_hide.configure(text=f"File: {name}")
            self.lbl_ext.configure(text=f"File: {name}")

    def run_hide(self):
        msg = self.msg_hide.get("0.0", "end").strip()
        key = self.key_hide.get().strip()
        if not self.selected_path or not key or not msg:
            messagebox.showerror("Error", "Missing input!")
            return
        
        # Always save as PNG
        out = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
        if out:
            try:
                engine.hide_data(self.selected_path, msg, key, out)
                messagebox.showinfo("Success", "Message hidden!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def run_extract(self):
        key = self.key_ext.get().strip()
        if not self.selected_path or not key:
            messagebox.showerror("Error", "Key/Image required!")
            return
        
        result = engine.extract_data(self.selected_path, key)
        self.msg_ext.delete("0.0", "end")
        self.msg_ext.insert("0.0", result)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = SteganoApp()
    app.mainloop()