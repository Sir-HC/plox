import sys

class Plox():
    pass

def runFile(path):
    bytes = b''
    with open(path, 'rb') as bf:
        bytes = bf.readall()
    run(bytes.decode(sys.getdefaultencoding()))
    
def runPrompt():
    
    while True:
        print("> ", end= '')
        line = input()
        if line == "":
            break
        run(line)

def run(string):
    pass

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        quit()
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()

