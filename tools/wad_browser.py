import tkinter as tk
from tkinter import ttk

from formats.wad import WadHeader

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

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
        self.file.menu['tearoff'] = 0
        self.file['menu'] = self.file.menu

        self.file.menu.add_command(label='Open .wad', command=self.open_wad)

        self.tree_view = ttk.Treeview(self)
        self.tree_view['columns'] = ['size']
        self.tree_view.heading('size', text='Size')
        self.tree_view.bind('<<TreeviewSelect>>', self.on_tree_item_select)
        self.tree_view.pack(side='left', expand=True, fill='both')

        self.file_view = ttk.Frame(self)
        self.file_view.pack(side='right', fill='both', expand=True)

        self.hex_view = tk.Text(self.file_view)
        self.hex_view['bg'] = '#fff'

        self.hex_view.pack(side='left', expand=True, fill='both')

    def open_wad(self):
        # open a popup dialog
        import tkinter.filedialog as filedialog
        path = filedialog.askopenfilename(filetypes=[('.wad', '*.wad')])

        # load .wad header
        self.wad = open(path, 'rb')
        self.wad_header = WadHeader(self.wad)

        # build file path to metadata mapping
        self.files = {}
        for file in self.wad_header.files:
            self.files[file['path']] = (file['offset'], file['size'])

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
            if subpath in self.files:
                self.tree_view.item(subpath, values=[sizeof_fmt(self.files[subpath][1])])
            if subfile['is_directory']:
                self.populate_tree(subfiles, subpath)

    def on_tree_item_select(self, event):
        self.hex_view.delete('1.0', 'end')

        path = self.tree_view.focus()
        if path not in self.files: return

        # display an hex view
        offset = self.wad_header.header_size + self.files[path][0]
        size = self.files[path][1]

        self.view_base_offset = offset
        self.view_offset = 0
        self.view_size = size

        self.update_hex_view()

    def update_hex_view(self):
        import string

        ROWS = 64
        COLUMNS = 16
        byte_count = min(ROWS*COLUMNS, self.view_size - self.view_offset)

        self.wad.seek(self.view_base_offset + self.view_offset)
        data = self.wad.read(ROWS*COLUMNS)

        for r in range(ROWS):
            # write offset
            self.hex_view.insert('end', '{:04x} | '.format(self.view_offset + r*16))
            # write bytes
            for c in range(COLUMNS):
                self.hex_view.insert('end', '{:02x} '.format(data[r*16 + c]))
            self.hex_view.insert('end', '   ')
            # write ascii
            for c in range(COLUMNS):
                byte = chr(data[r*16 + c])
                if byte in string.printable and (byte not in string.whitespace or byte == ' '):
                    self.hex_view.insert('end', byte)
                else:
                    self.hex_view.insert('end', '.')
            self.hex_view.insert('end', '\n')

root = tk.Tk()
app = Application(root)
app.mainloop()
