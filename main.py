import gi, threading, subprocess, requests, os, random, string, time, sys, tarfile

gi.require_versions({'Adw':'1', 'Gtk':'4.0', 'WebKit2':'5.0'})
from gi.repository import Gtk, Gdk, GLib, GObject, Adw, Gio, WebKit2
from xdg_base_dirs import xdg_cache_home
Adw.init()

class info_pkgs_parser():
    class info():
        def __init__(self, name, description, source_link, binary_link):
            self.name = name
            self.description = description
            self.source_link = source_link
            self.binary_link = binary_link
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
            if splited[0] == "SourceLink":
                if splited[1][0:1] == " ":
                    splited[1] = splited[1][1:len(splited[1])]
                self.source_link = str(splited[1])
            if splited[0] == "BinaryLink":
                if splited[1][0:1] == " ":
                    splited[1] = splited[1][1:len(splited[1])]
                self.binary_link = str(splited[1])
        try:
            return self.info(self.name, self.description, self.source_link, self.binary_link)
        except AttributeError:
            print("El archivo de informacion sobre el paquete esta corrupto/incompleto: ", sys.exc_info())

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='PyFileFinder')
        self.set_default_size(width=500, height=600)
        self.set_size_request(width=500, height=600)

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)
        self.init_webkit()
        
        self.set_child(self.scrolled_window)
    
    def init_webkit(self):
        self.webview = WebKit2.WebView()
        self.webview.connect("create", self.on_create)
        
        # Crea un objeto ScrolledWindow y agrega el WebView a él
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_child(self.webview)

        # Carga la página web en el WebView
        self.webview.load_uri("https://sites.google.com/view/archivedecompresor/p%C3%A1gina-principal")
        self.url = ""

    def on_create(self, webview, navigation_action):
        # Maneja la señal "create" del WebView
        self.url = navigation_action.get_request().get_uri()
        
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 12)
        self.horizontal_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 15)
        
        self.button = Gtk.Button.new_with_label("Descargar")
        self.progress = Gtk.ProgressBar.new()
        self.compiled_radio = Gtk.CheckButton.new_with_label(label="Descargar binarios")
        self.source_radio = Gtk.CheckButton.new_with_label(label="Descargar codigo fuente y compilar")
        self.text_view = Gtk.TextView.new()
        self.text_view_buffer = self.text_view.get_buffer()
        
        self.progress.set_show_text(True)
        self.horizontal_box.set_homogeneous(True)
        self.compiled_radio.set_group(self.source_radio)
        self.text_view_buffer.set_text("Que esta pasando")

        self.button.connect("clicked", self.button_clicked)

        self.horizontal_box.append(self.source_radio)
        self.horizontal_box.append(self.compiled_radio)
        self.box.append(self.progress)
        self.box.append(self.button)
        self.box.append(self.horizontal_box)
        self.box.append(self.text_view)

        self.set_child(self.box)

    def download_info_pkg(self, url):
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # tamaño de bloque en bytes
        downloaded_size = 0
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".cache"  # generar una cadena aleatoria de 10 caracteres
        self.home_temp_folder = str(xdg_cache_home())
        self.cache_file2 = os.path.join(self.home_temp_folder, name)

        with open(self.cache_file2, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded_size += len(data)
                progress = downloaded_size / total_size * total_size / total_size

                GLib.idle_add(self.progress.set_fraction, progress / 1)
                GLib.idle_add(self.progress.set_text, f"Descargado {downloaded_size} de un total de {total_size}")
                
        if not os.path.exists(self.cache_file2):
            print("No se pudo descargar la informacion del paquete")
            self.set_child(self.scrolled_window)
            return
        self.pkgs_info = info_pkgs_parser(self.cache_file2).parse()
        if self.source_radio.get_active():
            self.download_pkg(self.pkgs_info.source_link)
        elif self.compiled_radio.get_active():
            self.download_pkg(self.pkgs_info.binary_link)
    
    def download_pkg(self, url):
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # tamaño de bloque en bytes
        downloaded_size = 0
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".cache"  # generar una cadena aleatoria de 10 caracteres
        self.home_temp_folder = str(xdg_cache_home())
        self.cache_file = os.path.join(self.home_temp_folder, name)
        self.progress.set_fraction(0)
        with open(self.cache_file, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded_size += len(data)
                progress = downloaded_size / total_size * total_size / total_size
                GLib.idle_add(self.progress.set_fraction, progress)
                GLib.idle_add(self.progress.set_text, f"Descargado {downloaded_size} de un total de {total_size}")
        self.install_pkg()
    
    def install_pkg(self):
        # Descomprime el paquete
        with tarfile.open(self.cache_file, "r:gz") as file:
            name = os.path.join(self.home_temp_folder, os.path.splitext(os.path.split(self.cache_file)[1])[0])
            file.extractall(name)
        # Inicia el proceso y obtiene el objeto Popen
        proc = subprocess.Popen([os.path.join(name, "install.sh"), "source" if self.source_radio.get_active() else "binary"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.text_view_buffer.insert(self.text_view_buffer.get_end_iter(), "asd")
        # Itera sobre las líneas de salida del proceso mientras se ejecuta
        while True:
            # Lee una línea de salida del proceso-
            output = proc.stdout.readline()
            if not output:
                break
            # Imprime la línea de salida
            self.text_view_buffer.insert(self.text_view_buffer.get_end_iter(), output.strip().decode() + '\n')
            print("siguiendo en el loop")
        print("porque sales del loop")
        
    def button_clicked(self, button):
        threading.Thread(target=self.download_info_pkg, args=[self.url]).start()        


        #threading.Thread(target=self.download, args=[])
        print("chingado")
        
class MainApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.FileFinder.XtremeTHN",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = MainWindow(application=self)
        self.win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        try:
            os.remove(self.win.cache_file)
            os.remove(self.win.cache_file2)
        except:
            pass
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        print("adios")
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

MainApplication().run()