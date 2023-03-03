import argparse, sys, os, requests
from modules.funcs import printc
from pystyle import Colors
parser = argparse.ArgumentParser(prog="dda", usage="Ayuda abajo", 
                        description="Antes llamado Descompresor De Archivos, ahora sera un gestor de paquetes")

parser.add_argument("-i", "--install", action="store", dest="inst_opt", help="Instala paquetes que especifiques")

objs = parser.parse_args()
cprint = printc(Colors.blue_to_purple).init()
if objs.inst_opt:
    cprint("Instalando {}...")