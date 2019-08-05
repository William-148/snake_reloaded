"""def lineReader(line):
    ## Return No. game and game's time in a tuple
    game = ""
    time = ""
    state = 0
    ## noGame - coma - time
    for char in line:
        if state == 0:
            if char == ",":
                state = 1
            elif char != "\n" and char != " ":                
                game += char
        
        elif state == 1:
            if char != "\n" and char != "," and char != " ":                
                time += char
    
    return (game, time )
"""

def delete_space(text):
    new = ""
    for char in text:        
        if char != "\n":
            new += char
    return new

def read(file_name,data_list):
    try:
        f = open(file_name, "r")
        firstLine = True
        for line in f :
            if not firstLine:
                data_list.addEnd(delete_space(line))
            firstLine = False
            
    except FileNotFoundError:
        print("Error: archivo no encontrado.")
    finally:
        f.close()