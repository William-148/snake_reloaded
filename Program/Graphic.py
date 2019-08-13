
import subprocess
from os import startfile

path = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe"
extension = "-Tjpg"
extension1 = "-o" 
circular_list = 0
double_list = 1
queue_list = 2
stack_list = 3


def graph( list_to_graph, file_name, type_list):
    txt = file_name+".txt"
    img = file_name+".jpg"

    try:
        f = open(txt, "w")
        f.write("digraph G {\n")
        f.write("rankdir=LR;\n")
        f.write("node [shape=record];\n")
        ##Create nodes here
        
        if type_list == 0:
            circular_list_nodes(f,list_to_graph)
        elif type_list == 1:
            double_list_nodes(f,list_to_graph)
        elif type_list == 2:
            queue_list_nodes(f,list_to_graph)
        elif type_list == 3:
            stack_list_nodes(f,list_to_graph)


        f.write("}")
        f.close()

        command = [path, extension,txt, extension1, img]
        subprocess.call(command)

        startfile(img)

        return 1
    except :        
        print("Error: .")
        f.close()
        return 0

def circular_list_nodes(f, list_user):

     
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
def double_list_nodes(f, snake):
    print("snake")

def queue_list_nodes(f, score_history):
    if score_history.size > 0:
        aux = score_history.head
        count = 0

        #f.write("node0 [shape=record, label=\"{ | "+list_user.head.data+" | }\"]\n")

        while aux is not None:
            f.write("node"+str(count)+" [shape=record, label=\"{ ("+aux.data[0]+", "+str(aux.data[1])+") |  }\"]\n")
            aux = aux.next_node
            count += 1

        f.write("node"+str(count)+" [shape=record, label=\"{ null }\"]\n")    

        for i in range(score_history.size):            
            f.write("node"+str(i)+" -> node"+str(i+1)+"\n")
    else:
        f.write("node0 [shape=record, label=\"{ null }\"]\n")   

def stack_list_nodes(f, snake):
    print("snake")