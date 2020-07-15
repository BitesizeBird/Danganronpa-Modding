import tkinter as tk
from tkinter import ttk

from formats.wad import Wad
from formats.pak import PakHeader
from formats.tga import read_tga

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
            
        self.file_mb = tk.Menubutton(self.top, text='File', bg='#fff')
        self.file_mb.pack(anchor='nw')
        self.file_mb.menu = tk.Menu(self.file_mb)
        self.file_mb.menu['tearoff'] = 0
        self.file_mb['menu'] = self.file_mb.menu

        self.file_mb.menu.add_command(label='Open .wad', command=self.open_wad)

        self.wad_tree_top = ttk.Frame(self)
        self.wad_tree_top.pack(side='left', expand=True, fill='both')

        self.wad_tree = ttk.Treeview(self.wad_tree_top)
        self.wad_tree['columns'] = ['size']
        self.wad_tree.heading('size', text='Size')
        self.wad_tree.bind('<<TreeviewSelect>>', self.on_wad_tree_select)
        self.wad_tree.pack(side='left', expand=True, fill='both')

        self.wad_tree.menu = tk.Menu(self.wad_tree, bg='#fff')
        self.wad_tree.menu['tearoff'] = 0
        self.wad_tree.bind('<Button-3>', self.on_wad_tree_right_click)

        self.wad_tree.menu.add_command(label='Decode as .pak', command=self.decode_as_pak)

        self.wad_tree_vsb = ttk.Scrollbar(self.wad_tree_top, orient='vertical', command=self.wad_tree.yview)
        self.wad_tree_vsb.pack(side='right', fill='y')
        self.wad_tree.configure(yscrollcommand=self.wad_tree_vsb.set)

        self.file_view = ttk.Notebook(self)
        self.file_view.pack(side='right', fill='both', expand=True)

        self.file_hex_top = ttk.Frame(self.file_view)
        self.file_hex_top.pack(fill='both', expand=True)
        self.file_view.add(self.file_hex_top, text='Hex')

        self.file_hex_view = tk.Text(self.file_hex_top, bg='#fff')
        self.file_hex_view.pack(side='left', expand=True, fill='both')

        self.file_tga_top = ttk.Frame(self.file_view)
        self.file_tga_top.pack(fill='both', expand=True)
        self.file_view.add(self.file_tga_top, text='TGA') 

        self.file_tga_view = tk.Canvas(self.file_tga_top)

        self.file_tga_hsb = tk.Scrollbar(self.file_tga_top, orient='horizontal', command=self.file_tga_view.xview)
        self.file_tga_hsb.pack(side='bottom', fill='x')

        self.file_tga_vsb = tk.Scrollbar(self.file_tga_top, orient='vertical', command=self.file_tga_view.yview)
        self.file_tga_vsb.pack(side='right', fill='y')

        self.file_tga_view.configure(yscrollcommand=self.file_tga_vsb.set, xscrollcommand=self.file_tga_hsb.set)
        self.file_tga_view.pack(side='left', expand=True, fill='both')

    def on_wad_tree_right_click(self, event):
        path = self.wad_tree.identify_row(event.y)
        if path:
            self.wad_tree.selection_set(path)
            self.wad_tree.focus(path)

            self.wad_tree.menu.entryconfigure(0, state = 'normal' if path in self.files else tk.DISABLED)

            self.wad_tree.menu.tk_popup(event.x_root, event.y_root, 0)

    def open_wad(self, path=None):
        if path is None:
            # open a popup dialog
            import tkinter.filedialog as filedialog
            path = filedialog.askopenfilename(filetypes=[('.wad', '*.wad')])

        # load .wad header
        self.wad = Wad(path)
        self.files = self.wad.files.copy()

        # clear current tree
        self.wad_tree.delete(*self.wad_tree.get_children())

        # populate tree view with directory structure
        self.populate_tree(self.wad.subfiles, '')

    def populate_tree(self, subfiles, path):
        for subfile in subfiles[path]:
            subpath = path + ('/' if path else '') + subfile['name']
            self.wad_tree.insert(path, 'end', iid=subpath, text=subfile['name'])
            if subpath in self.files:
                self.wad_tree.item(subpath, values=[sizeof_fmt(self.files[subpath][1])])
            if subfile['is_directory']:
                self.populate_tree(subfiles, subpath)

    def decode_as_pak(self):
        path = self.wad_tree.focus()
        if path not in self.files: return

        try:
            pak_header = PakHeader(self.wad.file, self.file_offset)
            offsets = pak_header.offsets + [self.file_size]

            for i, offset in enumerate(pak_header.offsets):
                iid = '{}:{}'.format(path, offset)
                self.wad_tree.insert(path, 'end', iid=iid, text='{:02}'.format(i))
                self.files[iid] = [
                        pak_header.base_offset + offset,
                        offsets[i+1] - offsets[i]]
                self.wad_tree.item(iid, values=[sizeof_fmt(offsets[i+1] - offsets[i])])
        except ValueError:
            pass

    def on_wad_tree_select(self, event):
        self.file_hex_view.delete('1.0', 'end')
        self.file_tga_view.delete('all')

        path = self.wad_tree.focus()
        if path not in self.files: return

        # display an hex view
        self.file_offset = self.files[path][0]
        self.file_size = self.files[path][1]

        self.hex_view_offset = 0

        self.update_hex_view()

        # try to parse it as tga
        try:
            import png
            import io
            from PIL import Image, ImageTk

            color_map, pixel_data = read_tga(self.wad.file, self.file_offset)
            data = io.BytesIO()
            w = png.Writer(len(pixel_data[0]), len(pixel_data), palette=color_map)
            w.write(data, pixel_data)

            self.tga_view_image = ImageTk.PhotoImage(Image.open(data))

            self.file_tga_view.create_image(0, 0, image=self.tga_view_image, anchor=tk.NW)
            self.file_tga_view.configure(scrollregion=self.file_tga_view.bbox('all'))
        except:
            pass

    def update_hex_view(self):
        import string

        ROWS = 128
        COLUMNS = 16
        byte_count = min(ROWS*COLUMNS, self.file_size - self.hex_view_offset)

        self.wad.file.seek(self.file_offset + self.hex_view_offset)
        data = self.wad.file.read(byte_count)

        for r in range(ROWS):
            if r*16 >= byte_count: break

            # write offset
            self.file_hex_view.insert('end', '{:04x} | '.format(self.hex_view_offset + r*16))
            # write bytes
            for c in range(COLUMNS):
                if r*16 + c < byte_count:
                    self.file_hex_view.insert('end', '{:02x} '.format(data[r*16 + c]))
                else:
                    self.file_hex_view.insert('end', '   ')
            self.file_hex_view.insert('end', '   ')
            # write ascii
            for c in range(COLUMNS):
                if r*16 + c < byte_count:
                    byte = chr(data[r*16 + c])
                    if byte in string.printable and (byte not in string.whitespace or byte == ' '):
                        self.file_hex_view.insert('end', byte)
                    else:
                        self.file_hex_view.insert('end', '.')
                else:
                    self.file_hex_view.insert('end', ' ')
            self.file_hex_view.insert('end', '\n')

root = tk.Tk()
app = Application(root)

import sys
if len(sys.argv) > 1:
    app.open_wad(sys.argv[1])

app.mainloop()
