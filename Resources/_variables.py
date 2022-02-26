from hashlib import sha256
import pkg_resources

float_numbers = [
    0.01, 0.02, 0.03, 0.04, 0.05, 
    0.06, 0.07, 0.08, 0.09, 0.09, 
    0.1, 0.11, 0.12, 0.13, 0.15, 
    0.16, 0.17, 0.18, 0.19, 0.2, 
    0.21, 0.22, 0.23, 0.24, 0.25, 
    0.26, 0.27, 0.28, 0.29, 0.3, 
    0.31, 0.32, 0.33, 0.34, 0.35, 
    0.36, 0.37, 0.38, 0.39, 0.4, 
    0.41, 0.42, 0.43, 0.44, 0.45, 
    0.46, 0.47, 0.48, 0.49, 0.5, 
    0.51, 0.52, 0.53, 0.54, 0.55, 
    0.56, 0.57, 0.58, 0.59, 0.6, 
    0.61, 0.62, 0.63, 0.64, 0.65, 
    0.66, 0.67, 0.68, 0.69, 0.7, 
    0.71, 0.72, 0.73, 0.74, 0.75, 
    0.76, 0.77, 0.78, 0.79, 0.8, 
    0.81, 0.82, 0.83, 0.84, 0.85, 
    0.86, 0.87, 0.88, 0.89, 0.9, 
    0.91, 0.92, 0.93, 0.94, 0.95, 
    0.96, 0.97, 0.98, 0.99, 1.0
]

def hash(text):
    return sha256(text.encode()).hexdigest()

def join_lists(lists: list):
    joined_list = []
    for list in lists:
        for value in list:
            joined_list.append(value)
    return joined_list

def getitem_init(self, getitem):
    self._getitem = getitem
    self.__doc__ = getitem.__doc__

def getitem_call(self, *args, **kwargs):
    self._getitem(self, *args, **kwargs)

# Installer Variables
class _installer_variables:
    __init__ = getitem_init
    __call__ = getitem_call

    main = "main.py"
    install = "install.py"
    requirements = "requirements.txt"
    license = "LICENSE"

    class _resources:
        __init__ = getitem_init
        __call__ = lambda *args, **kwargs: "Resources"
        variables = "_variables.py"
        imports = "Imports.py"
        presets = "Presets.py"
    
    class _modules:
        __init__ = getitem_init
        __call__ = lambda *args, **kwargs: "Modules"
        mailer = "mailer.py"
        text = "text.py"
        url = "url.py"
    
    class _assets:
        __init__ = getitem_init
        __call__ = lambda *args, **kwargs: "Assets"
        ezruh = "ezruh.ico"
    
    class _scripts:
        __init__ = getitem_init
        __call__ = lambda *args, **kwargs: "Scripts"
        beemovie = "beemove.txt"
        onemillionpi = "onemillionpi.txt"
        pacertest = "pacertest.txt"
    
    class _storage:
        __init__ = getitem_init
        __call__ = lambda *args, **kwargs: "Storage"
        
        class _data:
            __init__ = getitem_init
            __call__ = lambda *args, **kwargs: "Data"
        
        @_data
        def data(self):
            return "Data"
        
        storage = "_storage.py"
        cryptography = "_cryptography.py"
    
    @_resources
    def resources(self):
        return "Resources"
    
    @_modules
    def modules(self):
        return "Modules"
    
    @_assets
    def assets(self):
        return "Assets"
    
    @_scripts
    def scripts(self):
        return "Scripts"
    
    @_storage
    def storage(self):
        return "Storage"

@_installer_variables
def required(self):
    raise TypeError(f"{self} is not subscriptable")

class _install:
    __init__ = getitem_init
    __call__ = getitem_call

    class Modules:
        def __init__(self):
            pyinstaller = ["PyInstaller", "https://github.com/pyinstaller/pyinstaller/archive/develop.zip"]
            self.required = set([
                "setuptools",
                "wheel",
                "gitpython",
                "pyautogui",
                "keyboard",
                "PyQt5",
                "email",
                "ssl",
                pyinstaller[0],
                pyinstaller[1]
            ])
            self.installed = {}
            self.missing = {}

            self.update() # updates missing and installed modules
        
        def set_required(self, modules: list):
            self.required = set(modules)

        def update(self):
            self.update_installed()
            self.update_missing()

        def update_missing(self):
            missing = []
            for item in self.required:
                if not self.is_installed(item):
                    missing.append(item)
            self.missing = set(missing)
        
        def update_installed(self):
            self.installed = {pkg.key for pkg in pkg_resources.working_set}
        
        def is_installed(self, module):
            return module in self.installed

@_install
def install(self):
    raise TypeError(f"{self} is not subscriptable.")
