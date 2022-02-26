from ._variables import getitem_init, getitem_call

class _presets:
    class text:
        def __init__(self, getitem):
            getitem_init(self, getitem)

            class PresetObject:
                def __init__(self):
                    pass

            self.PresetObject = PresetObject

        __call__ = getitem_call
        
        def discord(self):
            return self.PresetObject()
    
    class required_modules:
        __init__ = getitem_init
        __call__ = getitem_call

        RESOURCES = ["PyQt5", "hashlib", "pkg_resources"]
        MODULES = "<preset.modules>"
        SCRIPTS = "<preset.scripts>"
        STORAGE = "<preset.storage>"
        ASSETS = "<preset.assets>"

@_presets.text
def text(self):
    raise TypeError(f"{self} is not subscriptable.")

@_presets.required_modules
def pymodules(self):
    raise TypeError(f"{self} is not subscriptable.")