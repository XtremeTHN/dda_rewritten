import argparse, sys, os, threading, time
from modules.funcs import printc, pkgs_handler, jsonEx
from modules.funcs import querys as query
from pystyle import Colors
from progress import spinner

parser = argparse.ArgumentParser(prog="dda", usage="Ayuda abajo", 
                        description="Antes llamado Descompresor De Archivos, ahora sera un gestor de paquetes")

parser.add_argument("-i", "--install", action="store", dest="inst_opt", help="Instala paquetes que especifiques")
parser.add_argument("--reinstall", action="store_true", dest="reinst_opt", help="Reinstala un paquete")
parser.add_argument("-ui", "--uninstall", action="store", dest="uninstall", help="Desinstala el paquete que especifiques")
parser.add_argument("-gi", "--get-info", action="store", dest="pkg_info", help="Obtiene informacion del paquete que especifiques")
parser.add_argument("-s", "--start", nargs="*", dest="name", help="Ejecuta el programa especificado")

objs = parser.parse_args()
cprint, c_format = printc(Colors.blue_to_purple).init()
querys = query()

if objs.inst_opt:
    if querys.code == -1:
        cprint("Ha habido un error al intentar conectarse a internet. Vuelve a abrir mas tarde")
        sys.exit()
    if not objs.reinst_opt:
        if pkgs_handler.is_installed(objs.inst_opt):
            cprint("El paquete ya esta instalado")
            sys.exit()
    repo = querys.get_repo()
    url_object, file = querys.find_pkg(objs.inst_opt)
    if isinstance(file, int):
        cprint("El paquete no ha sido encontrado")
        sys.exit(110)
    cprint(f"Descargando el paquete {objs.inst_opt}...")
    compressed_pkg = pkgs_handler.remote.download(url_object,c_format)
    cprint(f"Instalando...")
    pkgs_handler.remote.install(compressed_pkg, objs.inst_opt, c_format)
    configs = jsonEx.get('modules/configs.json')
    alias = pkgs_handler.info_pkgs_parser(configs['pkg_installed'][objs.inst_opt]).parse().alias
    cprint("Creando acceso directo...")
    pkgs_handler.remote.shortcut_new(objs.inst_opt, alias)
    cprint("Instalado!")

if objs.uninstall:
    configs = jsonEx.get('modules/configs.json')
    if pkgs_handler.is_installed(objs.uninstall):
        info = pkgs_handler.info_pkgs_parser(configs['pkg_installed'][objs.uninstall]).parse()
        
        thread = threading.Thread(target=pkgs_handler.uninstall, args=[objs.uninstall, info.alias])
        spin = spinner.Spinner(c_format("Desinstalando... "))
        thread.start()
        spin.start()
        while thread.is_alive():
            spin.next()
            time.sleep(0.1)
        cprint("Desinstalado correctamente!", label="\n[INFO]")

if objs.pkg_info:
    configs = jsonEx.get('modules/configs.json')
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
    else:
        cprint("El paquete no existe")