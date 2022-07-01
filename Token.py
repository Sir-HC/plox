from Constants.TokenType import TokenType

class Token:
    def __init__(self, typ: TokenType, lexeme: str, literal, line: int):
        self.typ = typ
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        
    def __str__(self):
        return f"{self.typ} {self.lexeme} {self.literal}"
      