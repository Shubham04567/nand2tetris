class VMWriter:
    def __init__(self,out):
        self.l=open(out,"w")
        
        
    def writePush(self,segment,index):
        if segment=="constant":
            self.l.write(f"push {segment} {index}\n")
        elif segment=="local":
            self.l.write(f"push local {index}\n")
        elif segment == "field":
            self.l.write(f"push this {index}\n")
        elif segment=="static":
            self.l.write(f"push {segment} {index}\n")
        else:
            self.l.write(f"push {segment} {index}\n")
            
    def writePop(self,segment,index):
        if segment=="constant":
            self.l.write(f"pop {segment} {index}\n")
        elif segment=="local":
            self.l.write(f"pop local {index}\n")
        elif segment == "field":
            self.l.write(f"pop this {index}\n")
        elif segment=="static":
            self.l.write(f"pop {segment} {index}\n")
        else:
            self.l.write(f"pop {segment} {index}\n")
            
    
    def writhArithmetic(self,command):
        if command=="+":
            self.l.write(f"add\n")
        elif command=="-":
            self.l.write(f"sub\n")
        elif command=="=":
            self.l.write(f"eq\n")
        elif command=="&lt;":
            self.l.write(f"lt\n")
        elif command=="&gt;":
            self.l.write(f"gt\n")
        elif command=="&amp;":
            self.l.write(f"and\n")
        elif command=="|":
            self.l.write(f"or\n")  
        elif command=="~":
            self.l.write(f"not\n") 
        elif command=="!":
            self.l.write(f"neg\n")  
            
    def writeLabel(self,label):
        self.l.write(f"label {label}\n")
    
    def writeGoto(self,label):
        self.l.write(f"goto {label}\n")
    
    def writeIf(self,label):
        self.l.write(f"if-goto {label}\n")
    
    def writeCall(self,name,nargs):
        self.l.write(f"call {name} {nargs}\n")
    
    def writeFunction(self,name,nVars,):
        self.l.write(f"function {name} {nVars}\n")
    
    def writeReturn(self):
        self.l.write("return\n")
    
    def close(self):
        self.l.close()
        