class CompilationEngine:
    def __init__(self,output1,output2):
        self.k=open(output1,"r")
        
        self.k1=open(output2,"w")
        self.o=self.k.readline()
        self.line=None
        self.tabshift="   "
        
    def compileClass(self):
        self.k1.write("<class>\n")
        self.line=self.k.readline()
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        
        while "static" in self.line or "field" in self.line:
            self.compileClassVarDec(self.line)
            
        while "function" in self.line or "method" in self.line or "constructor" in self.line:
            self.compileSubroutine(self.line)
        self.k1.write(f"{self.tabshift}{self.line}")
        self.k1.write("</class>\n")
            
                
    def compileClassVarDec(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<classVarDec>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run=True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            if ";" in self.line:
                self.k1.write(f"{a}</classVarDec>\n")
                self.tabshift=a
                break
            self.line=self.k.readline()
        self.line=self.k.readline()
                
        
    def compileSubroutine(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<subroutineDec>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run=True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            if "(" in self.line:
                self.line=self.k.readline()
                self.compileParameterList(self.line)
                self.tabshift=a
                break
            self.line=self.k.readline() 
        self.k1.write(f"{a}</subroutineDec>\n")
            
    
    def compileParameterList(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<parameterList>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run=True
        while(run):
            if ")" in self.line:
                self.tabshift=a
                break
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
        self.k1.write(f"{a}</parameterList>\n")
        self.k1.write(f"{a}{self.line}")
        self.line=self.k.readline()
        self.compileSubroutineBody(self.line)
        
    
    def compileSubroutineBody(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<subroutineBody>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        while "var" in self.line:
            self.compileVarDec(self.line)
        while "let" in self.line or "while" in self.line or "if" in self.line or "do" in self.line or "return" in self.line:
            self.compileStatement(self.line)
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        self.tabshift=a
        self.k1.write(f"{a}</subroutineBody>\n")
        
    
    def compileStatement(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<statements>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run=True
        while run:
            if " let " in self.line:
                self.compileLet(self.line)
            elif " while " in self.line:
                self.compileWhile(self.line)
            elif " if " in self.line:
                self.compileIf(self.line)
            elif " do " in self.line:
                self.compileDo(self.line)
            elif " return " in self.line:
                self.compileReturn(self.line)
            else:
                break
        self.k1.write(f"{a}</statements>\n")
        if "}" in self.line:
            self.tabshift=a
            pass
        else:
            self.tabshift=a
            self.line=self.k.readline()
        
        
    def compileVarDec(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<varDec>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            if ";" in self.line:
                self.tabshift=a
                self.k1.write(f"{a}</varDec>\n")
                break
            self.line=self.k.readline()
        self.line=self.k.readline()
    
    
    def compileLet(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<letStatement>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
            if "[" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
            if "=" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
            
            if ";" in self.line:
                self.tabshift=a
                break
        self.k1.write(f"{self.tabshift}{self.line}")
        self.k1.write(f"{a}</letStatement>\n")
        self.line=self.k.readline()
        
        
    def compileWhile(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<whileStatement>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
            if "{" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileStatement(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.tabshift=a
                break
        self.k1.write(f"{a}</whileStatement>\n")
            
    def compileIf(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<ifStatement>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
            if "{" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileStatement(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.tabshift=a
                break
            
        if "else" in self.line:
            a=self.tabshift
            self.tabshift=self.tabshift+"   "
            s=run
            while s:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                if "(" in self.line:
                    self.k1.write(f"{self.line}")
                    self.line=self.k.readline()
                    self.compileExpression(self.line)
                    self.k1.write(f"{self.line}")
                    self.line=self.k.readline()
                if "{" in self.line:
                    self.k1.write(f"{self.tabshift}{self.line}")
                    self.line=self.k.readline()
                    self.compileStatement(self.line)
                    self.k1.write(f"{self.tabshift}{self.line}")
                    self.line=self.k.readline()
                    self.tabshift=a
                    break
        self.k1.write(f"{a}</ifStatement>\n")

    def compileDo(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<doStatement>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpressionlist(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.tabshift=a
                break
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
        self.k1.write(f"{a}</doStatement>\n")
        
    def compileReturn(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<returnStatement>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        self.k1.write(f"{self.tabshift}{self.line}")
        self.line=self.k.readline()
        run =True
        while run:
            if ";" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.tabshift=a
                break
            self.compileExpression(self.line)
            
        self.k1.write(f"{a}</returnStatement>\n")
        
    def compileExpression(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<expression>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            self.compileTerm(self.line)
            
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                
            self.sim=self.line.split(">")[1].split("<")[0].strip(" ")
            h=["+","-","=","&lt;","&gt;","&amp;","*","/","|"] 
            for i in h:
                if self.sim == i:
                    self.k1.write(f"{self.tabshift}{self.line}")
                    self.line=self.k.readline()
                    self.compileTerm(self.line)
                    
                
            if ";" in self.line and "&" not in self.line:
                self.k1.write(f"{a}</expression>\n")
                self.tabshift=a
                break
            if "]" in self.line:
                self.k1.write(f"{a}</expression>\n")
                self.tabshift=a
                break
            if "," in self.line:
                self.k1.write(f"{a}</expression>\n")
                self.tabshift=a
                break
            else:
                self.k1.write(f"{a}</expression>\n")
                self.tabshift=a
                break
                
    def compileTerm(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<term>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.k1.write(f"{a}</term>\n")
                self.tabshift=a
                break
            rr=self.line
            self.k1.write(f"{self.tabshift}{self.line}")
            self.line=self.k.readline()
            
            if "." in self.line:
                    self.k1.write(f"{self.tabshift}{self.line}")
                    self.line=self.k.readline()
                    self.k1.write(f"{self.tabshift}{self.line}")
                    self.line=self.k.readline()
                    if "(" in self.line:
                        self.k1.write(f"{self.tabshift}{self.line}")
                        self.line=self.k.readline()
                        self.compileExpressionlist(self.line)
                        self.k1.write(f"{self.tabshift}{self.line}")
                        self.line=self.k.readline()
                        
            if "~" in rr and "(" in self.line:
                self.compileTerm(self.line)
                self.k1.write(f"{a}</term>\n")
                break
            if "(" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                count=self.compileExpressionlist(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.tabshift=a
                break
            
            if "[" in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
            if "-" in rr:
                self.compileTerm(self.line)
            if "~" in rr:
                self.compileTerm(self.line)
                self.k1.write(f"{a}</term>\n")
                self.tabshift=a
                break
            self.tabshift=a
            self.k1.write(f"{a}</term>\n")
            break
        
    def compileExpressionlist(self,line):
        self.line=line
        self.k1.write(f"{self.tabshift}<expressionList>\n")
        a=self.tabshift
        self.tabshift=self.tabshift+"   "
        run =True
        while run:
            if ")" in self.line:
                self.tabshift=a
                break
            if "," in self.line:
                self.k1.write(f"{self.tabshift}{self.line}")
                self.line=self.k.readline()
            self.compileExpression(self.line)
        self.tabshift=a
        self.k1.write(f"{a}</expressionList>\n")