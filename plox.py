import sys
from Constants.TokenType import TokenType

class Plox:
    def __init__(self, args):
        self.hadError = False
        if len(args) > 2:
            print("Usage: plox [script]")
            quit()
        elif len(args) == 2:
            self.runFile(args[1])
        else:
            self.runPrompt()

    def runFile(self, path):
        bytes = b''
        with open(path, 'rb') as bf:
            bytes = bf.read()
        print(f"Running with encoding: {sys.getdefaultencoding()}")
        self.run(bytes.decode(sys.getdefaultencoding()))
        if self.hadError:
            quit()
        
    def runPrompt(self):
        
        while True:
            print("> ", end= '')
            line = input()
            if line == "":
                break
            self.run(line)
            self.hadError = False

    def run(self, string):
        print(string)

    def error(self, line_no, msg):
        report(line_no, "", msg)
        
    def report(self, line_no, where, msg):
        print(f"[line {line_no}] Error {where}: {msg}", file=sys.stderr)
        self.hadError = True
    

if __name__ == "__main__":
    Plox(sys.argv)

