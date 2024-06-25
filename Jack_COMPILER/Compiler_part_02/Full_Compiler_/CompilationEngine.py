from VMWriter import VMWriter
from SymbolTable import SymbolTable
import os 
class CompilationEngine:
    def __init__(self,output1,output2):
        self.out = output2
        self.k=open(output1,"r")
        self.k1=open(output2,"w")
        self.o=self.k.readline()
        self.line=None
        self.li=" 785 "
        self.cl_list=SymbolTable()
        self.sl_list=SymbolTable()
        out=output2[:-4]+".vm"
        self.writable=VMWriter(out)
        self.op=[]
        self.classname=""                                      # store the classname
        self.label=0                                           # define the new label
        self.variable_count=0                                  # count total number of variable in function
        self.parameter_c=0                                     # count total number of argument in function
        self.field_count=0                                     # count total number of class variable in class
    
    def compileClass(self):
        self.k1.write("<class>\n")
        self.line=self.k.readline()
        self.cl_list.reset()                                   #calling reset function for class symbol table
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()
        self.k1.write(f"{self.line}")
        self.classname=self.line.split(">")[1].split("<")[0].strip(" ")
        self.line=self.k.readline()
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()

        while "static" in self.line or "field" in self.line:
            self.compileClassVarDec(self.line)  
        while "function" in self.line or "method" in self.line or "constructor" in self.line:
            self.compileSubroutine(self.line)
        self.k1.write(f"{self.line}")
        self.k1.write("</class>\n")
        self.k1.close()
        os.remove(self.out)
                           
    def compileClassVarDec(self,line):
        self.line=line
        self.k1.write("<classVarDec>\n")
        nextlin_1=None
        nextlin_2=None
        nextlin_3=None
        run=True
        while run:
            if "field" in self.line or "static" in line:
                if "field" in self.line:
                    self.field_count+=1
                self.k1.write(f"{self.line}")
                nextlin_1=self.line.split(">")[1].split("<")[0].strip(" ")           # kind of class variable
                self.line=self.k.readline()
                self.k1.write(f"{self.line}")
                nextlin_2=self.line.split(">")[1].split("<")[0].strip(" ")           # type of class variable
                self.line=self.k.readline()
                self.k1.write(f"{self.line}")
                nextlin_3=self.line.split(">")[1].split("<")[0].strip(" ")           # name of class variable
                self.line=self.k.readline()
                self.cl_list.define(nextlin_1,nextlin_2,nextlin_3)                   # adding variable to class table    
            if "," in self.line:
                self.field_count+=1
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if "identifier" in self.line:
                self.k1.write(f"{self.line}")
                nextlin_4=self.line.split(">")[1].split("<")[0].strip(" ")
                self.line=self.k.readline()
                self.cl_list.define(nextlin_1,nextlin_2,nextlin_4)
            if ";" in self.line:
                break
        self.k1.write(f"{self.line}")
        self.k1.write("</classVarDec>\n")
        self.line=self.k.readline()       
          
    def compileSubroutine(self,line):
        self.line=line
        self.k1.write("<subroutineDec>\n")
        run=True
        while run:
            line1=self.line
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            self.k1.write(f"{self.line}")
            tt=self.line.split(">")[1].split("<")[0].strip(" ")                        # take the function type
            self.line=self.k.readline()
            function_name=self.line.split(">")[1].split("<")[0].strip(" ")             # take the function name
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            
            if "(" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileParameterList(self.line,line1)
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                point=self.k.tell()
            
                if "function" in line1:
                    self.var_count()
                    self.k.seek(point)
                    name=self.classname+"."+function_name
                    self.writable.writeFunction(name,self.variable_count)                  # handling the function
                    self.variable_count=0
                    
                elif "constructor" in line1:
                    self.var_count()
                    self.k.seek(point)
                    name=tt+"."+function_name
                    self.writable.writeFunction(name,self.variable_count)
                    self.writable.writePush("constant",self.field_count)
                    self.variable_count=0
                    self.field_count=0
                    self.writable.writeCall("Memory.alloc",1)
                    self.writable.writePop("pointer",0)
                    
                elif "method" in line1:
                    self.var_count()
                    self.k.seek(point)
                    name=self.classname+"."+function_name
                    self.writable.writeFunction(name,self.variable_count)
                    self.variable_count=0
                    self.writable.writePush("argument",0)
                    self.writable.writePop("pointer",0)
                break 
            self.line=self.k.readline()
        self.compileSubroutineBody(self.line)     
        self.k1.write("\t</subroutineDec>\n")
        
