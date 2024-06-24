
class CodeWriter:
    fileName=""
    def __init__(self,output_file):
       
        self.f1=output_file
        self.label_counter=0
        self.funct=""
        self.i = 0
        
        
    def setFileName(self,name):self.fileName=name
        
        
    def writeArithmetic(self,command):
        if command=="add":
            self.f1.write("@R0\nD=M-1\nA=D\nD=M\nA=A-1\nM=M+D\n@R0\nM=M-1\n@R0\nA=M\nM=0\n")
        elif command=="sub":
            self.f1.write("@R0\nD=M-1\nA=D\nD=M\nA=A-1\nM=M-D\n@R0\nM=M-1\n@R0\nA=M\nM=0\n")
        elif command=="neg":
            self.f1.write("@R0\nD=M-1\nA=D\nM=-M\n")
        elif command=="and":
            self.f1.write("@R0\nD=M-1\nA=D\nD=M\nA=A-1\nM=M&D\n@R0\nM=M-1\n@R0\nA=M\nM=0\n")
        elif command=="or":
            self.f1.write("@R0\nD=M-1\nA=D\nD=M\nA=A-1\nM=M|D\n@R0\nM=M-1\n@R0\nA=M\nM=0\n")
        elif command=="not":
            self.f1.write("@R0\nD=M-1\nA=D\nM=!M\n")
        elif command=="gt":
            label = self._generate_label()
            self.f1.write(f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M\nM=0\n@TRUE_{label}\nD;JLE\n@SP\nA=M\nM=-1\n(TRUE_{label})\n@SP\nM=M+1\n")
        elif command=="lt":
            label = self._generate_label()
            self.f1.write(f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M\nM=0\n@TRUE_{label}\nD;JGE\n@SP\nA=M\nM=-1\n(TRUE_{label})\n@SP\nM=M+1\n")
        elif command=="eq":
            label = self._generate_label()
            self.f1.write(f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M\nM=0\n@TRUE_{label}\nD;JNE\n@SP\nA=M\nM=-1\n(TRUE_{label})\n@SP\nM=M+1\n")
            
            
    def writePushPop(self,command,segment,index):
        if command=="C_PUSH" :
            if segment=="constant":
                self.f1.write(f"@{index}\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1\n")
            elif segment=="local":
                self.f1.write(f"@{index}\nD=A\n@LCL\nA=M\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="argument":
                self.f1.write(f"@{index}\nD=A\n@ARG\nA=M\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="this":
                self.f1.write(f"@{index}\nD=A\n@THIS\nD=D+M\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="that":
                self.f1.write(f"@{index}\nD=A\n@THAT\nD=D+M\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="temp":
                self.f1.write(f"@{index}\nD=A\n@R5\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="pointer":
                if index=="0":
                    self.f1.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                else:
                    self.f1.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment=="static":
                self.f1.write(f"@static_{self.fileName}.{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                    
            else:
                pass
        else:
            # if segment=="constant":
            #     self.f1.write(f"@{index}\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1\n")
            if segment=="local":
                self.f1.write(f"@{index}\nD=A\n@LCL\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            elif segment=="argument":
                self.f1.write(f"@{index}\nD=A\n@ARG\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            elif segment=="this":
                self.f1.write(f"@{index}\nD=A\n@THIS\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            elif segment=="that":
                self.f1.write(f"@{index}\nD=A\n@THAT\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            elif segment=="temp":
                self.f1.write(f"@{index}\nD=A\n@R5\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            elif segment=="pointer":
                if index=="0":
                    self.f1.write("@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n")
                else:
                    self.f1.write("@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n")
            elif segment=="static":
                self.f1.write(f"@SP\nM=M-1\nA=M\nD=M\n@static_{self.fileName}.{index}\nM=D\n")
                    
            # elif segment=="temp":
            #     self.f1.write(f"@{index}\nD=A\n@R5\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n")
            
    def WriteLabel(self,label):
        a = self.funct + label
        self.f1.write(f"({a})\n")
    
    def WriteGoto(self,label):
        a = self.funct + label
        
        self.f1.write(f"@{a}\n0;JMP\n")
    
    def WriteIf(self,label):
        a = self.funct + label
        self.f1.write(f"@SP\nM=M-1\nA=M\nD=M\n@{a}\nD;JNE\n") 
    
    def WriteFunction(self,functionName,nVars):
        self.funct=functionName
        self.f1.write(f"({functionName})\n")
        for i in range(int(nVars)):
            self.f1.write(f"@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.i=0
    
    def WriteCall(self,functionName,nArgs):
        self.f1.write(f"@return_{self.funct}.{self.i}\n")
        self.f1.write("D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.f1.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.f1.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.f1.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.f1.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.f1.write(f"@5\nD=A\n@{nArgs}\nD=A+D\n@SP\nD=M-D\n@ARG\nM=D\n")
        self.f1.write("@SP\nD=M\n@LCL\nM=D\n")
        self.f1.write(f"@{functionName}\n0;JMP\n")
        self.f1.write(f"(return_{self.funct}.{self.i})\n")
        self.i = self.i +1
    
    def WriteReturn(self):
        self.f1.write("@LCL\nD=M\n@13\nM=D\n")
        # self.f1.write("@5\nA=D-A\nD=M\n@R14\nM=D\n")
        self.f1.write("@13\nD=M\n@5\nD=D-A\nA=D\nD=M\n@14\nM=D\n")
        self.f1.write("@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        self.f1.write("@ARG\nD=M\n@1\nD=D+A\n@SP\nM=D\n")
        # self.f1.write("@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n")
        
        self.f1.write("@13\nD=M\n@1\nD=D-A\nA=D\nD=M\n@THAT\nM=D\n")
        self.f1.write("@13\nD=M\n@2\nD=D-A\nA=D\nD=M\n@THIS\nM=D\n")
        self.f1.write("@13\nD=M\n@3\nD=D-A\nA=D\nD=M\n@ARG\nM=D\n")
        self.f1.write("@13\nD=M\n@4\nD=D-A\nA=D\nD=M\n@LCL\nM=D\n")
        self.f1.write("@14\nA=M\n0;JMP\n")
    
    def _generate_label(self):
        """
        Generates a unique label for branching operations.
        """
        self.label_counter += 1
        return str(self.label_counter)       
    
    def closes(self):
        self.f1.write("(END)\n@END\n0;JMP\n")
            
        
        
        
        
            
        
        

































































































































































