from SymbolTable import SymbolTable
class Code:
    def __init__(self,file2):
        self.g = open(file2,"w")
        self.sim = SymbolTable()             #object for the symbol table
        self.count_var=16                    #store the values corresponding to variable

    def inst_map(self,string):
        d=string
        if d.isdigit()==True:
            self.g.write('0')
            self.g.write(bin(int(d))[2:].zfill(15))
        elif self.sim.contain(d)==True:
            value=self.sim.getEntry(d)
            self.g.write(bin(value)[2:].zfill(16))
        else:
            self.sim.addEntry(d,self.count_var)
            self.g.write(bin(self.count_var)[2:].zfill(16))
            self.count_var+=1

    def l_inst(self,string,idx):
        d=string
        self.sim.addEntry(d,idx)

    def dest_map(self,string):
        d=string
        if d in self.sim._dest:
            self.g.write(self.sim._dest[d])
        
    def comp_map(self,string):
        d=string
        if d in self.sim._comp:
            self.g.write(self.sim._comp[d])

    def jump_map(self,string):
        d=string
        if d in self.sim._jump:
            self.g.write(self.sim._jump[d])

    def change_line(self):
        self.g.write(f"\n")

    def add(self):
        self.g.write("111")
