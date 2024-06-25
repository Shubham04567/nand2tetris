import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import os
from os import walk
class Jackanalyser:
    def __init__(self):
        inp=sys.argv[1]
        if ".jack" in inp:
            self.b=JackTokenizer(inp)
            fi=inp[:-5]+"T.xml"             # tockens file
            fe=inp[:-5]+".xml"             # final xml file for project 10
            self.fe=fe
            self.fi=fi
            self.out=open(fi,"w")
            self.tokenize()
            self.grammer()
            self.out.close()
            os.remove(self.fi)
        else:
            for (dirpath,_,filenames) in walk(inp):
                for name in filenames:
                    if name.endswith(".jack"):
                        name=os.path.join(dirpath,name)
                        self.b=JackTokenizer(name)
                        fi=name[:-5]+"T.xml"              #tockens file
                        fe=name[:-5]+".xml"              # final file for project 10
                        self.fe=fe
                        self.fi=fi
                        self.out=open(fi,"w")
                        self.tokenize()
                        self.grammer()
                        self.out.close()
                        os.remove(self.fi)
    
    def tokenize(self):
        self.out.write("<tokens>\n")
        while (self.b.hasMoreLine()):
            self.b._advance()
        while (self.b.hasMoreTocken()):
            self.b.advance()
            if self.b.tokenType()=="KEYWORD":
                self.out.write(f"<keyword> {self.b.current_token} </keyword>\n")
            elif self.b.tokenType()=="SYMBOL":
                if self.b.current_token!="<" and self.b.current_token!=">" and self.b.current_token!="&":
                    self.out.write(f"<symbol> {self.b.current_token} </symbol>\n")
                elif self.b.current_token=="<":
                    self.out.write(f"<symbol> &lt; </symbol>\n")
                elif self.b.current_token==">":
                    self.out.write(f"<symbol> &gt; </symbol>\n")
                elif self.b.current_token=="&":
                    self.out.write(f"<symbol> &amp; </symbol>\n")
            elif self.b.tokenType()=="INT_CONST":
                self.out.write(f"<integerConstant> {self.b.current_token} </integerConstant>\n")
            elif self.b.tokenType()=="STRING_CONST":
                self.out.write(f"<stringConstant> {self.b.current_token} </stringConstant>\n")
            elif self.b.tokenType()=="IDENTIFIER":
                self.out.write(f"<identifier> {self.b.current_token} </identifier>\n")
            
        self.out.write("</tokens>\n")
        self.out.close()
       
    def grammer(self):
        fu=CompilationEngine(self.fi,self.fe)
        fu.compileClass()
        
if __name__=="__main__":
    a=Jackanalyser()
    