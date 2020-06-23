import tkinter as tk
import noName


flag = 'run'

def appendEges2PQ(pqSet, tSet, vertex, listofEdges, listofVertexes, canvasName):
    for key, indexEdge in listofVertexes[vertex].neighbors.items():
        if indexEdge in tSet or indexEdge in pqSet:
            continue
        if pqSet == []:
            pqSet.append(indexEdge)
            noName.drawEdge(listofEdges[indexEdge], canvasName, color="#b8aeae")
        else:
            i = 0
            while i != len(pqSet):
                if listofEdges[indexEdge].weight <= listofEdges[pqSet[i]].weight:
                    break
                i = i + 1
            pqSet.insert(i, indexEdge)
            noName.drawEdge(listofEdges[indexEdge], canvasName, color="#b8aeae")



def prim(listofEdges, listofVertexes, window):

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
    window1.title("Prim")
    window1.rowconfigure(0, minsize=500, weight=1)
    window1.columnconfigure(1, minsize=900, weight=1)

    frmText = tk.Frame(master=window1, relief=tk.SUNKEN, borderwidth=5)
    frmText.grid(row=0, column=0, sticky="ns")

    lblStep1 = tk.Label(master=frmText, text="Bước 1: Khởi tạo O = {s}", anchor='w', bg="white", justify=tk.LEFT)
    lblStep1.pack(fill=tk.X)

    lblStep11 = tk.Label(master=frmText, text="\tThêm các cạnh có chứa đỉnh s vào PQ ", anchor='w', bg="white")
    lblStep11.pack(fill=tk.X)

    lblStep2 = tk.Label(master=frmText, text="Bước 2: While PQ != empty", anchor='w', bg="white")
    lblStep2.pack(fil=tk.X)

    lblStep21 = tk.Label(master=frmText, text="\t2.1 If (u, v) = PQ.getMin() không tạo chu trình:", anchor='w', bg="white")
    lblStep21.pack(fil=tk.X)

    lblStep211 = tk.Label(master=frmText, text="\t\tThêm v vào O và "
                                               "các cạnh liên kết với v vào PQ ", anchor='w', bg="white")
    lblStep211.pack(fil=tk.X)

    lblStep3 = tk.Label(master=frmText, text="Bước 3: Kết luận", anchor='w', bg="white")
    lblStep3.pack(fil=tk.X)

    btnRun = tk.Button(master=window1, text="Run", width=20, command=run)
    btnRun.grid(row=1, column=0)

    btnNext = tk.Button(master=window1, text="Next", width=20, command=next)
    btnNext.grid(row=1, column=1)



    scrollbar = tk.Scrollbar(frmText)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frmText)
    listbox.pack(fill=tk.BOTH, expand=1)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    canv = tk.Canvas(master=window1)
    canv.grid(row=0, column=1, sticky="nesw")
    noName.drawShape(listofEdges, listofVertexes, canv)



    #----------------------------------------------------

    window.wait_variable(var)

    n = len(listofVertexes)
    oSet = []
    oSet.append(0)
    pqSet = []
    tSet = []
    text = "Khởi tạo: O = {0}"
    noName.drawVertex(listofVertexes[0], canv, color="#f7bb05")
    noName.doEachStep(lblStep1, text, listbox, window, flag, var)
    appendEges2PQ(pqSet, tSet, 0, listofEdges, listofVertexes, canv)
    text = "=>Các cạnh trong PQ:\n" + noName.convert2Text(pqSet, listofEdges)
    noName.doEachStep(lblStep11, text, listbox, window, flag, var)
    while pqSet != []:
        text = "Các cạnh trong PQ:\n" + noName.convert2Text(pqSet, listofEdges) +\
            "\n=> PQ khác rỗng."
        indexEdge = pqSet.pop(0)
        noName.doEachStep(lblStep2, text, listbox, window, flag, var)
        idItems = noName.drawVertexAndEdge(listofEdges[indexEdge], canv, color="#3cf005")
        text = "Lấy cạnh nhỏ nhất " + str(listofEdges[indexEdge].point1.nameOfNode) +\
               str(listofEdges[indexEdge].point2.nameOfNode) + "(w=" +\
            str(listofEdges[indexEdge].weight) + ") khỏi PQ"
        noName.doEachStep(lblStep21, text, listbox, window, flag, var)
        if listofEdges[indexEdge].point1.nameOfNode in oSet \
                and listofEdges[indexEdge].point2.nameOfNode in oSet:
            text = "Tạo chu trình!!"
            noName.doEachStep(lblStep21, text, listbox, window, flag, var)
            noName.undoColor(idItems, canv)
            noName.drawEdge(listofEdges[indexEdge], canv, color="black")
            continue
        else:
            currentVertex = listofEdges[indexEdge].point1.nameOfNode if listofEdges[indexEdge].point1.nameOfNode \
                not in oSet else listofEdges[indexEdge].point2.nameOfNode
            tSet.append(indexEdge)
            oSet.append(currentVertex)
            noName.drawVertexAndEdge(listofEdges[indexEdge], canv, color="#f7bb05")
            appendEges2PQ(pqSet, tSet, currentVertex, listofEdges, listofVertexes, canv)
            text = "Không tạo chu trình!\n=>Thêm đỉnh {} vào tập O".format(currentVertex) + \
                "\n=>Các đỉnh trong tập O:\n" + ','.join(str(vertex) for vertex in oSet) +\
                "\nThêm các cạnh kề với đỉnh {} vào PQ".format(currentVertex) +\
                "\n=>Các phần tử trong PQ:\n" + noName.convert2Text(pqSet, listofEdges)
            noName.doEachStep(lblStep211, text, listbox, window, flag, var)
    text = "Các cạnh trong PQ:\n...\n=> PQ  rỗng."
    noName.doEachStep(lblStep2, text, listbox, window, flag, var)
    if len(oSet) == n:
        text = "Các cạnh trong cây khung nhỏ nhất:\n" + noName.convert2Text(tSet, listofEdges) +\
            "\nTrong số của cây khung nhỏ nhất : " + str(noName.getWeight(tSet, listofEdges))
        noName.doEachStep(lblStep3, text, listbox, window, flag, var)
    else:
        text = "Không tìm được cây khung nhỏ nhất\n.Do đồ thị không liên thông!"
        noName.doEachStep(lblStep3, text, listbox, window, flag, var)

    window1.mainloop()







