import tkinter as tk
import noName
import dijkstra as visualDijkstra
import kruskal as visualKruskal
import prim as visualPrim
from tkinter.filedialog import askopenfilename, asksaveasfilename


numberOfNodes = 0
listAllItems = {} # dic chua tat cac item duoc tao trong canv
flag = "nameFunction"
points = [] # ve duong thang neu points chua hai diem
weight = 0
listofEdges = []
listofVertexes = []



class vertex():
    def __init__(self, x, y, nameOfNode, neighbors):
        self.x = x
        self.y = y
        self.nameOfNode = nameOfNode
        self.neighbors = neighbors

class edge():
    def __init__(self, point1, point2, weight):
        self.point1 = point1
        self.point2 = point2
        self.weight = weight

class point():
    def __init__(self, x, y, nameOfNode):
        self.x = x
        self.y = y
        self.nameOfNode = nameOfNode

def openFile():
    global  listofEdges
    global  listofVertexes
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "r") as inputFile:
        textVertexes, textEdges = inputFile.readlines()
        for textVertex in textVertexes.split('and'):
            if textVertex == '\n':
                continue
            textX, textY, textNameOfNode, textNeighbors = textVertex.split('-')
            listofVertexes.append(vertex(int(textX), int(textY), int(textNameOfNode), eval(textNeighbors)))
        print(listofVertexes)

        for textEdge in textEdges.split('and'):
            if textEdge == '':
                continue
            textPoint1, textPoint2, textWeight = textEdge.split('+')
            """Poin1"""
            textX, textY, textNameOfNode = textPoint1.split('-')
            point1 = point(int(textX), int(textY), int(textNameOfNode))
            """Poin2"""
            textX, textY, textNameOfNode = textPoint2.split('-')
            point2 = point(int(textX), int(textY), int(textNameOfNode))

            listofEdges.append(edge(point1, point2, int(textWeight)))
        print(listofEdges)

    noName.drawShape(listofEdges, listofVertexes, canv)

    window.title(f"Graph - {filepath}")


def saveFile():
    global  listofEdges
    global  listofVertexes
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as outputFile:
        textVertexes = ''
        textEdges = ''
        for vertex in listofVertexes:
            textVertexes += str(vertex.x) + '-' + str(vertex.y) + '-' + str(vertex.nameOfNode)  + '-' + str(vertex.neighbors)
            textVertexes += 'and'
        for edge in listofEdges:
            textEdges += str(edge.point1.x) + '-' + str(edge.point1.y) + '-' + str(edge.point1.nameOfNode) + '+' +\
                        str(edge.point2.x) + '-' + str(edge.point2.y) + '-' + str(edge.point2.nameOfNode) + '+' +\
                        str(edge.weight)
            textEdges += 'and'
        outputFile.write(textVertexes + '\n' + textEdges)
    window.title(f"Graph - {filepath}")


def getWeight():
    def getEntry():
        weight = entWeight.get()
        createWeight((points[0].x + points[1].x) / 2, (points[0].y + points[1].y) / 2, weight, canv)
        listofEdges.append(edge(points[0], points[1], int(weight)))
        listofVertexes[points[0].nameOfNode].neighbors[points[1].nameOfNode] = len(listofEdges) - 1
        listofVertexes[points[1].nameOfNode].neighbors[points[0].nameOfNode] = len(listofEdges) - 1
        points.clear()
        formGetWeight.destroy()
        return

    formGetWeight = tk.Tk()

    windowWidth = formGetWeight.winfo_reqwidth()
    windowHeight = formGetWeight.winfo_reqheight()

    positionRight = int(formGetWeight.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(formGetWeight.winfo_screenheight()/2 - windowHeight/2)

    formGetWeight.geometry("+{}+{}".format(positionRight, positionDown))


    lblWeight = tk.Label(master=formGetWeight, text="Weight:")
    lblWeight.pack(side=tk.LEFT)

    entWeight = tk.Entry(master=formGetWeight)
    entWeight.pack(side=tk.LEFT)

    btnSubmit = tk.Button(master=formGetWeight, text="Submit", command=getEntry)
    btnSubmit.pack()


def createVertex(x, y, r, canvasName, nameOfNode): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    idItem = canvasName.create_oval(x0, y0, x1, y1, fill="white")
    listAllItems[idItem] = point(x, y, nameOfNode)
    idItem = canvasName.create_text(x, y, text=str(nameOfNode))
    listAllItems[idItem] = point(x, y, nameOfNode)
    return idItem

def createWeight(x, y, text, canvasName):
    idItem = canvasName.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="yellow")
    listAllItems[idItem] = point(0, 0, 0)
    idItem = canvasName.create_text(x, y, text=text)
    listAllItems[idItem] = point(0, 0, 0)

