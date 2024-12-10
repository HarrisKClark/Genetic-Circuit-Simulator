import math
import random

import pygame
import matplotlib
from numpy.ma.core import append
from pygame.event import clear

matplotlib.use("tkagg")
matplotlib.use("Agg")
import numpy as np
import tkinter as tk

from Genetic_dict import Genetic_Circuit

last_time = 2000
last_dt = 1
last_mode = "deterministic"

pygame.init()

FPS = 60

WIDTH = 1000
HEIGHT = 600
SIZE = 20

bleeblo = False

font = pygame.font.Font('freesansbold.ttf', 17)
font2 = pygame.font.Font('freesansbold.ttf', 32)
font3 = pygame.font.Font('freesansbold.ttf', 13) #node font
font4 = pygame.font.Font('freesansbold.ttf',  15) #big node font

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

icon_image = pygame.image.load("logo.jpg")
pygame.display.set_icon(icon_image)

image_path = "emptygraph.PNG"
empty_graph_image = pygame.image.load(image_path)

image_path = "clearsymbol.png"
clearsymbol = pygame.image.load(image_path)

image_path = "compilesymbol.png"
compilesymbol = pygame.image.load(image_path)

pygame.display.set_caption("Gene Network Visualizer")

class UserInterface:
   def __init__(self):
       self.x = WIDTH-200
       self.color1 = (150, 150, 150)
       self.color2 = (0, 0, 0)

       self.regulatory_genes_x, self.regulatory_genes_y = WIDTH - 185, 10
       self.reporter_genes_x, self.reporter_genes_y = WIDTH - 185, self.regulatory_genes_y+35
       self.inducer_x, self.inducer_y = self.reporter_genes_x, self.reporter_genes_y+35

       self.simulate_x, self.simulate_y = WIDTH - 185, 530
       self.run_x, self.run_y = WIDTH - 185, self.simulate_y+35

        #drop downs=

        #report
       self.gfp_x, self.gfp_y = WIDTH-185, 150 #use this to anchor others

       self.rfp_x, self.rfp_y = WIDTH - 185, self.gfp_y +35
       self.bfp_x, self.bfp_y = WIDTH-185, self.rfp_y +35

        #regulatory
       self.node_x, self.node_y = WIDTH - 185, self.gfp_y

       #inducers
       self.IPTG_x, self.IPTG_y = WIDTH - 185, self.gfp_y
       self.Arabinose_x, self.Arabinose_y = WIDTH - 185, self.IPTG_y +35


       # main buttons
       self.regulatory = False
       self.reporter = False
       self.inducer = False
       self.simulate = False

       # node types
       self.current_node = "None"

       # reporter drop down
       self.gfp = False
       self.rfp = False
       self.bfp = False

       # regulatory drop down
       self.node = False

       # inducer drop down
       self.iptg = False
       self.arabinose = False

       #sim settings
       self.simulate_settings = False

       #default, t, dt, mode
       self.settings = {'time': 2000, 'dt': 1, 'mode': 'deterministic', 'inducer_times': {"1": 0, "2": 0}}

       self.RUN = False

       self.screen = "draw"

       self.clear = False


   # draws all the buttons and stuff
   def draw(self):
       # draw menu background

        #clear symbol
       image_x, image_y = self.x-35, 5
       image_width, image_height = 30, 30
       clearsymboln = pygame.transform.scale(clearsymbol, (image_width, image_height))

       WIN.blit(clearsymboln, (image_x, image_y)) 

       # compile symbol
       image_width, image_height = 30, 30
       compilesymboln = pygame.transform.scale(compilesymbol, (image_width, image_height))

       WIN.blit(compilesymboln, (image_x-40, image_y))


       #window select
       pygame.draw.rect(WIN, self.color2, (10, 6, 180, 35), 1)
       pygame.draw.rect(WIN, self.color2, (189, 6, 180, 35), 1)


       pygame.draw.rect(WIN, (255, 255, 255), (self.x, 0, 300, HEIGHT))
       pygame.draw.line(WIN, (0,0,0), (self.x, 0), (self.x, HEIGHT))
       pygame.draw.line(WIN, (0, 0, 0), (0, HEIGHT-40), (self.x, HEIGHT-40))
       pygame.draw.line(WIN, (0, 0, 0), (0, 40), (self.x, 40))
       pygame.draw.line(WIN, (0, 0, 0), (self.x, self.inducer_y+40), (WIDTH, self.inducer_y+40))

       #pygame.draw.rect(WIN, self.color2, (self.regulatory_genes_x - 5, self.regulatory_genes_y - 5, 180, 30))
       pygame.draw.rect(WIN, self.color2, (self.reporter_genes_x - 5, self.reporter_genes_y - 5, 180, 30),1)
       pygame.draw.rect(WIN, self.color2, (self.simulate_x - 5, self.simulate_y - 5, 180, 30),1)
       pygame.draw.rect(WIN, self.color2, (self.run_x - 5, self.run_y - 5, 180, 30),1)
       pygame.draw.rect(WIN, self.color2, (self.inducer_x - 5, self.inducer_y - 5, 180, 30),1)
       pygame.draw.rect(WIN, self.color2, (self.regulatory_genes_x - 5, self.regulatory_genes_y - 5, 180, 30),1)


       button_regulatory = font.render("Regulatory Genes", True, (0, 0, 0))
       button_reporter = font.render("Reporter Genes", True, (0, 0, 0))
       button_simulation_settings = font.render("Simulation Settings", True, (0, 0, 0))
       button_run_simulation = font.render("Run Simulation", True, (0, 0, 0))
       button_inducer = font.render("Inducers", True, (0, 0, 0))


       WIN.blit(button_regulatory, (self.regulatory_genes_x, self.regulatory_genes_y))
       WIN.blit(button_reporter, (self.reporter_genes_x, self.reporter_genes_y))
       WIN.blit(button_simulation_settings, (self.simulate_x, self.simulate_y))
       WIN.blit(button_run_simulation,(self.run_x, self.run_y) )
       WIN.blit(button_inducer, (self.inducer_x, self.inducer_y))

       #display current node selected
       current_node_disp = font.render("Current Selected Node: " + self.current_node, True, (0, 0, 0))
       WIN.blit(current_node_disp, (10, HEIGHT-28))


       if self.screen == "draw":
           pygame.draw.line(WIN, (255, 255, 255), (11, 40), (188, 40),1)\

       if self.screen == "sim":
           pygame.draw.line(WIN, (255, 255, 255), (190, 40), (367, 40), 1)

       current_node_disp = font.render("Draw", True, (0, 0, 0))
       WIN.blit(current_node_disp, (30, 14))
       current_node_disp = font.render("Results", True, (0, 0, 0))
       WIN.blit(current_node_disp, (210, 14))

       if self.reporter: # reporter gene drop down menu
           #gfp
           pygame.draw.rect(WIN, self.color2, (self.gfp_x - 5, self.gfp_y - 5, 180, 30),1)
           button_invert = font.render("GFP", True, (0, 0, 0))
           WIN.blit(button_invert, (self.gfp_x, self.gfp_y))
            #rfp
           pygame.draw.rect(WIN, self.color2, (self.rfp_x - 5, self.rfp_y - 5, 180, 30),1)
           button_invert = font.render("RFP", True, (0, 0, 0))
           WIN.blit(button_invert, (self.rfp_x, self.rfp_y))
            #bfp
           pygame.draw.rect(WIN, self.color2, (self.bfp_x - 5, self.bfp_y - 5, 180, 30),1)
           button_invert = font.render("BFP", True, (0, 0, 0))
           WIN.blit(button_invert, (self.bfp_x, self.bfp_y))

       if self.regulatory: #regulatory drop down menu
           pygame.draw.rect(WIN, self.color2, (self.node_x - 5, self.node_y - 5, 180, 30),1)
           button_invert = font.render("Ideal Gene", True, (0, 0, 0))
           WIN.blit(button_invert, (self.node_x, self.node_y))

       if self.inducer:
           #IPTG
           pygame.draw.rect(WIN, self.color2, (self.IPTG_x - 5, self.IPTG_y - 5, 180, 30),1)
           button_invert = font.render("IPTG", True, (0, 0, 0))
           WIN.blit(button_invert, (self.IPTG_x, self.IPTG_y))

           # Arabinose
           pygame.draw.rect(WIN, self.color2, (self.Arabinose_x - 5, self.Arabinose_y - 5, 180, 30),1)
           button_invert = font.render("Arabinose", True, (0, 0, 0))
           WIN.blit(button_invert, (self.Arabinose_x, self.Arabinose_y))


   def button_press(self, x, y):
       #clicked draw window
       if valid_press(x, y, 10, 6):
           self.screen = "draw"

        # results window
       if valid_press(x, y, 189, 6):
           self.screen = "sim"


       if valid_press(x, y, self.regulatory_genes_x, self.regulatory_genes_y):
           if self.regulatory:
               self.regulatory = False
           else:
               self.regulatory = True
               self.inducer = False
               self.reporter = False

       if valid_press(x, y, self.reporter_genes_x, self.reporter_genes_y):
           if self.reporter:
               self.reporter = False
           else:
               self.regulatory = False
               self.inducer = False
               self.reporter = True

       if valid_press(x, y, self.inducer_x, self.inducer_y):
           if self.inducer:
               self.inducer = False
           else:
               self.inducer = True
               self.regulatory = False
               self.reporter = False

        # simulate settings
       if valid_press(x, y, self.simulate_x, self.simulate_y):
           if self.simulate_settings == False:
               self.simulate_settings = True

               self.settings = show_settings_window()

               self.simulate_settings = False

        # RUN SIMULATION
       if valid_press(x, y, self.run_x, self.run_y):
           if self.RUN == False:
               self.RUN = True

        #reporter drop down
       if valid_press(x, y, self.gfp_x, self.gfp_y) and self.reporter:
           self.gfp = not self.gfp
           self.rfp = False
           self.bfp = False
           self.current_node = "GFP"

       if valid_press(x, y, self.rfp_x, self.rfp_y) and self.reporter:
           self.rfp = not self.rfp
           self.gfp = False
           self.bfp = False
           self.current_node = "RFP"

       if valid_press(x, y, self.bfp_x, self.bfp_y) and self.reporter:
           self.bfp = not self.bfp
           self.gfp = False
           self.rfp = False
           self.current_node = "BFP"

        #regulatory drop down
       if valid_press(x, y, self.node_x, self.node_y) and self.regulatory: # node
           self.node = not self.node
           self.current_node = "Node"
           print("poo")

       #inducer drop down
       if valid_press(x, y, self.IPTG_x, self.IPTG_y) and self.inducer: # node
           self.iptg = not self.iptg
           self.arabinose = False

           self.current_node = "IPTG"
           self.current_inducer = "IPTG"
           print("pee")

       if valid_press(x, y, self.Arabinose_x, self.Arabinose_y) and self.inducer:  # node
           self.arabinose = not self.iptg
           self.iptg = False
           self.current_node = "Arabinose"
           self.current_inducer = "Arabinose"

       if clear_press(x,y,self.x):
            self.clear = True

