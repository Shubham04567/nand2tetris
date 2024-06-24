class JackTokenizer:
    def __init__(self,file):
        
        self.f=open(file,"r")
        self.current_line=None
        self.current_token=None
        self.keywordSet = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
        self.symbolSet = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
        self.lista=[]        
        self.li=[]
        self.counter=0
        
    def hasMoreLine(self):
        ptr=self.f.tell()
        a=self.f.readline() != ''
        self.f.seek(ptr)
        return  a    
    
    def _advance(self):
        line=self.f.readline().rstrip("\n").lstrip("\t")
        while line.startswith("//") or len(line) == 0:
            if self.hasMoreLine():
                line = self.f.readline().strip() 
            else:
                break
            
        ki=line.find("//")
        if ki!=-1:
            line=line[:ki]
            line=line.rstrip()
        if line.startswith("/**"):
            if line.find("*/")==-1:
                found=True
                while line.find("*/")==-1:
                    a=self.f.tell()
                    linesread=self.f.read()
                    self.f.seek(a)
                    if len(linesread)>0:
                        line=self.f.readline().rstrip("\n")
                    else:
                        print("Invalid Syntax")
                        found=False
                        break
                if line.find("*/")!=-1:
                    line=self.f.readline()
            else:
                line=self.f.readline().rstrip("\n")
        self.current_line=line
        self._split(self.current_line)
        
    def _split(self,gh):
        b=gh.find("\"")
        if b==-1:
            self.splitting(gh)
        else:
            ab=gh[:b]      
            self.splitting(ab)
            cc1=gh[b+1:]
            r=cc1.find("\"")  
            strring=cc1[:r]
            self.li.append(strring) 
            self.lista.append(strring) 
            ba=cc1[r+1:].rstrip()
            self.splitting(ba)
            
    def splitting(self,fg):
        cc=fg.split()
        for i in range(len(cc)):
            if cc[i].isalpha()==True:
                self.lista.append(cc[i])
            elif cc[i].isdigit()==True:
                self.lista.append(cc[i])
            elif(len(cc[i])==1):
                if cc[i] in self.symbolSet:
                    self.lista.append(cc[i])
                    
            else:
                while len(cc[i]) != 0:
                    found_symbol = False
                    for h in cc[i]:
                        if h in self.symbolSet:
                            r = cc[i].find(h)
                            if r==0:
                                self.lista.append(cc[i][r:r+1])
                                cc[i] = cc[i][r+1:]
                                found_symbol = True
                                break  
                            else:
                                self.lista.append(cc[i][:r])
                                self.lista.append(cc[i][r:r+1])
                                cc[i] = cc[i][r+1:]
                                found_symbol = True
                                break
                    
                    if not found_symbol:
                        self.lista.append(cc[i])
                        break
                    
    def hasMoreTocken(self):
        if self.counter < len(self.lista):
            return True
        else:
            return False
    def advance(self):
        self.current_token=self.lista[self.counter]
        self.counter+=1
    
    def tokenType(self):
        
        if self.current_token in self.keywordSet:
            return "KEYWORD"
        elif self.current_token in self.symbolSet:
            return "SYMBOL"
        elif self.current_token.isdigit()==True:
            return "INT_CONST"
        elif self.current_token in self.li:
            return "STRING_CONST"
        else:
            return "IDENTIFIER"
        
    def keyWord(self):
        tocken=self.current_token
        if self.tokenType()=="KEYWORD":
            if tocken=="class":
                return "CLASS"
            elif tocken=="method":
                return "METHOD"
            elif tocken=="function":
                return "FUNCTION"
            elif tocken=="constructor":
                return "CONSTRUCTOR"
            elif tocken=="int":
                return "INT"
            elif tocken=="boolean":
                return "BOOLEAN"
            elif tocken=="char":
                return "CHAR"
            elif tocken=="void":
                return "VOID"
            elif tocken=="var":
                return "VAR"
            elif tocken=="static":
                return "STATIC"
            elif tocken=="field":
                return "FIELD"
            elif tocken=="let":
                return "LET"
            elif tocken=="do":
                return "DO"
            elif tocken=="if":
                return "IF"
            elif tocken=="else":
                return "ELSE"
            elif tocken=="while":
                return "WHILE"
            elif tocken=="return":
                return "RETURN"
            elif tocken=="true":
                return "TRUE"
            elif tocken=="false":
                return "FALSE"
            elif tocken=="this":
                return "THIS"
            elif tocken=="null":
                return "NULL"
    
    def symbol(self):
        if self.tokenType()=="SYMBOL":
            return self.current_token
    
    def identifier(self):
        if self.tokenType()=="IDENTIFIER":
            return self.current_token

    def intVal(self):
        if self.tokenType()=="INT_CONST":
            return self.current_token
    
    def stringVal(self):
        if self.tokenType()=="STRING_CONST":
            return self.current_token