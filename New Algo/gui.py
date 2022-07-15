import random
from doctest import master
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from Main import Call_Main
import Main
import platform
import time
from tkinter import *
from PIL import ImageTk, Image

col = ["white", "#9A8C98", "light grey", "white"]
font = {'font': ("lato bold", 10, "")}

G = nx.Graph()
height = 0
width = 0


class MainApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        global height
        global width
        height = self.root.winfo_screenheight()
        width = self.root.winfo_screenwidth()
        self.root.attributes('-fullscreen', True)
        self.draw_board_frame = tk.Frame(self.root)
        self.draw_board_frame.grid()
        draw_board = PlotApp(self.draw_board_frame, self)

        self.run_app()

    def run_app(self):
        self.root.mainloop()

    class Nodes:
        def __init__(self, id, x, y):
            self.circle_id = id
            self.pos_x = x
            self.pos_y = y
            self.radius = 15
            self.adj_list = []

        def clear(self):
            self.circle_id = -1
            self.pos_x = 0
            self.pos_y = 0
            self.radius = 0
            self.adj_list = []


class PlotApp:

    def __init__(self, toframe, master):
        root = tk.Frame(toframe)
        root.grid(row=0, column=0)
        self.root = root
        self.l1 = tk.Label(root, text='Draw a test graph here', bg=col[2])
        self.l1.grid(row=0, column=0)
        self._root = root
        self.radius_circle = 15
        self.rnames = []
        self.master = master
        self.command = "Null"
        self.createCanvas()
        self.nodes_data = []

    colors = [
        '#F44336',
        '#FFEBEE',
        '#FFCDD2',
        '#EF9A9A',
        '#E57373',
        '#EF5350',
        '#E53935',
        '#D32F2F',
        '#C62828',
        '#B71C1C',
        '#FF8A80',
        '#FF5252',
        '#FF1744',
        '#D50000',
        '#FCE4EC',
        '#F8BBD0',
        '#F48FB1',
        '#F06292',
        '#EC407A',
        '#E91E63',
        '#D81B60',
        '#C2185B',
        '#AD1457',
        '#880E4F',
        '#FF80AB',
        '#FF4081',
        '#F50057',
        '#C51162',
        '#F3E5F5',
        '#E1BEE7',
        '#CE93D8',
        '#BA68C8',
        '#AB47BC',
        '#9C27B0',
        '#8E24AA',
        '#7B1FA2',
        '#6A1B9A',
        '#4A148C',
        '#EA80FC',
        '#E040FB',
        '#D500F9',
        '#AA00FF',
        '#EDE7F6',
        '#D1C4E9',
        '#B39DDB',
        '#9575CD',
        '#7E57C2',
        '#673AB7',
        '#5E35B1',
        '#512DA8',
        '#4527A0',
        '#311B92',
        '#B388FF',
        '#7C4DFF',
        '#651FFF',
        '#6200EA',
        '#E8EAF6',
        '#C5CAE9',
        '#9FA8DA',
        '#7986CB',
        '#5C6BC0',
        '#3F51B5',
        '#3949AB',
        '#303F9F',
        '#283593',
        '#1A237E',
        '#8C9EFF',
        '#536DFE',
        '#3D5AFE',
        '#304FFE',
        '#E3F2FD',
        '#BBDEFB',
        '#90CAF9',
        '#64B5F6',
        '#42A5F5',
        '#2196F3',
        '#1E88E5',
        '#1976D2',
        '#1565C0',
        '#0D47A1',
        '#82B1FF',
        '#448AFF',
        '#2979FF',
        '#2962FF',
        '#E1F5FE',
        '#B3E5FC',
        '#81D4FA',
        '#4FC3F7',
        '#29B6F6',
        '#03A9F4',
        '#039BE5',
        '#0288D1',
        '#0277BD',
        '#01579B',
        '#80D8FF',
        '#40C4FF',
        '#00B0FF',
        '#0091EA',
        '#E0F7FA',
        '#B2EBF2',
        '#80DEEA',
        '#4DD0E1',
        '#26C6DA',
        '#00BCD4',
        '#00ACC1',
        '#0097A7',
        '#00838F',
        '#006064',
        '#84FFFF',
        '#18FFFF',
        '#00E5FF',
        '#00B8D4',
        '#E0F2F1',
        '#B2DFDB',
        '#80CBC4',
        '#4DB6AC',
        '#26A69A',
        '#009688',
        '#00897B',
        '#00796B',
        '#00695C',
        '#004D40',
        '#A7FFEB',
        '#64FFDA',
        '#1DE9B6',
        '#00BFA5',
        '#E8F5E9',
        '#C8E6C9',
        '#A5D6A7',
        '#81C784',
        '#66BB6A',
        '#4CAF50',
        '#43A047',
        '#388E3C',
        '#2E7D32',
        '#1B5E20',
        '#B9F6CA',
        '#69F0AE',
        '#00E676',
        '#00C853',
        '#F1F8E9',
        '#DCEDC8',
        '#C5E1A5',
        '#AED581',
        '#9CCC65',
        '#8BC34A',
        '#7CB342',
        '#689F38',
        '#558B2F',
        '#33691E',
        '#CCFF90',
        '#B2FF59',
        '#76FF03',
        '#64DD17',
        '#F9FBE7',
        '#F0F4C3',
        '#E6EE9C',
        '#DCE775',
        '#D4E157',
        '#CDDC39',
        '#C0CA33',
        '#AFB42B',
        '#9E9D24',
        '#827717',
        '#F4FF81',
        '#EEFF41',
        '#C6FF00',
        '#AEEA00',
        '#FFFDE7',
        '#FFF9C4',
        '#FFF59D',
        '#FFF176',
        '#FFEE58',
        '#FFEB3B',
        '#FDD835',
        '#FBC02D',
        '#F9A825',
        '#F57F17',
        '#FFFF8D',
        '#FFFF00',
        '#FFEA00',
        '#FFD600',
        '#FFF8E1',
        '#FFECB3',
        '#FFE082',
        '#FFD54F',
        '#FFCA28',
        '#FFC107',
        '#FFB300',
        '#FFA000',
        '#FF8F00',
        '#FF6F00',
        '#FFE57F',
        '#FFD740',
        '#FFC400',
        '#FFAB00',
        '#FFF3E0',
        '#FFE0B2',
        '#FFCC80',
        '#FFB74D',
        '#FFA726',
        '#FF9800',
        '#FB8C00',
        '#F57C00',
        '#EF6C00',
        '#E65100',
        '#FFD180',
        '#FFAB40',
        '#FF9100',
        '#FF6D00',
        '#FBE9E7',
        '#FFCCBC',
        '#FFAB91',
        '#FF8A65',
        '#FF7043',
        '#FF5722',
        '#F4511E',
        '#E64A19',
        '#D84315',
        '#BF360C',
        '#FF9E80',
        '#FF6E40',
        '#FF3D00',
        '#DD2C00',
        '#EFEBE9',
        '#D7CCC8',
        '#BCAAA4',
        '#A1887F',
        '#8D6E63',
        '#795548',
        '#6D4C41',
        '#5D4037',
        '#4E342E',
        '#3E2723',
        '#FAFAFA',
        '#F5F5F5',
        '#EEEEEE',
        '#E0E0E0',
        '#BDBDBD',
        '#9E9E9E',
        '#757575',
        '#616161',
        '#424242',
        '#212121',
        '#ECEFF1',
        '#CFD8DC',
        '#B0BEC5',
        '#90A4AE',
        '#78909C',
        '#607D8B',
        '#546E7A',
        '#455A64',
        '#37474F',
        '#263238',
        '#000000',
    ]
    # colors = ['#4BC0D9', '#76E5FC', '#6457A6', '#5C2751', '#7D8491', '#BBBE64', '#64F58D', '#9DFFF9', '#AB4E68',
    #           '#C4A287',
    #           '#6F9283', '#696D7D', '#1B1F3B', '#454ADE', '#FB6376', '#6C969D', '#519872', '#3B5249', '#A4B494',
    #           '#CCFF66', '#FFC800',
    #           '#FF8427', '#0F7173', '#EF8354', '#795663', '#AF5B5B', '#667761', '#CF5C36', '#F0BCD4', '#ADB2D3',
    #           '#FF1B1C', '#6A994E',
    #           '#386641', '#8B2635', '#2E3532', '#124E78']
    # colors = ['#4BC0D9'] * 1000
    # colors = ['#edf1fe', '#c6e3f7', '#e1eaec', '#e5e8f2', '#def7fe', '#f1ebda', '#f3e2c6', '#fff2de', '#ecdfd6',
    #           '#f5e6d3',
    #           '#e3e7c4', '#efdbcd', '#ebf5f0', '#cae1d9', '#c3ddd6', '#cef0cc', '#9ab8c2', '#ddffdd', '#fdfff5',
    #           '#eae9e0', '#e0dddd',
    #           '#f5ece7', '#f6e6c5', '#f4dbdc', '#f4daf1', '#f7cee0', '#f8d0e7', '#efa6aa', '#fad6e5', '#f9e8e2',
    #           '#c4adc9', '#f6e5f6',
    #           '#feedca', '#f2efe1', '#fff5be', '#ffffdd']
    nodes_data = []
    id_circle = []
    name_circle = []
    edge_count = 0
    hex_list = []
    multiple_rfp = 0
    cir = 0
    edges = []
    random_list = []
    connection = []
    oval = []
    rcanframe = []
    abc = 0
    xyz = 0
    elines = []
    connectivity = []

    def return_everything(self):
        pass

    def createCanvas(self):
        self.id_circle.clear()
        self.name_circle.clear()
        for i in range(0, 100):
            self.id_circle.append(i)
        for i in range(0, 100):
            self.name_circle.append(str(i))
        self.nodes_data.clear()
        self.edges.clear()
        self.edge_count = 0
        self.oval.clear()
        self.rcanframe.clear()
        self.abc = 0
        self.hex_list.clear()
        self.xyz = 0
        self.elines.clear()
        # border_details = {'highlight-background': 'black', 'highlight-color': 'black', 'highlight-thickness': 1}
        self.canvas = tk.Canvas(self._root, bg=col[3], width=width, height=height)
        self.canvas.grid(column=0, row=1, sticky='nwes', columnspan=5, rowspan=2)
        self.canvas.create_line(width / 2.2, 0, width / 2.2, height / 1.27, fill="red", width=5)
        if platform.system() == 'Darwin':  # if macOS
            self.canvas.bind("<Button-2>", self.addH)
            self.connection = []
            self.canvas.bind("<Button-1>", self.button_1_clicked)
            self.canvas.bind("<Button-3>", self.remove_node)

        elif platform.system() == 'Windows' or platform.system() == 'Linux':  # if Windows or Linux
            self.canvas.bind("<Button-3>", self.addH)
            self.connection = []
            self.canvas.bind("<Button-1>", self.button_1_clicked)
            self.canvas.bind("<Button-2>", self.remove_node)
        self.ButtonReset = tk.Button(self._root, text="Reset", fg='white', width=10, height=2, **font, relief='flat',
                                     bg=col[1], command=self.reset)
        self.ButtonReset.grid(column=0, row=1, sticky='n', pady=20, padx=100)
        self.Generate = tk.Button(self._root, text="Generate Plan ", fg='white', width=10, height=2, **font,
                                  relief='flat', bg=col[1], command=self.send_vals)
        self.Generate.grid(column=0, row=1, sticky='ne', pady=20, padx=00)

    def send_vals(self):
        # self.master.open_file("./saved_files/
        print("Drawing floor plan.")
        msg = " "
        msg = Call_Main(G)
        print("Message:", msg)
        self.canvas.create_text(
            width / 4, height / 1.2, fill='black', font="Times 16 bold", text=msg)
        # image = Image.open("FloorPlans/floor_plan1.jpg").resize((280, 210))
        # photo = ImageTk.PhotoImage(image)

        # label = tk.Label(self.root, image=photo)
        # label.image = photo
        # label.grid(row=1, column=4, columnspan=1)
        # print("Yo")
        # image = Image.open("FloorPlans/floor_plan2.jpg").resize((280, 210))
        # photo = ImageTk.PhotoImage(image)

        # label = tk.Label(self.root, image=photo)
        # label.image = photo
        # label.grid(row=2, column=4, columnspan=1)

        # image = Image.open("FloorPlans/floor_plan3.jpg").resize((280, 210))
        # photo = ImageTk.PhotoImage(image)

        # label = tk.Label(self.root, image=photo)
        # label.image = photo
        # label.grid(row=1, column=3, columnspan=1)
        if msg is None or Main.cip_check == 1:
            image = Image.open("FloorPlans/floor_plan4.jpg").resize((640, 480))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.root, image=photo)
            label.image = photo
            label.grid(row=1, column=4, columnspan=1)
        # self.root.destroy()

    def instructions(self):
        pass
        # print("Instructions", "--------User Instructrions--------\n 1. Draw the input graph. \n 2. Use right mouse
        # click to create a new room. \n 3. left click on one node then left click on another to create an edge
        # between them. \n 4. You can give your own room names by clicking on the room name in the graph or the table
        # on the right. \n 5. After creating a graph you can choose one of the option to create it's corresponding
        # RFP or multiple RFPs with or without dimension. You can also get the corridor connecting all the rooms by
        # selecting 'circultion' or click on 'RFPchecker' to check if RFP exists for the given graph. \n 6. You can
        # also select multiple options .You can also add rooms after creating RFP and click on RFP to re-create a new
        # RFP. \n 7.Reset button is used to clear the input graph. \n 8. Press 'Exit' if you want to close the
        # application or Press 'Restart' if you want to restart the application")

    def addH(self, event):
        x, y = event.x, event.y
        id_node = self.id_circle[0]
        self.id_circle.pop(0)
        self.create_new_node(x, y, id_node)
        G.add_node(id_node + 1, pos=(x / 100, y / 100))
        print(id_node, "position", (x, y))

    def button_1_clicked(self, event):

        if len(self.connection) == 2:
            self.canvas.itemconfig(self.oval[self.xyz], outline='black')
            self.canvas.itemconfig(self.oval[self.abc], outline='black')
            self.connection = []
        if len(self.nodes_data) <= 1:
            print("Connect Nodes", "Please make 2 or more nodes")
            return
        x, y = event.x, event.y
        value = self.get_id(x, y)
        # print("Node created ", value, " at position x:", x, " y:", y)
        self.abc = self.xyz
        self.xyz = self.nodes_data[value].circle_id
        self.hover_bright(event)
        if value == -1:
            evalue = self.get_edge(x, y)
            if evalue == -1:
                return
            else:
                self.toggle_edge_connectivity(evalue)
            return
        else:
            if value in self.connection:
                print("Connect Nodes",
                      "You have clicked on same node. Please try again")
                return
            self.connection.append(value)

        if len(self.connection) > 1:
            node1 = self.connection[0]
            node2 = self.connection[1]

            if node2 not in self.nodes_data[node1].adj_list:
                self.nodes_data[node1].adj_list.append(node2)
            if node1 not in self.nodes_data[node2].adj_list:
                self.nodes_data[node2].adj_list.append(node1)
                self.edge_count += 1
            self.edges.append(self.connection)
            G.add_edge(node1 + 1, node2 + 1)
            self.connect_circles(self.connection)

    def connect_circles(self, connections):
        node1_id = connections[0]
        node2_id = connections[1]
        node1_x = self.nodes_data[node1_id].pos_x
        node1_y = self.nodes_data[node1_id].pos_y
        node2_x = self.nodes_data[node2_id].pos_x
        node2_y = self.nodes_data[node2_id].pos_y
        edge = self.canvas.create_line(
            node1_x, node1_y, node2_x, node2_y, width=3)
        self.elines.append([edge, connections])

    def toggle_edge_connectivity(self, evalue):
        for node1_id, node2_id in evalue:
            for eid, connection in self.elines:
                if (connection[0] == node1_id and connection[1] == node2_id) or (
                        connection[0] == node2_id and connection[1] == node1_id):
                    if self.canvas.itemcget(eid, "fill") == 'black':
                        self.canvas.itemconfig(eid, fill='red')
                        self.connectivity.append(connection)
                    else:
                        self.canvas.itemconfig(eid, fill='black')
                        try:
                            self.connectivity.remove(connection)
                        except:
                            pass
                    return

    def create_new_node(self, x, y, id_node):
        self.random_list.append(0)
        hex_number = self.colors[random.randint(0, len(self.colors))]
        self.hex_list.append(hex_number)
        node = self.master.Nodes(id_node, x, y)
        self.nodes_data.append(node)
        self.rframe = tk.Frame(self._root, width=20, height=20)
        self.rname = tk.StringVar(self._root)
        self.rnames.append(self.rname)
        self.rname.set(self.name_circle[0])
        self.name_circle.pop(0)
        self.rframe.grid(row=0, column=1)
        self.oval.append(self.canvas.create_oval(x - self.radius_circle, y - self.radius_circle, x + self.radius_circle,
                                                 y + self.radius_circle, width=3, fill=hex_number, tag=str(id_node)))
        self.canvas.create_text(x, y, fill='black', font="Times 16 bold", text=str(id_node + 1))
        self.rcanframe.append(self.canvas.create_window(
            x, y - self.radius_circle - 12, window=self.rframe))
        self.entry = tk.Entry(self.rframe, textvariable=self.id_circle[0], relief='flat', justify='c', width=3,
                              bg='white')
        self.entry.grid()

    def retreive_graph(self, node_data, edge_data, con_data):

        for node in node_data:
            x = node[0]
            y = node[1]
            id_node = node[2]
            self.create_new_node(x, y, id_node)

        self.edges = edge_data
        for edge in self.edges:
            self.connect_circles(edge)

        self.connectivity = con_data

        for eid, connection in self.elines:
            revcon = []
            revcon.append(connection[1])
            revcon.append(connection[0])

            if connection in con_data or revcon in con_data:
                self.canvas.itemconfig(eid, fill='red')

        self.edge_count = len(self.edges)

        self.id_circle.clear()
        self.name_circle.clear()
        for i in range(len(self.nodes_data), 100):
            self.id_circle.append(i)
        for i in range(len(self.nodes_data), 100):
            self.name_circle.append(str(i))

    def get_edge(self, x, y):
        ans = []
        for i_no, i in enumerate(self.nodes_data):
            for j_no, j in enumerate(self.nodes_data):
                if i_no == j_no:
                    continue
                epsi = (x - i.pos_x) * (i.pos_y - j.pos_y) / \
                       (i.pos_x - j.pos_x) + i.pos_y - y
                if ((j.pos_x >= x >= i.pos_x) or (x >= i.pos_x >= x)) and (
                        (i.pos_y >= y >= j.pos_y) or (
                        i.pos_y <= y <= j.pos_y)) and 10 > epsi > -10:
                    ans.append((i_no, j_no))
        if not ans:
            print("Connect Nodes",
                  "You have clicked outside all the circles and edges. Please try again")
            return -1
        else:
            return ans

    def get_id(self, x, y):
        for j, i in enumerate(self.nodes_data):
            distance = ((i.pos_x - x) ** 2 + (i.pos_y - y) ** 2) ** (1 / 2)
            if distance <= self.radius_circle:
                return j
        # print("Connect Nodes","You have clicked outside all the circles. Please try again")
        return -1

    def remove_node(self, event):
        id = self.get_id(event.x, event.y)
        # id = self.nodes_data[id].circle_id
        self.canvas.delete(self.oval[id])
        self.canvas.delete(self.rcanframe[id])
        for i in self.elines:
            if i[1][0] == id or i[1][1] == id:
                self.canvas.delete(i[0])
                self.edges.remove(i[1])
                self.edge_count -= 1
        self.nodes_data[id].clear()
        self.nodes_data.pop(id)
        self.hex_list.pop(id)
        for j in range(self.table.number_of_columns):
            self.table._data_vars[id][j].set("")
        self.table._data_vars.pop(id)
        # self.edges.pop(id)
        # self.table.delete_row(id)
        i = id
        # while i < self.table._number_of_rows-1:
        #     row_of_vars_1 = self.table._data_vars[i]
        #     row_of_vars_2 = self.table._data_vars[i+1]

        #     j = 0
        #     while j <self.table._number_of_columns:
        #         row_of_vars_1[j].set(row_of_vars_2[j].get())
        #         j+=1
        #     i += 1

        # self.table._pop_n_rows(1)
        # self.table._number_of_rows-=1
        # self.table._data_vars.pop(id)
        for j in range(self.table.number_of_columns):
            self.table.grid_slaves(row=i + 1, column=j)[0].destroy()
        self.table._number_of_rows -= 1

        # if self.table._on_change_data is not None: self.table._on_change_data()

    def hover_bright(self, event):
        # self.canvas.itemconfig(self.oval[self.xyz],outline='red')
        self.canvas.itemconfig(self.oval[self.xyz], outline='black')

    def reset(self):
        global G
        Main.cip_check = 0
        G = nx.Graph()
        self.canvas.destroy()
        self.createCanvas()


# if __name__ == "_main__":
main = MainApp()
print("hi")
main.run_app()