def valid_press(x, y, x2, y2):
   if(x > x2-5) and (x < x2 + 185):
       if(y > y2-5) and (y < y2 + 25):
           return True
   return False

def clear_press(x,y,ss):
    if (math.hypot(ss-35-x+15, 5-y+15) < 15):
        return True
    return False


def show_settings_window():
    global last_time, last_dt, last_mode

    settings_window = tk.Tk()
    settings_window.title("Simulation Settings")

    window_width = 400
    window_height = 350
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    settings_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Time entry
    tk.Label(settings_window, text="Total Simulation Time").grid(row=0, column=0, padx=10, pady=10)
    time_entry = tk.Entry(settings_window)
    time_entry.insert(0, str(last_time))  # Set to last time or default
    time_entry.grid(row=0, column=1, padx=10, pady=10)

    # dt entry
    tk.Label(settings_window, text="Time Step (dt)").grid(row=1, column=0, padx=10, pady=10)
    dt_entry = tk.Entry(settings_window)
    dt_entry.insert(0, str(last_dt))  # Set to last dt or default
    dt_entry.grid(row=1, column=1, padx=10, pady=10)

    # Mode radio buttons
    tk.Label(settings_window, text="Mode").grid(row=2, column=0, padx=10, pady=10)
    mode_var = tk.StringVar(value=last_mode)  # Set to last selected mode
    tk.Radiobutton(settings_window, text="Deterministic", variable=mode_var, value="deterministic").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(settings_window, text="Stochastic", variable=mode_var, value="stochastic").grid(row=2, column=2, sticky="w")

    # Inducer Start Time entries for "arabinose" and "IPTG"
    tk.Label(settings_window, text="Inducer Start Times").grid(row=3, column=0, columnspan=2, pady=(15, 5))

    tk.Label(settings_window, text="Start time for Arabinose").grid(row=4, column=0, padx=10, pady=5)
    arabinose_entry = tk.Entry(settings_window)
    arabinose_entry.insert(0, "0")  # Default to 0 if no value specified
    arabinose_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Start time for IPTG").grid(row=5, column=0, padx=10, pady=5)
    iptg_entry = tk.Entry(settings_window)
    iptg_entry.insert(0, "0")  # Default to 0 if no value specified
    iptg_entry.grid(row=5, column=1, padx=10, pady=5)

    # Container to store result
    settings = {'time': 0, 'dt': 0, 'mode': 'deterministic', 'inducer_times': {}}

    def save_and_close():
        global last_time, last_dt, last_mode
        # Save settings
        settings['time'] = int(time_entry.get())
        settings['dt'] = int(dt_entry.get())
        settings['mode'] = mode_var.get()
        # Save inducer start times
        settings['inducer_times']['arabinose'] = int(arabinose_entry.get())
        settings['inducer_times']['iptg'] = int(iptg_entry.get())

        # Update last entered values
        last_time = settings['time']
        last_dt = settings['dt']
        last_mode = settings['mode']

        settings_window.destroy()

    tk.Button(settings_window, text="OK", command=save_and_close).grid(row=6, column=0, columnspan=3, pady=10)
    settings_window.mainloop()

    return settings


