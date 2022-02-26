from ._variables import rv_install, getitem_init, getitem_call
import subprocess
import sys

"""
[MODULES: TEXT]

from Resources.required_modules import pymodules
pymodules.install(pymodules.preset.modules("text"))

"""

class PyModuleObject:
    def __init__(self, modules):
        self.modules = modules
    
    def __is_pymodule__(self):
        return True

class _pymodules:
    __init__ = getitem_init
    __call__ = getitem_call

    def is_pymodule_object(self, _o):
        try:
            return _o.__is_pymodule__()
        except:
            return False

    def install(self, pymodule: object):
        if not self.is_pymodule_object(pymodule):
            return
        modules = rv_install.Modules()
        modules.set_required(pymodule.modules)
        if modules.missing:
            for module in modules.missing:
                subprocess.call(f"{sys.executable} -m pip install {module}")

    class _pymodule_preset:
        __init__ = getitem_init
        __call__ = getitem_call

        class _module_preset:
            __init__ = getitem_init
            __call__ = getitem_call

            _run = {}
        
        installer = ["GitPython"]

        @_module_preset
        def modules(self, script: str):
            self._run["text"] = ["pyautogui", "keyboard"]
            self._run["mailer"] = ["smtplib", "email", "ssl"]
            self._run["url"] = ["requests"]
            return PyModuleObject(self._run[script.lower()])
        
        @_module_preset
        def resources(self, script: str):
            self._run["imports"] = []
            self._run["presets"] = []
            return PyModuleObject(self._run[script.lower()])
        
        @_module_preset
        def storage(self, script: str):
            self._run["cryptography"] = []
            self._run["storage"] = []
            return PyModuleObject(self._run[script.lower()])

    @_pymodule_preset
    def presets(self):
        raise TypeError(f"{self} is not subscriptable.")

@_pymodules
def pymodules(self):
    raise TypeError(f"{self} is not subscriptable.")