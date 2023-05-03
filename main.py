import os
import tkinter as tk
from tkinter import filedialog

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.c_dir_button = tk.Button(self, text='Select C directory', command=self.select_c_dir)
        self.c_dir_button.pack()
        self.h_dir_button = tk.Button(self, text='Select header directory', command=self.select_h_dir)
        self.h_dir_button.pack()

    def select_c_dir(self):
        self.c_dir = filedialog.askdirectory()
        self.c_dir_button.destroy()
        self.draw_files()

    def select_h_dir(self):
        self.h_dir = filedialog.askdirectory()
        self.h_dir_button.destroy()
        self.draw_files()

    def draw_files(self):
        c_files = []
        h_files = []
        for dirpath, dirnames, filenames in os.walk(self.c_dir):
            for filename in filenames:
                if filename.endswith('.c'):
                    c_files.append(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(self.h_dir):
            for filename in filenames:
                if filename.endswith('.h'):
                    h_files.append(os.path.join(dirpath, filename))

        # Create a new Frame widget to hold the canvas and scrollbars
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Create a new Canvas widget inside the canvas frame
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create new scrollbar widgets attached to the canvas frame
        y_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Draw files
        coords = {}
        max_width = self.canvas.winfo_width() - 200
        max_height = self.canvas.winfo_height() - 200
        bbox_widths = []
        bbox_heights = []
        for i, c_file in enumerate(c_files):
            bbox = self.canvas.bbox(self.canvas.create_text(0, 0, text=c_file))
            bbox_widths.append(bbox[2] - bbox[0])
            bbox_heights.append(bbox[3] - bbox[1])
        bbox_width = max(bbox_widths)
        bbox_height = max(bbox_heights)
        grid_width = max_width // bbox_width
        grid_height = max_height // bbox_height
        for i, c_file in enumerate(c_files):
            row = i // grid_width
            col = i % grid_width
            x = col * bbox_width + 100
            y = row * bbox_height + 100
            coords[c_file] = (x, y)
            self.canvas.create_rectangle(x - bbox_width/2, y - bbox_height/2, x + bbox_width/2, y + bbox_height/2, fill='lightblue')
            self.canvas.create_text(x, y, text=c_file)

        for i, h_file in enumerate(h_files):
            row = (i + len(c_files)) // grid_width
            col = (i + len(c_files)) % grid_width
            x = col * bbox_width + 100
            y = row * bbox_height + 100
            coords[h_file] = (x, y)
            self.canvas.create_rectangle(x - bbox_width/2, y - bbox_height/2, x + bbox_width/2, y + bbox_height/2, fill='lightgreen')
            self.canvas.create_text(x, y, text=h_file)

        for c_file in c_files:
            with open(c_file, 'r') as f:
                contents = f.read()
                for h_file in h_files:
                    if h_file in contents:
                        start = coords[c_file]
                        end = coords[h_file]
                        self.canvas.create_line(start[0], start[1], end[0], end[1])

        # Set the scrollable region of the canvas to the size of the files
        # Set the scrollable region of the canvas to the size of the files
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create a vertical scrollbar that will scroll the canvas
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind the canvas to handle resizing
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the files
        file_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=file_frame, anchor="nw")

        # Add the files to the frame
        for i, file in enumerate(files):
            file_label = tk.Label(file_frame, text=file)
            file_label.pack(pady=10, padx=20)



    def get_relationships(self, c_files):
        relationships = {}
        for c_file in c_files:
            relationships[c_file] = self.check_h_files(c_file)
        return relationships

    def check_h_files(self, c_file):
        with open(c_file, 'r') as f:
            lines = f.readlines()

        h_files = []
        for line in lines:
            if line.startswith('#include'):
                h_file = line.split()[1]
                h_files.append(h_file.strip('"\n'))

        return h_files

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = App(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()