def clear():
    global numberOfNodes
    global wieght
    global flag
    numberOfNodes = 0
    for  item in listAllItems:
        canv.delete(item)
    listAllItems.clear()
    flag = "nameFunction"
    points.clear()
    weight = 0
    listofEdges.clear()
    listofVertexes.clear()
    btnClear.focus_set()




def addVertex():
    global flag
    btnAddVertex.focus_set()
    flag = "AddVertex"
    points.clear()

def connectVertexes():
    global flag
    btnConnect.focus_set()
    flag = "ConnectVertex"
    points.clear()


def solve(eventorigin):
    global numberOfNodes
    print(eventorigin)
    if flag == "AddVertex":
        createVertex(eventorigin.x, eventorigin.y, 10, canv, numberOfNodes)
        listofVertexes.append(vertex(eventorigin.x, eventorigin.y, numberOfNodes, {}))
        numberOfNodes += 1
    elif flag == "ConnectVertex":
        points.append(listAllItems[canv.find_closest(eventorigin.x, eventorigin.y)[0]])
        if len(points) == 2:
            idItem = canv.create_line(points[0].x, points[0].y, points[1].x,
                                      points[1].y, width=5, fill="black", smooth=True)
            listAllItems[idItem] = point(0, 0, 0)
            createVertex(points[0].x, points[0].y, 10, canv, points[0].nameOfNode)
            createVertex(points[1].x, points[1].y, 10, canv, points[1].nameOfNode)
            getWeight()

def dijkstra():
    visualDijkstra.dijkstra(listofEdges, listofVertexes, window)

def kruskal():
    visualKruskal.kruskal(listofEdges, listofVertexes, window)

def prim():
    visualPrim.prim(listofEdges, listofVertexes, window)





window = tk.Tk()
window.title("Main program")
window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


frmButton = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5)

btnAddVertex = tk.Button(master=frmButton, text="Add vertex", width=20, command=addVertex)
btnAddVertex.pack(pady=5, padx=5)

btnConnect = tk.Button(master=frmButton, text="Connect vertexes", width=20, command=connectVertexes)
btnConnect.pack(pady=5, padx=5)

btnClear = tk.Button(master=frmButton, text="Clear", width=20, command=clear)
btnClear.pack(pady=5, padx=5)

btnOpen = tk.Button(master=frmButton, text="Open", width=20, command=openFile)
btnOpen.pack(pady=5, padx=5)

btnSaveAs = tk.Button(master=frmButton, text="Save As...", width=20, command=saveFile)
btnSaveAs.pack(pady=5, padx=5)


btnDijkstra = tk.Button(master=frmButton, text="Dijkstra", width=20, command=dijkstra)
btnDijkstra.pack(side=tk.BOTTOM, pady=5, padx=5)

btnKruskal = tk.Button(master=frmButton, text="Kruskal", width=20, command=kruskal)
btnKruskal.pack(side=tk.BOTTOM, pady=5, padx=5)

btnPrim = tk.Button(master=frmButton, text="Prim", width=20, command=prim)
btnPrim.pack(side=tk.BOTTOM, pady=5, padx=5)


lblAlgor = tk.Label(master=frmButton, text="Algorithms", width=20)
lblAlgor.pack(side=tk.BOTTOM)



canv = tk.Canvas(master=window, width=100, height=100)


frmButton.grid(row=0, column=0, sticky="ns")
canv.grid(row=0, column=1, sticky="nsew")
canv.bind("<Button-1>", solve)


window.mainloop()