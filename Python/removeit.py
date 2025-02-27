import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove

class BackgroundRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("800x600")
        
        # Create frames
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)
        
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(pady=10)
        
        # Buttons
        tk.Button(self.top_frame, text="Select Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.top_frame, text="Remove Background", command=self.remove_background).pack(side=tk.LEFT, padx=5)
        tk.Button(self.top_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Image labels
        self.original_label = tk.Label(self.image_frame, text="No image selected")
        self.original_label.pack(side=tk.LEFT, padx=10)
        
        self.result_label = tk.Label(self.image_frame, text="Result will appear here")
        self.result_label.pack(side=tk.LEFT, padx=10)
        
        self.original_image = None
        self.result_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")
        ])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                # Resize for display
                display_image = self.original_image.copy()
                display_image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(display_image)
                self.original_label.config(image=photo)
                self.original_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def remove_background(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
            
        try:
            self.result_image = remove(self.original_image)
            # Resize for display
            display_image = self.result_image.copy()
            display_image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(display_image)
            self.result_label.config(image=photo)
            self.result_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove background: {str(e)}")

    def save_image(self):
        if self.result_image is None:
            messagebox.showwarning("Warning", "No processed image to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            try:
                self.result_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemover(root)
    root.mainloop()