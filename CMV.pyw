import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import networkx as nx
from tkinter import messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile, base64, zlib

# Console output at startup
print("Correlation Matrix Visualizer v. 1.0\n2025 © Data Animal")

# Global variables
global column_labels, data_labels, pddata, col_names

# Transparent icon settings
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
                                        'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

# Load CSV file
def load_file():
    global pddata, col_names, column_labels, data_labels
    try:
        filepath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if filepath:
            pddata = pd.read_csv(filepath)
            col_names = list(pddata.columns)
            datacolumns['values'] = col_names
            datacolumns2['values'] = col_names
            column_labels = []
            data_labels = []

            canvas = tk.Canvas(root)
            scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar_x.set)

            canvas.place(x=0, y=0, width=root.winfo_width(), height=270)
            scrollbar_x.place(x=0, y=270, width=root.winfo_width())

            frame_grid = tk.Frame(canvas)
            canvas.create_window((0, 0), window=frame_grid, anchor=tk.NW)

            col_name_frame = tk.Frame(frame_grid)
            col_name_frame.grid(row=2, columnspan=len(col_names))
            for i, col_name in enumerate(col_names):
                label = tk.Label(col_name_frame, text=col_name)
                label.grid(row=0, column=i, padx=40)
                column_labels.append(label)

            tk.Label(frame_grid).grid(row=3)

            for i in range(min(10, len(pddata))):
                row_labels = []
                for j, col_name in enumerate(col_names):
                    try:
                        text = pddata.iloc[i, j]
                    except IndexError:
                        text = ""
                    label = tk.Label(frame_grid, text=text)
                    label.grid(row=i + 4, column=j, padx=10)
                    row_labels.append(label)
                data_labels.append(row_labels)

            frame_grid.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            datacolumns.current(0)
            datacolumns2.current(0)
            return pddata
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the file: {e}")
        return None

# Update data labels
def update_display():
    global column_labels, data_labels, pddata, col_names

    if pddata is not None:
        col_names = list(pddata.columns)

        for i, col_name in enumerate(col_names):
            if i < len(column_labels):
                column_labels[i].config(text=col_name)

        for i in range(min(10, len(pddata))):
            if i < len(data_labels):
                for j, col_name in enumerate(col_names):
                    if j < len(data_labels[i]):
                        try:
                            text = pddata.iloc[i, j]
                        except IndexError:
                            text = ""
                        data_labels[i][j].config(text=text)

# Next 5 functions fetch data for Generate_heatmap()
def getCbar():
    if (z.get()):
        return True
    else:
        return False

def getAnnot():
    if (x.get()):
        return True
    else:
        return False

def getlnSize():
    lnsize_index = lnsize.current()
    if lnsize_index == 1:
        return .2
    elif lnsize_index == 2:
        return .8
    else:
        return .5

def getCmap():
    cmap_index = hmtypes.current()
    if cmap_index == 1:
        return "Greens"
    elif cmap_index == 2:
        return "Oranges"
    elif cmap_index == 3:
        return "Reds"
    elif cmap_index == 4:
        return "Purples"
    else:
        return "coolwarm"

def getBzise():
    bsize_index = hmsize.current()
    if bsize_index == 1:
        return (6, 4)
    elif bsize_index == 2:
        return (10, 8)
    else:
        return (8, 6)

# Generate heatmap from CSV data
def Generate_heatmap():
    global pddata
    if 'pddata' in globals():
        try:

            if heatmaptitle.get() == "":
                heatmapTitle = "Correlation matrix heatmap"
            else:
                heatmapTitle = heatmaptitle.get()

            correlation_matrix = pddata.corr()
            plt.figure(figsize=getBzise())
            sns.heatmap(correlation_matrix, annot=getAnnot(), cmap=getCmap(), fmt=".2f", linewidths=getlnSize(), cbar=getCbar())
            plt.title(heatmapTitle)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate heatmap: {e}")
    else:
        messagebox.showinfo("Error", "Please load a CSV file first.")

