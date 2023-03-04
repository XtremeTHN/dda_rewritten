from pystyle import Colorate
from random import randrange
from tqdm import tqdm
import json, requests, os, sys, math, tarfile
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

    def format_c(self,msg,color=None, endx='\n', label="[INFO]"):
        if not color:
            if self.print_color_default:
                return Colorate.Horizontal(self.print_color_default, label) + ' ' + msg
            else:
                raise SyntaxError("No color gived")
        else:
            print(Colorate.Horizontal(color, label), msg, end=endx)
    
class querys():
    def __init__(self) -> None:
        self.repo = None

    def __join(self,baseurl, file) -> str:
        if baseurl[len(baseurl) - 2:len(baseurl) - 1] == '/':
            return baseurl + file
        else:
            return baseurl + '/' + file
        
    def get_repo(self,repo="https://raw.githubusercontent.com/XtremeTHN/dda_rewritten/main/modules/repo.json") -> dict | int:
        file = requests.get(repo)
        try:
            self.repo = json.loads(file.content.decode('utf-8'))
            file.close()
            return json.loads(file.content.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return file.status_code
    
    def find_pkg(self,name) -> str | int:
        if name in self.repo['files']:
            pkg = self.__join(self.repo['base_url'], self.repo['files'][name])
            return (requests.get(pkg), pkg)
        else:
            return (None, -1)

class jsonEx:
    """
        Clase para dar soporte a los archivos de configuracion y la base de datos que contiene las extensiones
    """
    def update_json(filex,data) -> None:
        """
            Actualiza los datos de un archivo json. No devuelve nada
            filex: Archivo json
            data: Diccionario con configuraciones adentro
        """
        with open(filex,'w') as file:
            json.dump(data, file, indent=4)
        
    def get(filex) -> dict:
        """
            Obtiene los datos de un archivo json. Devuelve dict
            filex: Archivo json
        """
        with open(filex,'r') as file:
            return json.load(file)

class pkgs_handler:
    class remote:
        def download(pkg: requests.Response, path=os.path.join(os.getenv('HOME'), '.local', 'share', 'apps')) -> str:
            total_size = int(pkg.headers.get("content-length", 0))
            block_size = 1024
            wrote = 0
            name = str(randrange(0,190283123)) + '.tmp'
            path = os.path.join(os.getenv('HOME'),'.temp', 'com.dda.python.XtremeTHN', name)
            os.system(f"mkdir -p {os.path.join(os.getenv('HOME'),'.temp', 'com.dda.python.XtremeTHN')}")
            with open(path, "wb") as f:
                for data in tqdm(pkg.iter_content(block_size), total=math.ceil(total_size//block_size), unit="KB", unit_scale=True, desc="Descargando"):
                    wrote = wrote + len(data)
                    f.write(data)
            return path

        def install(pkg_path: str, pkg_name: str, path=os.path.join(os.getenv('HOME'), '.local', 'share', 'apps')) -> None:
            configs = jsonEx.get('modules/configs.json')
            dest = os.path.join(path, pkg_name)
            os.makedirs(dest, exist_ok=True)
            with tarfile.open(pkg_path, 'r') as file:
                progress = tqdm(file.getmembers())
                for member in progress:
                    file.extract(member, path=dest)
                    progress.set_description("Extrayendo paquete...")
                    progress.update(member.size)
                progress.close()
            configs['pkg_installed'][pkg_name] = os.path.join(dest, 'pkg.info')
            jsonEx.update_json('modules/configs.json', configs)
            
    class info_pkgs_parser():
        class info():
            def __init__(self, name, description, dependencies, version):
                self.name = name
                self.description = description
                self.dependencies = dependencies
                self.version = version
        def __init__(self, file: str):
            self.file = file
        
        def parse(self):
            content = open(self.file,'r').read().splitlines()
            for x in content:
                split_symbol = x.find(":")
                if split_symbol == -1:
                    raise SyntaxError(f"Error mientras se analizaba el archivo de informacion del paquete: {x}, esperado :")
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
            return self.info(self.name, self.description, self.dependencies, self.version)
    
    def is_installed(pkg_name):
        return pkg_name in jsonEx.get('modules/configs.json')['pkg_installed']
__all__ = ["finder.__finderstrict"]