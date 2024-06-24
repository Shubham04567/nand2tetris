import sys
# import os
from Parser import Parser
from CodeWriter import CodeWriter
from os import walk

class main:
    def __init__(self):
        inp=sys.argv[1]
        out_file=None
        coder=None
        fil_name=[]
        if ".vm" in inp:
            fil_name.append(inp)
            output_file=open(inp.replace(".vm",".asm"),'w')
            
            self.codewrite=CodeWriter(output_file)  
        else:
            for (dirpath,_,filenames) in walk(inp):
                for name in filenames:
                    if name.endswith(".vm"):
                        fil_name.append(dirpath+"/"+name)
            outname=""
            if "/" in inp:
                outname=inp[inp.rfind("/")+1:].strip()
            else:
                outname=inp
            
            output_file=open(inp+"/"+outname+".asm","w")
            self.codewrite=CodeWriter(output_file)  
            self.codewrite.f1.write("@256\nD=A\n@SP\nM=D\n")
        
            self.codewrite.WriteCall("Sys.init",0)
        
        for i_file in fil_name:
            # print(i_file)
            self.codewrite.setFileName(i_file.split("/")[-1][:-3])
            self.parser=Parser(i_file)
            self.generate()
        
      
    def generate(self):
        while self.parser.hasMoreLine()==True:
            self.parser.advance()
            
            if self.parser.CommandType()=="C_ARITHMETIC":
                self.codewrite.writeArithmetic(self.parser.arg1())
            elif self.parser.CommandType()=="C_PUSH" or self.parser.CommandType()=="C_POP":
                self.codewrite.writePushPop(self.parser.CommandType(),self.parser.arg1(),self.parser.arg2())
            elif self.parser.CommandType()=="C_LABEL":
                self.codewrite.WriteLabel(self.parser.arg1())
            elif self.parser.CommandType()=="C_GOTO":
                self.codewrite.WriteGoto(self.parser.arg1())
            elif self.parser.CommandType()=="C_IF":
                self.codewrite.WriteIf(self.parser.arg1())
            elif self.parser.CommandType()=="C_FUNCTION":
                self.codewrite.WriteFunction(self.parser.arg1(),self.parser.arg2())
            elif self.parser.CommandType()=="C_CALL":
                self.codewrite.WriteCall(self.parser.arg1(),self.parser.arg2())
            elif self.parser.CommandType()=="C_RETURN":
                self.codewrite.WriteReturn()
            
            
            else:
                pass
            
        self.codewrite.closes()

main()
