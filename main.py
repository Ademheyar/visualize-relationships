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
        self.main_dir_button = tk.Button(self, text='Select main directory', command=self.select_main_dir)
        self.main_dir_button.pack()

    def select_main_dir(self):
        self.main_dir = filedialog.askdirectory()
        self.main_dir_button.destroy()
        self.draw_files()

    def draw_files(self):
        os.chdir(self.main_dir)

        c_files = [f for f in os.listdir('.') if f.endswith('.c')]
        h_files = [f for f in os.listdir('.') if f.endswith('.h')]

        # Draw .c files
        c_coords = {}
        for i, c_file in enumerate(c_files):
            x = self.canvas.winfo_width() / (len(c_files) + 1) * (i + 1)
            y = self.canvas.winfo_height() * 0.25
            c_coords[c_file] = (x, y)
            self.canvas.create_rectangle(x - 50, y - 25, x + 50, y + 25, fill='lightblue')
            self.canvas.create_text(x, y, text=c_file)

        # Draw .h files
        h_coords = {}
        for i, h_file in enumerate(h_files):
            x = self.canvas.winfo_width() / (len(h_files) + 1) * (i + 1)
            y = self.canvas.winfo_height() * 0.75
            h_coords[h_file] = (x, y)
            self.canvas.create_rectangle(x - 50, y - 25, x + 50, y + 25, fill='lightgreen')
            self.canvas.create_text(x, y, text=h_file)

        # Draw connections between .c and .h files
        for c_file, h_files in self.get_relationships(c_files).items():
            for h_file in h_files:
                self.canvas.create_line(c_coords[c_file], h_coords[h_file], fill='gray')

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
