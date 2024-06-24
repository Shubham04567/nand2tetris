from Parser import Parser
from Code import Code
import sys
class Main:
    def __init__(self,file):
        self.f=file
        print(self.f)
        self.parse=Parser(self.f)        #object for parser module
        file2 = file[:-4]+".hack"        #output file
        self.code=Code(file2)            #object for code module

    def generate(self):
        #First pass (to add all label symbol table)
        self.parse.label_count()
        for i in range(len(self.parse.list)):
            self.code.l_inst(self.parse.list[i],self.parse.list2[i])

        #Second pass
        while self.parse.hasMoreLine():
            if self.parse.advance()==True:
                if self.parse.instructionType()=="A_INSTRUCTION":
                    self.code.inst_map(self.parse.symbol())
                    self.code.change_line()

                elif self.parse.instructionType()=="C_INSTRUCTION":
                    self.code.add()            #to add "111" in c_instruction
                    self.code.comp_map(self.parse.comp())
                    self.code.dest_map(self.parse.dest())
                    self.code.jump_map(self.parse.jump())
                    self.code.change_line()
        

if __name__=="__main__":
    inp=sys.argv[1]
    a=Main(inp)
    a.generate()