# Fetch data for Generate_network()
def getLabels():
    if (e.get()):
        return True
    else:
        return False

# Generate network diagram from CSV data
def Generate_network():
    global pddata
    if 'pddata' in globals():
        try:
            corr = pddata.corr()
            graph = nx.Graph()
            graph.add_nodes_from(corr.columns)

            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):
                    if abs(corr.iloc[i, j]) > 0.5:
                        graph.add_edge(corr.columns[i], corr.columns[j], weight=corr.iloc[i, j])

            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=getLabels(), node_size=scale1.get(), node_color=colortypes.get(), font_size=scale2.get(),
                    font_color="black")
            edge_labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate network diagram: {e}")

    else:
        messagebox.showinfo("Error", "Please load a CSV file first.")

# Next 2 functions fetch data for Generate_scatterplot()
def getHue():
    selection_index = datacolumns.current()
    if selection_index != -1:
        column_name = col_names[selection_index]
        return column_name
    else:
        return None

def getKind():
    kind_index = scatterplottype.current()
    if kind_index == 1:
        return "kde"
    elif kind_index == 2:
        return "reg"
    else:
        return "scatter"

# Generate scatter plot matrix from CSV data
def Generate_scatterplot():
    global pddata
    if 'pddata' in globals():
        try:
            corr = pddata.corr()
            if (u.get()) and getKind() != "kde":
                sns.pairplot(pddata, hue=getHue(), kind=getKind())
            elif (u.get()) and getKind() == "kde":
                messagebox.showerror("Error", "Cannot use kde with variable coloring")
                return
            else:
                sns.pairplot(pddata, kind=getKind())
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate scatter plot matrix: {e}")

    else:
        messagebox.showinfo("Error", "Please load a CSV file first.")

# Remove the selected column
def drop_column():
    global pddata, column_labels, data_labels, col_names
    if pddata is not None:
        try:
            selection_index = datacolumns2.current()
            if selection_index != -1:
                column_name = pddata.columns[selection_index]
                pddata = pddata.drop([column_name], axis=1)

                col_names = list(pddata.columns)
                datacolumns['values'] = col_names
                datacolumns2['values'] = col_names

                column_labels[selection_index].grid_forget()
                del column_labels[selection_index]

                for row_labels in data_labels:
                    row_labels[selection_index].grid_forget()
                    del row_labels[selection_index]

                datacolumns.current(0)
                datacolumns2.current(0)
                update_display()
            else:
                messagebox.showwarning("Warning", "No column selected.")
        except Exception as e:
            messagebox.showerror("Error", f"Error dropping column: {e}")
    else:
        messagebox.showinfo("Error", "Please load a CSV file first.")

# Update display
def display():
    if (u.get()):
        label_datacolumns.config(state='normal')
        datacolumns.config(state='readonly')
    else:
        label_datacolumns.config(state='disabled')
        datacolumns.config(state='disabled')

# Exit program
def close():
    root.destroy()

# Window settings
root = tk.Tk()
root.title("Correlation Matrix Visualizer")
root.geometry("850x700")
root.iconbitmap(default=ICON_PATH)
root.resizable(False, False)

# Menubar settings
menubar = tk.Menu(root)
root.config(menu = menubar)
filemenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="Open", command=load_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close)

# Widget settings - heatmap
heatmaplabel = tk.Label(text="Heatmap", font=('Arial', 20))
heatmapbtn = tk.Button(text="Generate Heatmap", command=Generate_heatmap)
colorpalette = tk.Label(text="Heatmap color palette")
hmtypes = ttk.Combobox(state="readonly", width=9, values=["coolwarm", "Greens", "Oranges", "Reds", "Purples"])
hmtypes.current(0)
x = tk.BooleanVar()
x.set(1)
annotswitch = tk.Checkbutton(text="Write the data value in each cell", variable=x, onvalue=True, offvalue=False)
z = tk.BooleanVar()
z.set(1)
cbarswitch = tk.Checkbutton(text="Colorbar", variable=z, onvalue=True, offvalue=False)
heatmaptitlelb = tk.Label(text="Heatmap title:")
heatmapsize = tk.Label(text="Heatmap block size:")
linesize = tk.Label(text="Width of the lines that divide cells:")
lnsize = ttk.Combobox(state="readonly", width=8, values=["Normal", "Wider", "Widest"])
lnsize.current(0)
hmsize = ttk.Combobox(state="readonly", width=8, values=["Normal", "Small", "Large"])
hmsize.current(0)
heatmaptitle = tk.Entry()

