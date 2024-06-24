class Parser:
    def __init__(self,tt):
        self.out=open(tt, "r")
        self.line=""                 #store the current instruction
        self.counter=0
        self.list=[]                 #list to store all label during first pass
        self.list2=[]                #list to store all correspoding values of label 
    
    def hasMoreLine(self):
        a=self.out.tell()
        line=self.out.readline()
        b=(line!="")
        self.out.seek(a)
        return b

    def advance(self):
        line=self.out.readline().rstrip("\n").lstrip().rstrip()
        if (line.startswith("//") or (len(line)==0)):
            return False
        else:
            if line.find("/")!=-1:
                b=line.find("/")
                line=line[:b].rstrip().lstrip()
            self.line=line
            return True

    def label_count(self):  
        #first pass
        aa=self.out.tell()
        while self.hasMoreLine():
            self.line=self.out.readline().rstrip("\n").lstrip()
            if (self.line.startswith("//") or (len(self.line)==0)):
                continue
            else:
                if self.line[0]=="(":
                    self.list.append(self.line.split("(")[1].split(")")[0])
                    self.list2.append(self.counter)
                else:
                    self.counter+=1
        self.out.seek(aa)
 
    def instructionType(self):
        if self.line.startswith("@"):
            return "A_INSTRUCTION"
        elif self.line.startswith("("):
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"

    def symbol(self):
        line=self.line
        if line[0]=="@":
            return f"{line[1:]}"
        else:
            ad=line.split("(")[1].split(")")[0]
            return f"{ad}"

    def dest(self):
        line=self.line      
        if "=" in line:
            a=line.find("=")
            return  f"{line[:a]}"
        else:
            return "null"

    def comp(self):
        line=self.line
        if ("=" in line) and (";" in line):
            aa=line.split("=")[1].split(";")[0]
            return f"{aa}"
        elif line.find("=")!=-1:
            aa=line.split("=")[1]
            return f"{aa}"
        else:
            aa=line.split(";")[0]
            return f"{aa}"

    def jump(self):
        line=self.line       
        if ";" in line:
            a=line.find(";")
            return  f"{line[a+1:]}"
        else:
            return "null"