# defining function for variable count in function
    def var_count(self):
        line=self.k.readline()
        while line.find("var")!=-1:
            type=self.k.readline()
            identifier=self.k.readline()
            line=self.k.readline()
            self.variable_count+=1
            if line.find(",")!=-1:
                while line.find(";")==-1:
                    identifier=self.k.readline()
                    self.variable_count+=1
                    line=self.k.readline()
            line=self.k.readline()
                   
    def compileParameterList(self,line,line1):
        self.sl_list.reset() 
        self.line=line
        self.k1.write("<parameterList>\n")
        if "method" in line1:
            self.sl_list.define("argument",self.classname,"this")                      # pushing this to symbol table for method
        run=True
        while(run):
            if "keyword" in self.line or "identifier" in self.line:
                self.parameter_c+=1                                                    # counting parameters
                self.k1.write(f"{self.line}")
                nextlin_1=self.line.split(">")[1].split("<")[0].strip(" ")
                self.line=self.k.readline()
                nextlin_2=self.line.split(">")[1].split("<")[0].strip(" ")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.sl_list.define("argument",nextlin_1,nextlin_2)                    # adding argument to symbol table   
            if "," in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if ")" in self.line:
                break
        self.k1.write("</parameterList>\n")
        
    def compileSubroutineBody(self,line):
        self.line=line
        self.k1.write("<subroutineBody>\n")
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()
        while "var" in self.line:
            self.compileVarDec(self.line)
        while "let" in self.line or "while" in self.line or "if" in self.line or "do" in self.line or "return" in self.line:
            self.compileStatement(self.line)
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()
        self.k1.write("</subroutineBody>\n")
        
    def compileStatement(self,line):
        self.line=line
        self.k1.write("<statements>\n")
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
        self.k1.write("</statements>\n")
        if "}" in self.line:
            pass
        else:
            self.line=self.k.readline()
        
    def compileVarDec(self,line):
        self.line=line
        self.k1.write("<varDec>\n")
        nextlin_1=None
        nextlin_2=None
        nextlin_3=None
        run=True
        while run:
            if "var" in self.line:
                self.k1.write(f"{self.line}")
                nextlin_1="local"
                self.line=self.k.readline()
                self.k1.write(f"{self.line}")
                nextlin_2=self.line.split(">")[1].split("<")[0].strip(" ")
                self.line=self.k.readline()
                self.k1.write(f"{self.line}")
                nextlin_3=self.line.split(">")[1].split("<")[0].strip(" ")
                self.line=self.k.readline()
                self.sl_list.define(nextlin_1,nextlin_2,nextlin_3)                          # adding variable to symbol table
                
            if "," in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if "identifier" in self.line:
                self.k1.write(f"{self.line}")
                nextlin_4=self.line.split(">")[1].split("<")[0].strip(" ")
                self.line=self.k.readline()
                self.sl_list.define(nextlin_1,nextlin_2,nextlin_4)
    
            if ";" in self.line:
                break
        self.k1.write(f"{self.line}")
        self.k1.write("</varDec>\n")
        self.line=self.k.readline()         

    def compileLet(self,line):
        self.line=line
        self.k1.write("<letStatement>\n")
        foundarray=False
        run =True
        while run:
            self.k1.write(f"{self.line}")
            varname=self.line.split(">")[1].split("<")[0].strip(" ")
            self.line=self.k.readline()
            # array handling
            if "[" in self.line:
                foundarray=True
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                available=self.sl_list.member(varname)                    
                if available:
                    self.writable.writePush(self.sl_list.kindOf(varname),self.sl_list.indexOf(varname))
                else:
                    available=self.cl_list.member(varname)
                    if available:
                        self.writable.writePush(self.cl_list.kindOf(varname),self.cl_list.indexOf(varname))
                
                self.compileExpression(self.line)
                self.writable.writhArithmetic("+")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if "=" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                #Handling the expression's array
                if foundarray==True:
                    self.writable.writePop("temp",0)
                    self.writable.writePop("pointer",1)
                    self.writable.writePush("temp",0)
                    self.writable.writePop("that",0)
                    foundarray=False
                else:
                    found=self.sl_list.member(varname)
                    if found :
                        self.writable.writePop(self.sl_list.kindOf(varname),self.sl_list.indexOf(varname))
                    else:
                        found=self.cl_list.member(varname)
                        if found :
                            self.writable.writePop(self.cl_list.kindOf(varname),self.cl_list.indexOf(varname))
            if ";" in self.line:
                break
        self.k1.write(f"{self.line}")
        self.k1.write("</letStatement>\n")
        self.line=self.k.readline()
        
    def compileWhile(self,line):
        self.line=line
        self.k1.write("<whileStatement>\n")
        run =True
        while run:
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            label3=self.label
            self.label+=1
            self.writable.writeLabel(f"WHILE.{label3}")
            if "(" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                label4=self.label
                self.label+=1
                self.writable.writhArithmetic("~")
                self.writable.writeIf(f"WHILE_END.{label4}")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if "{" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileStatement(self.line)
                self.writable.writeGoto(f"WHILE.{label3}")
                self.writable.writeLabel(f"WHILE_END.{label4}")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                break
        self.k1.write("</whileStatement>\n")
             
    def compileIf(self,line):
        self.line=line
        self.k1.write("<ifStatement>\n")
        run =True
        while run:
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            if "(" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.writable.writhArithmetic("~")
                label1=self.label
                self.label+=1
                self.writable.writeIf(f"IF_E.{label1}")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
            if "{" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                self.compileStatement(self.line)
                label2=self.label
                self.label+=1
                self.writable.writeGoto(f"IF_S.{label2}")
                self.writable.writeLabel(f"IF_E.{label1}")
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                break
        if "else" in self.line:
            s=run
            while s:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                if "{" in self.line:
                    self.k1.write(f"{self.line}")
                    self.line=self.k.readline()
                    self.compileStatement(self.line)
                    
                    self.k1.write(f"{self.line}")
                    self.line=self.k.readline()
                    break
        self.writable.writeLabel(f"IF_S.{label2}")
        self.k1.write("</ifStatement>\n")

    def compileDo(self,line):
        self.line=line
        self.k1.write("<doStatement>\n")
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()
        self.k1.write(f"{self.line}")
        token=self.line.split(">")[1].split("<")[0].strip(" ")
        self.line=self.k.readline()
        nexttoken=self.line.split(">")[1].split("<")[0].strip(" ")
        check=False
        name=token
        if nexttoken=="(":
            name=self.classname+"."+token
            self.writable.writePush("pointer",0)
            check=True
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            count=self.compileExpressionlist(self.line)
            self.k1.write(f'{self.line}')
            self.line=self.k.readline()
        else:
            check=self.sl_list.member(token)
            if check:
                self.writable.writePush("local",self.sl_list.indexOf(token))
                type=self.sl_list.typeOf(token)
                token=type
            else:
                check=self.cl_list.member(token)
                if check:
                    self.writable.writePush("this",self.cl_list.indexOf(token))
                    type=self.cl_list.typeOf(token)
                    token=type
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            name2=self.line.split(">")[1].split("<")[0].strip(" ")                        # subroutine name
            name=token+"."+name2
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            self.k1.write(f"{self.line}")
            self.line=self.k.readline()
            count=self.compileExpressionlist(self.line)
            self.k1.write(f'{self.line}')
            self.line=self.k.readline()
        if check:
            count+=1
        self.writable.writeCall(name,count)
        self.writable.writePop("temp",0)
        self.k1.write(f'{self.line}')
        self.line=self.k.readline()
        self.k1.write("</doStatement>\n")
         
    def compileReturn(self,line):
        self.line=line
        self.k1.write("<returnStatement>\n")
        self.k1.write(f"{self.line}")
        self.line=self.k.readline()
        found=False
        run =True
        while run:
            if ";" in self.line:
                self.k1.write(f"{self.line}")
                self.line=self.k.readline()
                break
            found=True
            self.compileExpression(self.line)
        if found:
            self.writable.writeReturn()
        else:
            self.writable.writePush("constant",0)
            self.writable.writeReturn()
        self.k1.write("</returnStatement>\n")
          
    def compileExpression(self,line):
        self.line=line
        self.k1.write("<expression>\n")
        run = True
        while run:
            self.compileTerm(self.line)
            self.sim=self.line.split(">")[1].split("<")[0].strip(" ")
            
            h=["+","-","=","&lt;","&gt;","&amp;","*","/","|","*"]                           # list of operators
            for i in h:
                if self.sim == i:
                    self.op.append(self.sim)
                    self.k1.write(self.line)
                    self.line=self.k.readline()
                    self.compileTerm(self.line)
                    last=self.op[-1]
                    # call for operators 
                    if last=="*":
                        self.writable.writeCall("Math.multiply",2)                         # calling function for multiply
                        self.op.pop()
                    elif last=="/":
                        self.writable.writeCall("Math.divide",2)                           # calling function for divide
                        self.op.pop()
                    else:
                        self.writable.writhArithmetic(last)
                        self.op.pop()
                    break
                
            if ";" in self.line and "&" not in self.line: 
                self.k1.write("</expression>\n")
                break
            if "]" in self.line:
                self.k1.write("</expression>\n")
                break
            if "," in self.line:
                self.k1.write("</expression>\n")
                break
            else:
                self.k1.write("</expression>\n")
                break
                 
    def compileTerm(self,line):
        self.line=line
        self.k1.write("<term>\n")
        run =True
        while run:
            if "(" in self.line:
                self.k1.write(self.line)
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.k1.write(self.line)
                self.line=self.k.readline()
                self.k1.write("</term>\n")
                break
            rr=self.line                                         # rr store the preceeding term value
            self.k1.write(f"{self.line}")
            const=rr.split(">")[1].split("<")[0].strip(" ")      # const store only term in line
            if const.isdigit()==True:
                self.writable.writePush("constant",const)
            elif "identifier" in self.line:
                found=self.sl_list.member(const)                 # checking for variable available in function symbol table 
                if found:
                    kind=self.sl_list.kindOf(const)
                    index=self.sl_list.indexOf(const)
                    self.writable.writePush(kind,index)             
                else:
                    found=self.cl_list.member(const)              # checking for variable available in class symbol table 
                    if found:
                        kind=self.cl_list.kindOf(const)
                        index=self.cl_list.indexOf(const)
                        self.writable.writePush(kind,index)
            elif const in ["true","false","null","this"]:
                if const=="true":
                    self.writable.writePush("constant",1)
                    self.writable.writhArithmetic("!")
                elif const=="false":
                    self.writable.writePush("constant",0)
                elif const=="null":
                    self.writable.writePush("constant",0)
                elif const=="this":
                    self.writable.writePush("pointer",0)
            # Handling the string in jack
            elif "stringConstant" in self.line:
                String_word=rr.split(">")[1].split("<")[0].lstrip()[:-1]
                lenght=len(String_word)
                self.writable.writePush("constant",lenght)
                self.writable.writeCall("String.new",1)
                for i in String_word:
                    self.writable.writePush("constant",ord(i))                  # pushing the respective ASCII value of string
                    self.writable.writeCall("String.appendChar",2)
                
            self.hh=self.line.split(">")[1].split("<")[0].strip(" ")
            self.line=self.k.readline()
            # handling the subroutine call
            if "." in self.line:
                    self.k1.write(self.line)
                    self.line=self.k.readline()
                    self.k1.write(self.line)
                    kk=self.line.split(">")[1].split("<")[0].strip(" ")
                    self.line=self.k.readline()
                    if "(" in self.line:
                        self.k1.write(self.line)
                        self.line=self.k.readline()
                        a=self.compileExpressionlist(self.line)
                        self.k1.write(self.line)
                        self.line=self.k.readline()
                        found=self.sl_list.member(const)
                        if found:
                            a+=1
                            typo=self.sl_list.typeOf(const)
                            na=typo+"."+kk
                            self.writable.writeCall(na,a)
                        else:
                            found2=self.cl_list.member(const)
                            if found2:
                                a+=1
                                qq=self.cl_list.typeOf(const)
                                na=qq+"."+kk
                                self.writable.writeCall(na,a)
                            else:
                                na=const+"."+kk
                                self.writable.writeCall(na,a)
            if "~" in rr and "(" in self.line:
                self.compileTerm(self.line)
                self.writable.writhArithmetic("~")
                self.k1.write("</term>\n")
                break
            if "(" in self.line:
                self.k1.write(self.line)
                self.line=self.k.readline()
                count=self.compileExpressionlist(self.line)
                self.writable.writeCall(const,count)
                self.k1.write(self.line)
                self.line=self.k.readline()
                break
            # Handling the array
            if "[" in self.line:
                self.k1.write(self.line)
                self.line=self.k.readline()
                self.compileExpression(self.line)
                self.writable.writhArithmetic("+")
                self.writable.writePop("pointer",1)
                self.writable.writePush("that",0)
                self.k1.write(self.line)
                self.line=self.k.readline()
            if "-" in rr:
                self.compileTerm(self.line)
                self.writable.writhArithmetic("!")
            if "~" in rr:
                self.compileTerm(self.line)
                self.writable.writhArithmetic("~")
                self.k1.write("</term>\n")
                break
            self.k1.write("</term>\n")
            break
        
        
    def compileExpressionlist(self,line):
        self.line=line
        self.k1.write("<expressionList>\n")
        run =True
        count=0                
        while run:
            if ")" in self.line:
                break
            if "," in self.line:
                self.k1.write(self.line)
                self.line=self.k.readline()
            count+=1
            self.compileExpression(self.line)
        self.k1.write("</expressionList>\n")
        return count           