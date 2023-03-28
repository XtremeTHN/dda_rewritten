#!/usr/bin/env python3
import os, sys, toml, sys, tarfile, shutil
from colorama import Fore, Style

INFO_TEMPLATE = """Name: {}
Description: {}
SourceLink: {}
BinaryLink: {}"""

INSTALL_SCRIPT_TEMPLATE = """#!/bin/bash
if [ "$1" == "binary" ]; then
    echo :::: Installing binary
    mv {} ~/.local/bin
    chmod +x ~/.local/bin/{}
    exit 0
fi

if [ "$1" == "source" ]; then
    echo :::: Compiling...
    cargo build
    mv {} ~/.local/bin
    chmod +x ~/.local/bin/{}
fi
"""

def printc(*values, label=f"{Fore.GREEN}{Style.BRIGHT}::::{Style.RESET_ALL}", endx='\n'):
    temp_list = ['"{}"'.format(elem) for elem in values]
    exec("print('{}', {},end=endx)".format(label, ', '.join(temp_list)))

def inputc(msg, label=f"{Fore.GREEN}{Style.BRIGHT}::{Style.RESET_ALL}"):
    print(label, msg, end='')
    return input()

def question():
    try:
        choice = input()
    except (KeyboardInterrupt, EOFError):
        sys.exit(1)
    if choice not in ['S', 'N']:
        printc("Porfavor, escriba un caracter valido (S/N): ", endx='')
        question()
    else:
        return choice == 'S'
    
class Analize:
    def proyect():
        if not os.path.exists("Cargo.toml"):
            # Si no existe el archivo toml de rust, significa que es un proyecto de python
            if not os.path.exists("PKGINFO.toml"):
                return -1, -1, -1
            with open('PKGINFO.toml') as file:
                toml_data = toml.load(file)
            return toml_data['bin']['name'], toml_data['bin']['path']
        # En caso contrario de que exista, entonces es un proyecto de rust
        with open("Cargo.toml") as file:
            toml_data = toml.load(file)
        return toml_data['package']['name'], toml_data["bin"][0]["name"] ,toml_data['bin'][0]['path']

class GenerateFuncs:
    def generate_pkg(name, bin_name, path):
        description = inputc("Porfavor, describa su proyecto detalladamente: ")
        printc("Generando paquetes...")
        if not os.path.exists('Cargo.toml'):
            if os.path.exists('main.py'):
                printc("Proyecto python detectado")
                with tarfile.open(f"{name}_x86_64-src.tar.gz", 'w:gz') as tar:
                    tar.add("main.py")
                    if path:
                        for x in path:
                            tar.add(x)
                shutil.copy(f"{name}_x86_64-src.tar.gz", f"{name}_x86_64-bin.tar.gz")
            else:
                printc("No se pudo detectar en que lenguaje esta escrito el proyecto", label=f"{Fore.RED}{Style.BRIGHT}::::{Style.RESET_ALL}")
                sys.exit(2)
        else:
            if not os.path.exists(path):
                printc("No se pudo saber si el archivo principal de rust existe, intenta comprobar el archivo Cargo.toml", label=f"{Fore.RED}{Style.BRIGHT}::::{Style.RESET_ALL}")
                sys.exit(3)
            printc("Compilando...")
            exit_code = os.system("cargo build")
            if exit_code > 0:
                printc(f"No se pudo compilar el proyecto. Codigo de error de cargo: {exit_code}")
                sys.exit(exit_code)
            shutil.move(f"target/debug/{bin_name}", os.getcwd())
            dirs = inputc("Escribe directorios/ficheros extra (separados por comas) para agregar al paquete del codigo fuente: ").split(',')
            with tarfile.open(f"{name}_x86_64-src.tar.gz", 'w:gz') as tar:
                tar.add(path)
                if dirs[0] != '':
                    for x in dirs:
                        tar.add(x)
                        
            dirs = inputc("Escribe directorios/ficheros extra (separados por comas) para agregar al paquete del codigo compilado: ").split(',')
            with tarfile.open(f"{name}_x86_64-bin.tar.gz", 'w:gz') as tar:
                tar.add(bin_name)
                if dirs[0] != '':
                    for x in dirs:
                        tar.add(x)
                
        printc(f"Sube los paquetes {name}_x86_64-src.tar.gz y {name}_x86_64-bin.tar.gz a un servidor en donde el link de descarga sea directo y pega los links respectivos de cada paquete abajo")
        source_link = inputc("Link del codigo fuente: ")
        binary_link = inputc("Link del codigo compilado (binarios): ")
        printc("Generando informacion del paquete...")
        GenerateFuncs.generate_pkg_info(name, description, source_link, binary_link)
            
    def generate_pkg_info(name, description, src_link, bin_link):
        with open(name+".info", 'w') as file:
            file.write(INFO_TEMPLATE.format(name, description, src_link, bin_link))
         
printc("Analizando proyecto...")
rust = True
python = False
name, bin_name, path = Analize.proyect()
if name == -1:
    printc("No se pudo detectar el archivo de configuracion", label=f"{Fore.RED}{Style.BRIGHT}::::{Style.RESET_ALL}")
    sys.exit(4)
    
printc(f"'{name}'", "es el nombre del proyecto")
printc("Esto es correcto? (S/N): ", endx='')
if not question():
    name = inputc("Escribe el nombre del proyecto: ")

printc("Generando paquete...")
GenerateFuncs.generate_pkg(name, bin_name, path)
