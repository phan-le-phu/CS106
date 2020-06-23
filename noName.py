import tkinter as tk


def waitthere(time, window):
    var = tk.IntVar()
    window.after(time, var.set, 1)
    print("waiting...")
    window.wait_variable(var)

def drawShape(listofEdges, listofVertexes, canvasName):
    for edge in listofEdges:
        drawEdge(edge, canvasName, "black")
    for vertex in listofVertexes:
        drawVertex(vertex, canvasName, "white")



def drawEdge(edge, canvasName, color):
    x1 = edge.point1.x
    y1 = edge.point1.y
    x2 = edge.point2.x
    y2 = edge.point2.y

    k = 10 * (x1 - x2) / (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2))
    x_1 = x1 - k
    x_2 = x2 + k
    a = (y2 - y1) / (x2 - x1)
    b = y1 - x1 * a
    y_1 = x_1 * a + b
    y_2 = x_2 * a + b

    idItems = []
    idItem = canvasName.create_line(x_1, y_1, x_2, y_2, width=5, fill=color, smooth=True)
    idItems.append(idItem)
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    idItem = canvasName.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="yellow")
    idItems.append(idItem)
    idItem = canvasName.create_text(x, y, text=edge.weight)
    idItems.append(idItem)
    return idItems

# ham to mau dinh
def drawVertex(vertex, canvasName, color):
    idItems = []
    x = vertex.x
    y = vertex.y
    x0 = x - 10
    y0 = y - 10
    x1 = x + 10
    y1 = y + 10
    idItem = canvasName.create_oval(x0, y0, x1, y1, fill=color)
    idItems.append(idItem)
    canvasName.tag_raise(idItem)
    idItem = canvasName.create_text(x, y, text=str(vertex.nameOfNode))
    idItems.append(idItem)
    return idItems

# ham to mau dinh va canh
def drawVertexAndEdge(edge, canvasName, color):
    idItems = []
    idItems = idItems + drawEdge(edge, canvasName, color)
    idItems = idItems + drawVertex(edge.point1, canvasName, color)
    idItems = idItems + drawVertex(edge.point2, canvasName, color)
    return idItems

def undoColor(idItems, canvasName):
    for item in idItems:
        canvasName.delete(item)

def doEachStep(nameLabel, text, listbox, window, flag, var):
    nameLabel["bg"] = "yellow"
    for line in text.split("\n"):
        listbox.insert(tk.END, line)
    listbox.insert(tk.END, '------------------------')
    listbox.see("end")
    print(flag)
    if flag == 'run':
        waitthere(1000, window)
    elif flag == 'next':
        print('i am here')
        window.wait_variable(var)
    nameLabel["bg"] = "white"


def convert2Text(listIndexEdge, listofEdges):
    text = ''
    for i, indexEdge in enumerate(listIndexEdge):
        text = text + str(listofEdges[indexEdge].point1.nameOfNode) +\
               str(listofEdges[indexEdge].point2.nameOfNode) + "(w=" +\
            str(listofEdges[indexEdge].weight) + "),"
        if (i + 1) % 3 == 0:
            text += "\n"
    return  text[0:-1]

def getWeight(listIndexEdge, listofEdges):
    weight = 0
    for indexEdge in listIndexEdge:
        weight += listofEdges[indexEdge].weight
    return weight



