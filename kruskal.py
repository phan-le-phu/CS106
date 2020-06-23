import tkinter as tk
import noName


flag = 'run'

def findParent(parent, i):
    if parent[i] == i:
        return i
    if parent[i] != i:
        return findParent(parent, parent[i])


def union(parent, x, y):
    xSet = findParent(parent, x)
    ySet = findParent(parent, y)
    parent[xSet] = ySet


def addEdge(parent, x, y):
    if findParent(parent, x) == findParent(parent, y):
        print("grahp will contains cycle if add edge")
        return False
    else:
        union(parent, x, y)
        print("add edge success")
        return True


def kruskal(listofEdges, listofVertexes, window):
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
    window1.title("Kruskal")
    window1.rowconfigure(0, minsize=500, weight=1)
    window1.columnconfigure(1, minsize=900, weight=1)

    frmText = tk.Frame(master=window1, relief=tk.SUNKEN, borderwidth=5)
    frmText.grid(row=0, column=0, sticky="ns")

    lblStep1 = tk.Label(master=frmText, text="Bước 1: \n\tSắp xêp các cạnh theo trọng số tăng dần vào tập G\n\t"
                                             "Khởi tạo T = {}", anchor='w', bg="white", justify=tk.LEFT)
    lblStep1.pack(fill=tk.X)

    lblStep2 = tk.Label(master=frmText, text="Bước 2: while G != {} or T đủ n - 1 phần tử (n là số đỉnh)", anchor='w', bg="white")
    lblStep2.pack(fill=tk.X)

    lblStep21 = tk.Label(master=frmText, text="\t2.1 Lấy cạnh e khỏi tập G", anchor='w', bg="white")
    lblStep21.pack(fil=tk.X)

    lblStep22 = tk.Label(master=frmText, text="\t2.2 if e không tạo chu trình then", anchor='w', bg="white")
    lblStep22.pack(fil=tk.X)

    lblStep221 = tk.Label(master=frmText, text="\t\tThêm e vào T", anchor='w', bg="white")
    lblStep221.pack(fil=tk.X)

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

    window.wait_variable(var)


    gSet = []
    tSet = []
    for indexEdge in range(len(listofEdges)):
        if gSet == []:
            gSet.append(indexEdge)
        else:
            i = 0
            while i != len(gSet):
                if listofEdges[indexEdge].weight <= listofEdges[gSet[i]].weight:
                    break
                i = i + 1
            gSet.insert(i, indexEdge)
    n = len(listofVertexes)
    g = [ i for i in range(n)]
    text = "Khởi tạo:" + "\nTập G:" + "\n" + noName.convert2Text(gSet, listofEdges)
    noName.doEachStep(lblStep1, text, listbox, window, flag, var)
    while gSet != [] and len(tSet) != (n -1):
        text = "Tập G:" + "\n" + noName.convert2Text(gSet, listofEdges) +\
            "\nSố phần tử của T = {} < n - 1 = {}".format(len(tSet), n - 1) +\
            "\nThõa mãn!"
        noName.doEachStep(lblStep2, text, listbox, window, flag, var)
        indexE = gSet.pop(0)
        idItems = noName.drawVertexAndEdge(listofEdges[indexE], canv, "#43fc05")
        text = "Lấy cạnh " + str(listofEdges[indexE].point1.nameOfNode) +\
               str(listofEdges[indexE].point2.nameOfNode) + "(w=" +\
            str(listofEdges[indexE].weight) + ") khỏi G"
        noName.doEachStep(lblStep21, text, listbox, window, flag, var)
        text = "Kiểm tra..."
        noName.doEachStep(lblStep22, text, listbox, window, flag, var)
        if addEdge(g, listofEdges[indexE].point1.nameOfNode, listofEdges[indexE].point2.nameOfNode):
            noName.drawVertexAndEdge(listofEdges[indexE], canv, "#fcc203")
            text = "Cạnh " + str(listofEdges[indexE].point1.nameOfNode) +\
               str(listofEdges[indexE].point2.nameOfNode) + "(w=" +\
            str(listofEdges[indexE].weight) + ") không tạo chu trình." +\
                "\n=> Thêm vào T"
            noName.doEachStep(lblStep221, text, listbox, window, flag, var)
            tSet.append(indexE)
            continue
        noName.undoColor(idItems, canv)
        text = "Tạo chu trình!!\n=>Không thêm vào T"
        noName.doEachStep(lblStep22, text, listbox, window, flag, var)
    if len(tSet) == (n - 1):
        text = "Dừng vòng lặp!!\nDo:" + \
               "\nSố phần tử của T = {} = n - 1 = {}".format(len(tSet), n - 1)
        noName.doEachStep(lblStep2, text, listbox, window, flag, var)
        text = "Các cạnh trong tập T:" +\
            "\n" + noName.convert2Text(tSet, listofEdges) +\
            "\nTrọng số của cây khung nhỏ nhất: " + str(noName.getWeight(tSet, listofEdges))
        noName.doEachStep(lblStep3, text, listbox, window, flag, var)
    else:
        text = "Dừng vòng lặp!!\nDo:" + \
               "Tập G rỗng."
        noName.doEachStep(lblStep2, text, listbox, window, flag, var)
        text = "Không tìm được cây khung nhỏ nhất.\nDo đồ thị không liên thông"
        noName.doEachStep(lblStep3, text, listbox, window, flag, var)



    window1.mainloop()




