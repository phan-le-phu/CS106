import tkinter as tk
import noName
from queue import PriorityQueue

flag = 'run'

def dijkstra(listofEdges, listofVertexes, window):
    global flag
    var = tk.IntVar()

    def run():
        global flag
        var.set(10)
        flag = 'run'

    def next():
        global flag
        var.set(10)
        flag = 'next'

    window1 = tk.Tk()
    window1.title("Dijkstra")
    window1.rowconfigure(1, minsize=20, weight=1)
    window1.columnconfigure(1, minsize=900, weight=1)

    frmText = tk.Frame(master=window1, relief=tk.SUNKEN, borderwidth=5)
    width = None
    lblStep1 = tk.Label(master=frmText, text="Bước 1:\n\tg(a) = 0\n\tpre(a)=None\n\tOpen = {a}\n\tClose = {}", anchor='w', justify=tk.LEFT, bg="white", width=width)
    lblStep1.pack(fill=tk.X)
    lblStep2 = tk.Label(master=frmText, text="Bước 2: while open # {} do:", bg="white", width=width, anchor='w')
    lblStep2.pack(fill=tk.X)
    lblStep21 = tk.Label(master=frmText, text="\t2.1: Chọn x thuộc open sao cho g(x) nhỏ nhất", bg="white", width=width, anchor='w')
    lblStep21.pack(fill=tk.X)
    lblStep22 = tk.Label(master=frmText, text="\t2.2: Chuyển x tử Open sang Close", bg="white", width=width, anchor='w')
    lblStep22.pack(fill=tk.X)
    lblStep23 = tk.Label(master=frmText, text="\t2.3: Xác định các đỉnh kế của x", bg="white", width=width, anchor='w')
    lblStep23.pack(fill=tk.X)
    lblStep23TH1 = tk.Label(master=frmText, text="\tTH1: y không thuộc Open và Close", bg="white", width=width, anchor='w')
    lblStep23TH1.pack(fill=tk.X)
    lblStep23TH11 = tk.Label(master=frmText, text="\t\tg(y) = g(x) + w(x,y)\n\t\tpre(y) = x\n\t\t Lưu lại y trong Open", justify=tk.LEFT, bg="white", width=width, anchor='w')
    lblStep23TH11.pack(fill=tk.X)
    lblStep23TH2 = tk.Label(master=frmText, text="\tTH2: y thuộc Open", bg="white", width=width, anchor='w')
    lblStep23TH2.pack(fill=tk.X)
    lblStep23TH21 = tk.Label(master=frmText, text="\tif g(x) + w(x,y) < g(y) then", bg="white", width=width, anchor='w')
    lblStep23TH21.pack(fill=tk.X)
    lblStep23TH22 = tk.Label(master=frmText, text="\t\tg(y) = g(x) + w(x,y)\n\t\tpre(y) = x", justify=tk.LEFT, bg="white", width=width, anchor='w')
    lblStep23TH22.pack(fill=tk.X)
    lblStep3 = tk.Label(master=frmText, text="Bước 3: Kết luận", justify=tk.LEFT, bg="white", width=width, anchor='w')
    lblStep3.pack(fill=tk.X)


    btnRun = tk.Button(master=window1, text="Run", width=20, command=run)
    btnRun.grid(row=1, column=0)

    btnNext = tk.Button(master=window1, text="Next", width=20, command=next)
    btnNext.grid(row=1, column=1)



    canv = tk.Canvas(master=window1)


    frmText.grid(row=0, column=0, sticky="ns")
    canv.grid(row=0, column=1, sticky="nsew")

    noName.drawShape(listofEdges, listofVertexes, canv)

    scrollbar = tk.Scrollbar(frmText)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frmText)
    listbox.pack(fill=tk.X)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    #-------------------------------------------

    window.wait_variable(var)

    openSet = {}
    openSet[0] = 0
    closeSet = []
    cameFrome = {}
    cameFrome[0] = None
    costSoFar = {}
    costSoFar[0] = 0
    text = "Khởi tạo:\ng(0) = 0\npre(0) = None\nOpen = {0}\nClose = {} "
    noName.doEachStep(lblStep1, text, listbox, window, flag, var)
    while openSet != {}:
        text = "Các đỉnh trong tập O:\n" + ', '.join(str(vertex) for vertex in openSet) +\
            "\n=> O khác rỗng."
        noName.doEachStep(lblStep2, text, listbox, window, flag, var)
        currentVertex = min(openSet, key=openSet.get)
        noName.drawVertex(listofVertexes[currentVertex], canv, "#11fc05")
        text = "Chọn đỉnh {0} có g({0}) = {1} nhỏ nhất.".format(currentVertex, openSet.pop(currentVertex))
        noName.doEachStep(lblStep21, text, listbox, window, flag, var)
        closeSet.append(currentVertex)
        text = "Chuyển đỉnh {} sang tập Close.".format(currentVertex) +\
            "\n=>Các đỉnh trong tập Close:" +\
            "\n" + ','.join(str(vertex) for vertex in closeSet)
        noName.doEachStep(lblStep22, text, listbox, window, flag, var)
        text = "Các đỉnh kề với đỉnh {}:".format(currentVertex) +\
            "\n" + ','.join(str(vertex) for vertex in listofVertexes[currentVertex].neighbors)
        noName.doEachStep(lblStep23, text, listbox, window, flag, var)
        for nextVertex, indexEdge in listofVertexes[currentVertex].neighbors.items():
            idItems = noName.drawVertex(listofVertexes[nextVertex], canv, "#0ae6fa")
            idItems = idItems + noName.drawEdge(listofEdges[indexEdge], canv, "#0ae6fa")
            text = "Xét đỉnh kề {}.".format(nextVertex)
            noName.doEachStep(lblStep23TH1, text, listbox, window, flag, var)
            newCost = costSoFar[currentVertex] + listofEdges[indexEdge].weight
            if nextVertex in closeSet:
                text = "Đỉnh {} trong tập Close!!".format(nextVertex)
                noName.doEachStep(lblStep23, text, listbox, window, flag, var)
            elif nextVertex not in openSet:
                openSet[nextVertex] = newCost
                cameFrome[nextVertex] = currentVertex
                costSoFar[nextVertex] = newCost
                noName.drawVertex(listofVertexes[nextVertex], canv, "#ffb700")
                noName.drawEdge(listofEdges[indexEdge], canv, "#ffb700")
                text = "Đỉnh {} không thuộc Open và Close!!".format(nextVertex) +\
                "\n=>Thực hiện:\ng({1}) = g({0}) + w({0},{1}) = {2} + {3} = {4}".format(currentVertex, nextVertex,
                                                                            costSoFar[currentVertex],
                                                                            listofEdges[indexEdge].weight,
                                                                            newCost) +\
                "\npre({}) = {}".format(nextVertex, currentVertex)
                "\nLưu đỉnh {} vào Open".format(nextVertex)
                noName.doEachStep(lblStep23TH11, text, listbox, window, flag, var)
                continue
            elif nextVertex in openSet:
                text = "Đỉnh {} thuộc Open!!".format(nextVertex)
                noName.doEachStep(lblStep23TH2, text, listbox, window, flag, var)
                text = "Kiểm tra:" + \
                       "\ng({0}) + w({0},{1}) ? g({1}) hay {2} + {3} ? {4}".format(currentVertex, nextVertex,
                                                                                   costSoFar[currentVertex],
                                                                                   listofEdges[indexEdge].weight,
                                                                                   costSoFar[nextVertex])
                noName.doEachStep(lblStep23TH21, text, listbox, window, flag, var)
                if newCost < costSoFar[nextVertex]:
                    text = "Tìm được đường đi ngắn hơn hiện tại!!".format(nextVertex)
                    noName.doEachStep(lblStep23TH21, text, listbox, window, flag, var)
                    text = "=>Thực hiện" + \
                           "\ng({1}) = g({0}) + w({0},{1}) = {2} + {3} = {4}".format(currentVertex,
                                                                                                   nextVertex,
                                                                                                   costSoFar[
                                                                                                       currentVertex],
                                                                                                   listofEdges[
                                                                                                       indexEdge].weight,
                                                                                                   newCost) + \
                           "\npre({}) = {}".format(nextVertex, currentVertex)
                    noName.doEachStep(lblStep23TH22, text, listbox, window, flag, var)
                    openSet[nextVertex] = newCost
                    cameFrome[nextVertex] = currentVertex
                    costSoFar[nextVertex] = newCost
                    for vertex, anotherIndexEdge in listofVertexes[nextVertex].neighbors.items():
                        if vertex != currentVertex:
                            noName.drawEdge(listofEdges[anotherIndexEdge], canv, "black")
                    noName.drawVertex(listofVertexes[nextVertex], canv, "#ffb700")
                    noName.drawEdge(listofEdges[indexEdge], canv, "#ffb700")
                    continue
            noName.undoColor(idItems, canv)
        noName.drawVertex(listofVertexes[currentVertex], canv, "#ffb700")
    text = "Các đỉnh trong tập O:\n" + '...' + "\n=> O rỗng."
    noName.doEachStep(lblStep2, text, listbox, window, flag, var)
    textRoute = ''
    for vertex in range(1, len(listofVertexes)):
        listResult = []
        textRoute = textRoute + "Đỉnh {} : ".format(vertex)
        listResult.append(vertex)
        currentVertex = vertex
        while currentVertex != None:
            currentVertex = cameFrome[currentVertex]
            listResult.append(currentVertex)
        listResult.reverse()
        textRoute = textRoute + '0'
        for j in listResult[2:]:
            textRoute = textRoute + "-->" + str(j)
        textRoute = textRoute + "\n"
    text = "Kết quả:\n" + textRoute
    noName.doEachStep(lblStep3, text, listbox, window, flag, var)

    window1.mainloop()


