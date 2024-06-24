class Parser:
    def __init__(self,file):
        f=open(file,'r')
        self.f=f
        self.current_command = None
        
    def hasMoreLine(self):
        ptr=self.f.tell()
        a=self.f.readline() != ''
        self.f.seek(ptr)
        return  a
    
    def advance(self):
       
        line = self.f.readline().strip('\n')  # Read and strip newline characters
        while line.startswith("//") or len(line) == 0:
            line = self.f.readline().strip()  # Keep reading until a valid line is found
            
        if line.find("//")!=-1:
            a=line.find("//")
            
            line=line[:a]
            line=line.strip("\n")
        self.current_command = line.strip()
       
                    
    def CommandType(self):
        
        line=self.current_command.strip()
        if line in ["add","sub","neg","eq","gt","lt","and","or","not"]:
            return "C_ARITHMETIC"

        
        elif line.find('pop')!=-1:
            return "C_POP"
        elif line.find('push')!=-1:
            return "C_PUSH"
        elif line.find("label")!=-1:
            return "C_LABEL"
        elif line.find("goto")!=-1 and line.find("if")==-1:
            
            return "C_GOTO"
        elif line.find("if-goto")!=-1:
            return "C_IF"
        elif line.find("function")!=-1:
            return "C_FUNCTION"
        elif line.find("return")!=-1:
            return "C_RETURN"
        elif line.find("call")!=-1:
            return "C_CALL"
        
        
    def arg1(self):
        if self.CommandType()=="C_ARITHMETIC":
            return f'{self.current_command}'
        elif self.CommandType()=="C_POP":
            aa=self.current_command.split()
            return f"{aa[1]}"
        elif self.CommandType()=="C_PUSH":
            aa=self.current_command.split()
            return f"{aa[1]}"
        elif self.CommandType()=="C_LABEL":
            aa=self.current_command.split()
            return f"{aa[1]}"
        elif self.CommandType()=="C_GOTO":
            aa=self.current_command.split()
            return f"{aa[1]}"
        elif self.CommandType()=="C_IF":
            aa=self.current_command.split()
            # print("dcvsjk")
            return f"{aa[1]}"
        elif self.CommandType()=="C_FUNCTION":
            aa=self.current_command.split()
            return f"{aa[1]}"
        elif self.CommandType()=="C_CALL":
            aa=self.current_command.split()
            return f"{aa[1]}"
        
        
    def arg2(self):
        if self.CommandType()=="C_POP":
            aa=self.current_command.split()
            return f"{aa[2]}"
        elif self.CommandType()=="C_PUSH":
            aa=self.current_command.split()
            return f"{aa[2]}"
        elif self.CommandType()=="C_FUNCTION":
            aa=self.current_command.split()
            return f"{aa[2]}"
        elif self.CommandType()=="C_CALL":
            aa=self.current_command.split()
            return f"{aa[2]}"
        
        