import argparse, sys, os, requests
from modules.funcs import printc, pkgs_handler, jsonEx
from modules.funcs import querys as query
from pystyle import Colors
parser = argparse.ArgumentParser(prog="dda", usage="Ayuda abajo", 
                        description="Antes llamado Descompresor De Archivos, ahora sera un gestor de paquetes")

parser.add_argument("-i", "--install", action="store", dest="inst_opt", help="Instala paquetes que especifiques")
parser.add_argument("-gi", "--get-info", action="store", dest="pkg_info", help="Obtiene informacion del paquete que especifiques")

configs = jsonEx.get('modules/configs.json')
objs = parser.parse_args()
cprint = printc(Colors.blue_to_purple).init()
querys = query()

if objs.inst_opt:
    if pkgs_handler.is_installed(objs.inst_opt):
        cprint("El paquete ya esta instalado")
        sys.exit()
    repo = querys.get_repo()
    url_object, file = querys.find_pkg(objs.inst_opt)
    if isinstance(file, int):
        cprint("El paquete no ha sido encontrado")
        sys.exit(110)
    cprint(f"Descargando el paquete {objs.inst_opt}...")
    compressed_pkg = pkgs_handler.remote.download(url_object)
    cprint("Instalando el paquete...")
    pkgs_handler.remote.install(compressed_pkg, objs.inst_opt)
    cprint("Instalado!")

if objs.pkg_info:
    if pkgs_handler.is_installed(objs.pkg_info):
        info = pkgs_handler.info_pkgs_parser(configs['pkg_installed'][objs.pkg_info]).parse()
        print("Nombre:", info.name)
        print("Descripion:", info.description)
        print("Dependencias:")
        if info.dependencies['system']:
            print("     Administrador de paquetes del sistema:", info.dependencies['system'])
        if info.dependencies['pip']:
            print("     Administrador de paquetes pip:", info.dependencies['pip'])
        print("Version:", info.description)