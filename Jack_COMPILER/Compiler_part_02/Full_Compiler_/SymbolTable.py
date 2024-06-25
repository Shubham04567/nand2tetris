class SymbolTable:
    def __init__(self):
        self.list=[]
        self.index_field=0
        self.index_static=0
        self.index_arg=0
        self.index_var=0
    
    def reset(self):
        self.list=[]
        self.index_field=0
        self.index_static=0
        self.index_arg=0
        self.index_var=0
        
        
    def define(self,a,b,c):
        name=c
        type=b
        kind=a
        if kind == "field":
            self.list.append([name,type,kind,self.index_field])
            self.index_field+=1
        if kind == "static":
            self.list.append([name,type,kind,self.index_static])
            self.index_static+=1
        if kind == "argument":
            self.list.append([name,type,kind,self.index_arg])
            self.index_arg+=1
        if kind == "local":
            self.list.append([name,type,kind,self.index_var])
            self.index_var+=1
        # print(self.list)
        
        
        
    def varCount(self,kin):
        count=0
        for i in range(len(self.list)):
            if kin==self.list[i][2]:
                count+=1
        return count
        
        
    def kindOf(self,ad):
        name=ad
        for i in range(len(self.list)):
            if name==self.list[i][0]:
                return self.list[i][2]
        return None
    
    
    def typeOf(self,nam):
        for i in range(len(self.list)):
            if nam==self.list[i][0]:
                return self.list[i][1]
            
            
    def indexOf(self,ind):
        for i in range(len(self.list)):
            if ind==self.list[i][0]:
                return self.list[i][3]
            
    def member(self,name):
        for i in self.list:
            if i[0]==name:
                return True
        return False