# Widget settings - network diagram
networklabel = tk.Label(text="Network Diagram", font=('Arial', 20))
nodecolor = tk.Label(text="Node color")
colortypes = ttk.Combobox(state="readonly", width=9, values=["Skyblue", "Blue", "Green", "Orange", "Red", "Purple"])
colortypes.current(0)
e = tk.BooleanVar()
e.set(1)
labelswitch = tk.Checkbutton(text="Add labels", variable=e, onvalue=True, offvalue=False)
networkbtn = tk.Button(text="Generate Network Diagram", command=Generate_network)
scalelabel = tk.Label(text="Node size:")
scale1 = tk.Scale(from_=500, to=3000, length=100, orient='horizontal', font=("Arial",8), tickinterval = 1000)
scale1.set(1500)
fontlabel = tk.Label(text="Font size:")
scale2 = tk.Scale(from_=5, to=30, length=100, orient='horizontal', font=("Arial",8), tickinterval = 5)
scale2.set(10)

# Widget settings - scatter plot matrix
scatterplotlabel = tk.Label(text="Scatter Plot Matrix", font=('Arial', 20))
u = tk.BooleanVar()
u.set(0)
scatterswitch = tk.Checkbutton(text="Color the points based on the variable", variable=u, onvalue=True, offvalue=False, command=display)
scatterplotbtn = tk.Button(text="Generate Scatter Plot Matrix", command=Generate_scatterplot)
label_datacolumns = tk.Label(text="The column based on which the points are colored:", state="disabled")
datacolumns = ttk.Combobox(state="disabled")
scatterplottypelabel = tk.Label(text="Type:")
scatterplottype = ttk.Combobox(state="readonly", width=6, values=["scatter", "kde", "reg"])
scatterplottype.current(0)

# Widget settings - column drops
droplabel = tk.Label(text="Select column(s) to be dropped:", font=('Arial', 15))
datacolumns2 = ttk.Combobox(state="readonly")
dropcolumn = tk.Button(text="Drop", command=drop_column)

# Widget placements - heatmap
heatmaplabel.place(x=30, y=300)
heatmaptitlelb.place(x=30, y=350)
heatmaptitle.place(x=30, y=375)
colorpalette.place(x=30, y=405)
hmtypes.place(x=30, y=430)
heatmapsize.place(x=30, y=460)
hmsize.place(x=30, y=485)
linesize.place(x=30, y=520)
lnsize.place(x=30, y=545)
annotswitch.place(x=30, y=570)
cbarswitch.place(x=30, y=590)
heatmapbtn.place(x=30, y=640)

# Widget placements - network diagram
networklabel.place(x=280, y=300)
nodecolor.place(x=280, y=350)
colortypes.place(x=280, y=375)
scalelabel.place(x=280, y=410)
scale1.place(x=280, y=430)
fontlabel.place(x=280, y=490)
scale2.place(x=280, y=510)
labelswitch.place(x=280, y=570)
networkbtn.place(x=280, y=640)

# Widget placements - scatter plot matrix
scatterplotlabel.place(x=530, y=300)
scatterswitch.place(x=530, y=350)
label_datacolumns.place(x=530, y=375)
datacolumns.place(x=530, y=400)
scatterplottypelabel.place(x=530, y=430)
scatterplottype.place(x=530, y=455)
scatterplotbtn.place(x=530, y=500)

# Widget placements - drop columns
droplabel.place(x=530, y=600)
datacolumns2.place(x=530, y=645)
dropcolumn.place(x=690, y=640)

if __name__ == '__main__':
    root.mainloop()