class Node:
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.color = (230, 230, 230)
       self.type = "node"
       self.text = "Ideal"

class Inducer(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "inducer"

class Iptg(Inducer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (200, 200, 250)
        self.type = "iptg"
        self.text = "IPTG"

class Arabinose(Inducer):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (200, 200, 250)
        self.type = "arabinose"
        self.text = "ARABINOSE"

class RegulatoryNode(Node):
   def __init__(self, x, y):
       super().__init__(x, y)
       self.type = "regulatory"

class ReporterNode(Node):
   def __init__(self, x, y):
       super().__init__(x, y)
       self.type = "reporter"

class RFPNode(ReporterNode):
   def __init__(self, x, y):
       super().__init__(x, y)
       self.color = (200, 90, 90)
       self.type = "rfp"
       self.text = "RFP"


class GFPNode(ReporterNode):
   def __init__(self, x, y):
       super().__init__(x, y)
       self.color = (90, 200, 90)
       self.type = "gfp"
       self.text = "GFP"

class BFPNode(ReporterNode):
   def __init__(self, x, y):
       super().__init__(x, y)
       self.color = (90, 90, 200)
       self.type = "bfp"
       self.text = "BFP"


class Edge():
   def __init__(self, node1, node2, type):
       self.node1 = node1
       self.node2 = node2
       self.type = type


def find_path(graph, start, finish):
   paths = graph.get(start)

   for path in paths:
       if path == finish:
           return path

   newPaths = []

   for path in paths:
       tempPath = graph.get(path)
       for path2 in tempPath:
           newPaths.append(path2)

   find_path(newPaths, start, finish)


def draw_node(node, px, py):
   if math.hypot(node.x - px,node.y - py) < SIZE:
       pygame.draw.circle(WIN, (0, 0, 0), (node.x, node.y), SIZE + 3)
       pygame.draw.circle(WIN, node.color, (node.x, node.y), SIZE + 2)
       text_surface = font4.render(str(node.text), True, (0, 0, 0))
   else:
       pygame.draw.circle(WIN, (0, 0, 0), (node.x, node.y), SIZE + 1)
       pygame.draw.circle(WIN, node.color, (node.x, node.y), SIZE)
       text_surface = font3.render(str(node.text), True, (0, 0, 0))

   text_rect = text_surface.get_rect(center=(node.x, node.y))
   WIN.blit(text_surface, text_rect)


def draw_edge(x1, y1, x2, y2, edge_type):
   dir1 = math.atan2((y2 - y1), (x2 - x1))
   dir2 = dir1 + math.pi

   pygame.draw.line(WIN, (0, 0, 0),(x1 - SIZE*math.cos(dir2), y1 - SIZE*math.sin(dir2)), (x2 + SIZE*math.cos(dir2), y2 + SIZE*math.sin(dir2)),3)

   if edge_type=="activator":
       pygame.draw.line(WIN, (0, 0, 0), (x2 + SIZE*math.cos(dir2), y2 + SIZE*math.sin(dir2)), (x2 + SIZE*math.cos(dir2) + SIZE*math.cos(dir2 + math.pi/4), y2 + SIZE*math.sin(dir2) + SIZE*math.sin(dir2 + math.pi/4)), 3)
       pygame.draw.line(WIN, (0, 0, 0), (x2 + SIZE*math.cos(dir2), y2 + SIZE*math.sin(dir2)), (x2 + SIZE*math.cos(dir2) + SIZE*math.cos(dir2 - math.pi/4), y2 + SIZE*math.sin(dir2) + SIZE*math.sin(dir2 - math.pi/4)), 3)

   if edge_type=="repressor":
       pygame.draw.line(WIN, (0, 0, 0), (x2 + 20*math.cos(dir2 + math.pi/4), y2 + 20*math.sin(dir2+ math.pi/4)), (x2 + 20*math.cos(dir2 - math.pi/4), y2 + 20*math.sin(dir2 - math.pi/4)), 3)


def add_graph(graph,node, edge):
   if(node == None):
       graph.get(edge.node1).append(edge.node2)
       graph.get(edge.node2).append(edge.node1)

   if(edge == None):
       graph[node] = []

   return graph


def valid_position(nodes,x,y):
   if x < WIDTH - (200 + SIZE) and x > SIZE and y > 40+SIZE and y < (HEIGHT- + SIZE):
       for node in nodes:
           if math.hypot(node.x-x, node.y-y) < SIZE*2:
               return False
       return True
   return False




def compile_genetic_circuit(nodes, edges, times):
   no_inducer_nodes = []
   inducer_nodes = []

   for node in nodes:
       if not isinstance(node, Inducer):
            no_inducer_nodes.append(node)
       else:
           inducer_nodes.append(node)

   nodes = no_inducer_nodes

   gene_circuit_dict = {}
   inducer_dict = {}

   for i in range(1, len(nodes)+1):
       gene_circuit_dict[str(i)] =[[], [], [], [], 0.2, 0.01, 0]

   for i in range(1,len(inducer_nodes)+1):

       try:
           if inducer_nodes[i - 1].type == "iptg":
               time = int(times["iptg"])
           else:
               time = int(times["arabinose"])

       except KeyError as e:
           return {}, {}

       inducer_dict[str(i)] = [[], [], int(times[str(inducer_nodes[i-1].type)])]


   inducer_count = 1


   for inducer in inducer_nodes:
       for edge in edges:
           if edge.node1 == inducer:

               if edge.type == "activator":
                   inducer_dict[str(inducer_count)][0].append(nodes.index(edge.node2)+1)

       #1 ideal
       inducer_dict[str(inducer_count)][1] = [1] * len(nodes)

       inducer_count += 1

   node_count = 1

   for node in nodes:
       if node.type == "rfp":
           gene_circuit_dict[str(node_count)][6] = 1

       elif node.type == "gfp":
           gene_circuit_dict[str(node_count)][6] = 2

       elif node.type == "bfp":
           gene_circuit_dict[str(node_count)][6] = 3

       else:
           gene_circuit_dict[str(node_count)][6] = 0

       for edge in edges:
           if edge.node1 == node:
               if edge.type == "repressor":
                   gene_circuit_dict[str(node_count)][1].append(nodes.index(edge.node2)+1)
               else:
                   gene_circuit_dict[str(node_count)][0].append(nodes.index(edge.node2)+1)


       # non - idealities (1 is ideal)
       for i in range(0,len(nodes)):
           gene_circuit_dict[str(node_count)][2].append(1)
           gene_circuit_dict[str(node_count)][3].append(1)

       node_count +=1

   for value in gene_circuit_dict.values():
       if value[0] == []:
           value[0] = [0]

       if value[1] == []:
           value[1] = [0]


   return gene_circuit_dict, inducer_dict


def main():
   clock = pygame.time.Clock()
   nodes = []
   edges = []
   addnode = []
   ReporterNodes = []

   graph = {}
   ui = UserInterface()

   run = True
   while run:
       poop = False
       x, y = pygame.mouse.get_pos()
       clock.tick(FPS)
       pressed = pygame.key.get_pressed()

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               run = False

           # add repressor
           if event.type == pygame.MOUSEBUTTONDOWN and pressed[pygame.K_SPACE] and ui.screen=="draw":
               for node in nodes:

                   if math.hypot(node.x - x, node.y - y) < SIZE:
                       if len(addnode) == 0:
                           if (not issubclass(type(node), Inducer)) and (not issubclass(type(node), ReporterNode)):
                               addnode.append(node)

                           else:
                                addnode.clear()

                       else:
                           if not issubclass(type(node), Inducer):
                               addnode.append(node)
                               edge = Edge(addnode[0], addnode[1], "repressor")
                               edges.append(edge)
                               graph = add_graph(graph, None, edge)

                               addnode.clear()

                           else:
                               addnode.pop

           # add activator
           if event.type == pygame.MOUSEBUTTONDOWN and pressed[pygame.K_LSHIFT] and ui.screen=="draw":
               for node in nodes:

                   if math.hypot(node.x - x, node.y - y) < SIZE:
                       if len(addnode) == 0:
                           if not issubclass(type(node), ReporterNode):
                               addnode.append(node)

                           else:
                               addnode.clear()

                       else:
                           if not issubclass(type(node), Inducer):
                               addnode.append(node)
                               edge = Edge(addnode[0], addnode[1], "activator")
                               edges.append(edge)
                               graph = add_graph(graph, None, edge)

                               addnode.clear()

                           else:
                               addnode.pop


           # checks for right and left input
           elif event.type == pygame.MOUSEBUTTONDOWN:

               ui.button_press(x, y)

               if event.button == 1:
                   if valid_position(nodes,x,y)  and ui.screen=="draw":

                       if ui.current_node == "None":
                           break

                       elif ui.current_node == "IPTG":
                           node = Iptg(x, y)

                       elif ui.current_node == "Arabinose":
                           node = Arabinose(x, y)

                       elif ui.current_node == "GFP":
                            node = GFPNode(x, y)

                       elif ui.current_node == "RFP":
                           node = RFPNode(x, y)

                       elif ui.current_node == "BFP":
                           node = BFPNode(x, y)

                       elif ui.current_node == "Node":
                           node = Node(x, y)

                       elif ui.current_node == "Expressed Node":
                           node = ExpressedNode(x, y)


                       nodes.append(node)
                       graph = add_graph(graph, node, None)

               # remove node and connected edges
               elif event.button == 3  and ui.screen=="draw":
                   temp_nodes = nodes.copy()
                   remove = []

                   for node in temp_nodes:
                       if math.hypot(node.x - x, node.y - y) < SIZE:

                           for edge in edges:
                               if edge.node1 == node or edge.node2 == node:
                                   remove.append(edge)

                           temp_nodes.remove(node)

                           try:
                               if addnode[0] == node:
                                   addnode.clear()
                           except IndexError:
                               pass

                   for r in remove:
                       edges.remove(edges[edges.index(r)])

                   nodes = temp_nodes.copy()

       WIN.fill((250, 250, 250))

       if ui.screen=="draw":
            for node in nodes:
                draw_node(node,x,y)

            for edge in edges:
                draw_edge(edge.node1.x, edge.node1.y, edge.node2.x, edge.node2.y, edge.type)

       ui.draw()

       if ui.RUN:
           genetic_circuit_dict, inducer_dict = compile_genetic_circuit(nodes, edges, ui.settings["inducer_times"])

           Initial_concentrations = [0.1] * len(genetic_circuit_dict)

           time = ui.settings["time"]
           dt = ui.settings["dt"]

           inducer_times = ui.settings["inducer_times"]

           circuit = Genetic_Circuit(genetic_circuit_dict,Initial_concentrations, inducer_dict,inducer_times)
           circuit.simulate(time, dt, ui.settings["mode"])
           circuit.plot_circuit()

           image_path = "plot.png"
           empty_graph_image = pygame.image.load(image_path)

           poop = True

       if poop:
           bleeblo = True
           ui.RUN = False
           poop = False

       if ui.clear:
           ui.clear = False
           nodes = []
           edges = []

       if ui.screen=="sim":
           try:
               image_x, image_y = 0, 41
               image_width, image_height = ui.x, HEIGHT - 79
               empty_graph_image_mod = pygame.transform.smoothscale(empty_graph_image, (image_width, image_height))

               WIN.blit(empty_graph_image_mod, (image_x, image_y))
           except Exception as e:
               image_path = "emptygraph.PNG"
               empty_graph_image = pygame.image.load(image_path)

               image_x, image_y = 0, 41
               image_width, image_height = ui.x, HEIGHT - 79
               empty_graph_image_mod = pygame.transform.smoothscale(empty_graph_image, (image_width, image_height))

               WIN.blit(empty_graph_image_mod, (image_x, image_y))

       pygame.display.flip()
   pygame.quit()


if __name__ == '__main__':
   main()
