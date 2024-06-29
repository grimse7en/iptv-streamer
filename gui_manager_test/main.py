import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 4x4 Grid Frame
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.grid(row=0, column=0, sticky="nsew")
        
        for i in range(4):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)
        
        # Populate the 4x4 grid
        self.images = []  # To keep references to the images
        self.image_labels = []  # To keep references to image labels
        for row in range(4):
            for col in range(4):
                cell_frame = ttk.Frame(self.grid_frame, borderwidth=1, relief="solid")
                cell_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                
                # Inner frame to organize number and image
                inner_frame = ttk.Frame(cell_frame)
                inner_frame.pack(fill="both", expand=True)

                number_label = tk.Label(inner_frame, text=f"{row*4+col+1}", anchor="w",
                                        highlightbackground="blue", highlightcolor="blue", highlightthickness=2, font=("Helvetica", 170, "bold"))
                number_label.pack(side="left")

                image_label = tk.Label(inner_frame, anchor="e",
                                       highlightbackground="yellow", highlightcolor="yellow", highlightthickness=2)
                image_label.pack(side="left", expand=True, fill="both")
                self.image_labels.append(image_label)
        
        for index, image_label in enumerate(self.image_labels):
            image_label.update_idletasks()  # Ensure the label is fully rendered
            width = image_label.winfo_width()
            height = image_label.winfo_height()
            print(f"Image Label {index + 1} size: {width}x{height}")
            # Image loading
            image = Image.open("img/1.png")  # replace with your image path
            image.thumbnail((50, 50), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)
            image_label.config(image=image_tk)
            self.images.append(image_tk)
        
        # Number window
        self.number_window = ttk.Frame(self.root, width=self.screen_width//10, height=self.screen_width//10, borderwidth=2, relief="solid")
        self.number_label = ttk.Label(self.number_window, text="00", font=("Arial", 24))
        self.number_label.pack(expand=True, fill="both")

        # Loading window
        self.loading_window = ttk.Frame(self.root, width=self.screen_width//4, height=self.screen_height//10, borderwidth=2, relief="solid")
        self.loading_label = ttk.Label(self.loading_window, text="Loading...", font=("Arial", 24))
        self.loading_label.pack(expand=True, fill="both")

        # Channel info window
        self.channel_info_window = ttk.Frame(self.root, width=self.screen_width//4, height=self.screen_height//20, borderwidth=2, relief="solid")
        self.channel_info_label = ttk.Label(self.channel_info_window, text="Channel Info", font=("Arial", 24))
        self.channel_info_label.pack(expand=True, fill="both")

        #self.root.after(1000, self.print_image_label_sizes)  # Print sizes after 1 second delay

    def show_number_window(self):
        self.number_window.place(x=0, y=0)

    def hide_number_window(self):
        self.number_window.place_forget()

    def show_loading_window(self):
        self.loading_window.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def hide_loading_window(self):
        self.loading_window.place_forget()

    def show_channel_info_window(self):
        self.channel_info_window.place(relx=0.5, y=0)

    def hide_channel_info_window(self):
        self.channel_info_window.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUIManager(root)
    gui.show_number_window()
    gui.show_loading_window()
    gui.show_channel_info_window()
    root.mainloop()
