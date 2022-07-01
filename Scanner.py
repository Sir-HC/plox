from Constants.TokenType import TokenType as tt, TokenType
from Token import Token
from Plox import Plox

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    def scanTokens(self):
        # Prevent multiple executions adding additional EoF token
        if self.isAtEnd():
            return self.tokens
        
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken();
        
        self.tokens.append(Token(tt.EOF, "", None, self.line))
        return self.tokens
        
    def isAtEnd(self):
        return self.current >= len(self.source)
        
    def scanToken(self):
        c = self.advance()
        match c:
            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1
            case '(': self.addToken(tt.LEFT_PAREN)
            case ')': self.addToken(tt.RIGHT_PAREN)
            case '{': self.addToken(tt.LEFT_BRACE)
            case '}': self.addToken(tt.RIGHT_BRACE)
            case ',': self.addToken(tt.COMMA)
            case '.': self.addToken(tt.DOT)
            case '-': self.addToken(tt.MINUS)
            case '+': self.addToken(tt.PLUS)
            case ';': self.addToken(tt.SEMICOLON)
            case '*': self.addToken(tt.STAR)
            case '!':
                self.addToken(tt.BANG_EQUAL if self.match('=') else tt.BANG)
            case '=':
                self.addToken(tt.EQUAL_EQUAL if self.match('=') else tt.EQUAL)
            case '<':
                self.addToken(tt.LESS_EQUAL if self.match('=') else tt.LESS)
            case '>':
                self.addToken(tt.GREATER_EQUAL if self.match('=') else tt.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.isAtEnd(): self.advance()
                else:
                    self.addToken(tt.SLASH)
            case '"': self.string()
            case _: 
                if self.isDigit(c):
                    self.number()
                else:    
                    #Plox.error(self.line, "Unexpected character.")
                    print(f'{self.line} - Unexpected character - {c}')
            
    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False
        
        self.current += 1
        return True
        
    def peek(self):
        if self.isAtEnd(): return '\0'
        return self.source[self.current]
        
    def peekNext(self):
        if self.current + 1 > len(self.source): return '\0'
        
        return self.source[self.current + 1]
        
    def advance(self):
        res = self.source[self.current] 
        self.current += 1
        return res
    
    def isDigit(self, c):
        return '0' <= c and c <= '9'
        
    def number(self):
        while self.isDigit(self.peek()): self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            # consume .
            self.advance()
            
            while self.isDigit(self.peek()): self.advance()
            
        self.addToken(tt.NUMBER, float(self.source[self.start:self.current]))
    
    def string(self):
        while self.peek() != '\"' and not self.isAtEnd():
            if self.peek() == '\n': self.line += 1
            self.advance()
            
        if self.isAtEnd():
            #Plox.error(self.line, "Unterminated string.")
            print(f'{self.line} - Unterminated string.')
            
        # Consume "
        self.advance()
        
        value = self.source[self.start + 1: self.current - 1]
        self.addToken(tt.STRING, value)
    
    def addToken(self, _type: TokenType, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(_type, text, literal, self.line))