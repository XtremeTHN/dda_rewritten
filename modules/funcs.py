from pystyle import Colorate
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

__all__ = ["finder.__finderstrict"]