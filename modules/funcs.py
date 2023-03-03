from pystyle import Colorate
import json
class printc():
    def __init__(self, default_color):
        self.print_color_default = default_color
    def init(self):
        return self.printc
    def printc(self,msg,color=None, endx='\n', label="[INFO]"):
        if not color:
            if self.print_color_default:
                print(Colorate.Horizontal(self.print_color_default, label), msg, end=endx)
            else:
                raise SyntaxError("No color gived")
        else:
            print(Colorate.Horizontal(color, label), msg, end=endx)
class info_pkgs_parser():
    def __init__(self, file):
        self.file = file
    
    def parse(self):
        content = open('test_info','r').read().splitlines()
        for x in content:
            split_symbol = x.find(":")
            if split_symbol == -1:
                raise SyntaxError(f"Error while parsing file: {x}, expected :")
            splited = [x[:split_symbol], x[split_symbol +1:]]
            if splited[0] == "Name":
                if splited[1][0:1] == " ":
                    splited[1] = splited[1][1:len(splited[1])]
                self.name = str(splited[1])
            if splited[0] == "Description":
                if splited[1][0:1] == " ":
                    splited[1] = splited[1][1:len(splited[1])]
                self.description = str(splited[1])
            if splited[0] == "Dependencies":
                self.dependencies = json.loads(splited[1])
            if splited[0] == "Version":
                self.version = float(splited[1])
        return (self.name, self.description, self.dependencies, self.version)
class querys:
    def __join(self, baseurl, file):
        if baseurl[len(baseurl) - 2:len(baseurl) - 1] == '/':
            return baseurl + file
        else:
            return baseurl + '/' + file
    def get_repo():
        open('modules/repo.json')
__all__ = ["finder.__finderstrict"]