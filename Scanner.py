from Constants.TokenType import TokenType as tt, TokenType
from Constants.TokenType import keywords as TokenKeyword
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
                    while not self.isAtEnd() and self.peek() != '\n': 
                        print(self.current)
                        self.advance()
                elif self.match('*'):
                    while not self.isAtEnd() and (self.peek() != '*' and self.peekNext() != '/'): 
                        self.advance()
                    # Consume final */
                    self.advance()
                    self.advance()
                else:
                    self.addToken(tt.SLASH)
            case '"': self.string()
            case _: 
                if isDigit(c):
                    self.number()
                elif isAlpha(c):
                    self.identifier()
                else:    
                    #Plox.error(self.line, "Unexpected character.")
                    print(f'{self.line} - Unexpected character - {c}')
            
    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False
        
        self.current += 1
        return True
    
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def peek(self):
        if self.isAtEnd(): return '\0'
        return self.source[self.current]
        
    def peekNext(self):
        if self.current >= len(self.source): return '\0'
        return self.source[self.current + 1]
        
    def advance(self):
        res = self.source[self.current]
        self.current += 1
        return res
        
    def number(self):
        while isDigit(self.peek()): self.advance()
        
        if self.peek() == '.' and isDigit(self.peekNext()):
            # consume .
            self.advance()
            
            while isDigit(self.peek()): self.advance()
            
        self.addToken(tt.NUMBER, float(self.source[self.start:self.current]))
    
    def identifier(self):
        while isAlphaNumeric(self.peek()): self.advance()
        self.addToken(tt.IDENTIFIER)
    
    def string(self):
        
        while self.peek() != '\"' and not self.isAtEnd():
            if self.peek() == '\n': 
                self.line += 1
            self.advance()
        
        # Fixed edge case of end terminated string
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
    
@staticmethod
def isAlpha(c):
    return ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z') or (c == '_')

@staticmethod    
def isDigit(c):
    return '0' <= c and c <= '9'

@staticmethod
def isAlphaNumeric(c):
    return isAlpha(c) or isDigit(c)