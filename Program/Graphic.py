
import subprocess
from os import startfile

path = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe"
extension = "-Tjpg"
extension1 = "-o" 

def graph( list_user, file_name):
    txt = file_name+".txt"
    img = file_name+".jpg"

    try:
        f = open(txt, "w")
        f.write("digraph G {\n")
        f.write("rankdir=LR;\n")
        f.write("node [shape=record];\n")
        ##Create nodes here
        create_nodes(f,list_user)

        f.write("}")
        f.close()

        command = [path, extension,txt, extension1, img]
        subprocess.call(command)

        startfile(img)

        return 1
    except :        
        print("Error: .")
        return 0

def create_nodes(f, list_user):

     
    if list_user.size > 0:
        aux = list_user.head.next_node
        count = 1

        f.write("node0 [shape=record, label=\"{ | "+list_user.head.data+" | }\"]\n")

        while aux is not list_user.head:
            f.write("node"+str(count)+" [shape=record, label=\"{ | "+aux.data+" |  }\"]\n")
            aux = aux.next_node
            count += 1
        for i in range(list_user.size):
            
            if i == list_user.size -1:
                f.write("node"+str(i)+" -> node0\n node0 -> node"+str(i)+"\n")
            else:
                f.write("node"+str(i)+" -> node"+str(i+1)+"\n node"+str(i+1)+" -> node"+str(i)+"\n")

            #file.write("node3 [shape=record, label="{ a | b | c }"]")