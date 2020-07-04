import tkinter as tk
from tkinter import ttk

from formats.wad import WadHeader

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.title('.wad browser')
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.top = tk.Frame(self)
        self.top.pack(fill='x')
            
        self.file = tk.Menubutton(self.top, text='File')
        self.file.pack(anchor='nw')
        self.file.menu = tk.Menu(self.file)
        self.file['menu'] = self.file.menu

        self.file.menu.add_command(label='Open .wad', command=self.open_wad)

        self.tree_view = ttk.Treeview(self)
        self.tree_view.pack(side='left', expand=True, fill='both')

    def open_wad(self):
        # open a popup dialog
        import tkinter.filedialog as filedialog
        path = filedialog.askopenfilename(filetypes=[('.wad', '*.wad')])

        # load .wad header
        self.file = open(path, 'rb')
        self.wad_header = WadHeader(self.file)

        # build directory path to subfiles mapping
        subfiles = {}
        for dir in self.wad_header.dirs:
            subfiles[dir['path']] = dir['subfiles']

        # clear current tree
        self.tree_view.delete(*self.tree_view.get_children())

        # populate tree view with directory structure
        self.populate_tree(subfiles, '')

    def populate_tree(self, subfiles, path):
        for subfile in subfiles[path]:
            subpath = path + ('/' if path else '') + subfile['name']
            self.tree_view.insert(path, 'end', iid=subpath, text=subfile['name'])
            if subfile['is_directory']:
                self.populate_tree(subfiles, subpath)


root = tk.Tk()
app = Application(root)
app.mainloop()
