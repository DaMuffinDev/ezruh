from os import mkdir, environ, listdir, remove, rmdir
from os.path import join, exists, isdir, isfile
from Resources._variables import required
from subprocess import call as system
import platform

def install_required_modules():
    pyinstaller = ["PyInstaller", "https://github.com/pyinstaller/pyinstaller/archive/develop.zip"]
    required_modules = [
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
    ]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            system(f"python -m pip install {module}")

try:
    from shutil import move, rmtree
    from git.util import rmtree as git_rmtree
    from git import Repo
except ImportError:
    install_required_modules()
    from shutil import move, rmtree
    from git.util import rmtree as git_rmtree
    from git import Repo

if platform.system() == "Windows":
    destination = join(environ["LOCALAPPDATA"], "Programs")
elif platform.system() == "Linux" or platform.system() == "Darwin":
    destination = "/usr/local"
build_folder = join(destination, "ezruh")

required_folders = {
    required.modules(): [
        required.modules.mailer,
        required.modules.text,
        required.modules.url
    ],
    required.resources(): [
        required.resources.variables,
        required.resources.imports,
        required.resources.presets
    ],
    required.assets(): [
        required.assets.ezruh
    ],
    required.scripts(): [
        required.scripts.beemovie,
        required.scripts.onemillionpi,
        required.scripts.pacertest
    ]
}

required_files = [
    required.main,
    required.install,
    required.requirements,
    required.license,
]

git_url = "https://github.com/DaMuffinDev/ezruh.git"

def get_requirements():
    with open(required.requirements, "r") as file:
        return file.read()

def remove_git(dir):
    git_rmtree(join(dir, ".git"))

def clone(des):
    if exists(des):
        return
    Repo.clone_from(git_url, des)
    remove_git(des)

def create_build_folder(override=False):
    if exists(build_folder): 
        if not override: return
        rmtree(build_folder)
    mkdir(build_folder)

def install_ezruh_build():
    tempo_build = join(build_folder, "build")
    clone(tempo_build)
    for item in listdir(tempo_build):
        move(join(tempo_build, item), build_folder)

    for file in [".gitignore", "README.md"]:
        file_path = join(build_folder, file)
        if exists(file_path):
            remove(file_path)
    
    for item in listdir(build_folder):
        if not item in [*required_files, *list(required_folders.keys())]:
            if isfile(item):
                try: remove(item)
                except Exception: pass
            elif isdir(item):
                try: rmtree(item)
                except Exception: pass
    create_main_executable()

class Verification:
    def __init__(self, getitem):
        self._getitem = getitem
        self.__doc__ = getitem.__doc__

    def __call__(self):
        self._getitem(self)

    class Build:
        def __init__(self, getitem):
            self.__doc__ = getitem.__doc__
        
        def required_modules(self):
            required_modules = get_requirements().split("\n")
            for module in required_modules:
                try:
                    __import__(module)
                except ImportError:
                    return False
            return True
        
        def module(self, module):
            try:
                __import__(module)
                return True
            except ImportError:
                return False

        def get_folders(self):
            found_folders = []
            for folder in listdir(build_folder):
                if isdir(folder):
                    found_folders.append(folder)
            return found_folders

        def folder(self, name):
            return name in self.get_folders()
        
        def folders(self):
            found_folders, missing_folders = self.get_folders(), []
            
            for folder in required_folders:
                if not folder in found_folders:
                    missing_folders.append(folder)
            
            return {"output": len(missing_folders) == 0, "data": missing_folders}

        def get_files(self):
            found_files = []
            for file in listdir(build_folder):
                if not isdir(file):
                    found_files.append(file)
            return found_files
        
        def file(self, name):
            return name in self.get_files()
        
        def files(self):
            found_files, missing_files = self.get_files(), []

            for file in required_files:
                if not file in found_files:
                    missing_files.append(file)

            return {"output": len(missing_files) == 0, "data": missing_files}

    @Build
    def build(self):
        raise TypeError(f"{self} is not subscriptable.")

@Verification
def verify(self):
    """Used for verification of either (a) certain file(s) or folder(s)"""
    if not verify.build.files() or not verify.build.folders():
        return False
    return True

class Repair:
    def __init__(self, getitem, **kwargs):
        self.__doc__ = getitem.__doc__
        self.__getitem = getitem
    
    def __call__(self, file=None, folder=None, queue=None):
        self.__getitem(self, file=file, folder=folder, queue=queue)

    def cleanup(self):
        try:
            rmtree(join(build_folder, "_repair"))
        except Exception:
            pass

        if exists(join(build_folder, ".git")):
            remove_git(build_folder)
        
        for file in listdir(build_folder):
            if isfile(file) and not file in required_files:
                try:
                    remove(file)
                except Exception:
                    pass

    def reinstall(self):
        try:
            rmtree(build_folder)
        except:
            pass
        main()
    
    def install_module(self, module):
        system(f"python -m pip install {module}")

    def install_missing_modules(self):
        required_modules = get_requirements().split("\n")
        missing_modules = []
        for module in required_modules:
            if not verify.build.module(module):
                missing_modules.append(module)
        
        for module in missing_modules:
            self.install_module(module)

    class Queue:
        def __init__(self):
            self.__file_queue = []
            self.__folder_queue = []

            class QueueFolderObject:
                queue_object = True
                def __init__(self, folders):
                    self.folders = folders
                
            class QueueFileObject:
                queue_object = True
                def __init__(self, files):
                    self.files = files
            
            self.QueueFileObject = QueueFileObject
            self.QueueFolderObject = QueueFolderObject
        
        def get_files(self):
            return self.QueueFileObject(self.__file_queue)
        
        def get_folders(self):
            return self.QueueFolderObject(self.__folder_queue)
        
        def add(self, files, folders):
            if len(files) > 0: self.add_files(files)
            if len(folders) > 0: self.add_folders(folders)
        
        def add_file(self, file):
            self.__file_queue.append(file)
        
        def add_folder(self, folder):
            self.__folder_queue.append(folder)
        
        def add_folders(self, folders):
            if not isinstance(folders, list): return

            for folder in folders:
                self.add_folder(folder)

        def add_files(self, files):
            if not isinstance(files, list): return

            for file in files:
                self.add_file(file)
        
        def remove_file(self, file):
            if file in self.__file_queue:
                self.__file_queue.remove(file)
        
        def remove_folder(self, folder):
            if folder in self.__folder_queue:
                self.__folder_queue.remove(folder)

        def clear_folder(self):
            self.__folder_queue = []
        
        def clear_file(self):
            self.__file_queue = []
        
        def clear(self):
            self.clear_file()
            self.clear_folder()
        
        def setup_for_processing(self):
            return self.conjoin({"type": "folders", "data": self.__folder_queue}, {"type": "files", "data": self.__file_queue})
        
        def conjoin(self, folders, files):
            return {"files": files, "folders": folders}

def remove_dir_items(path, exclude=[]):
    for item in listdir(path):
        if not item in exclude:
            if isdir(item):
                rmtree(join(path, item))
            elif isfile(item):
                remove(join(path, item))

def join_lists(list1, list2):
    new_list = []
    for item in list1:
        new_list.append(item)
    
    for item in list2:
        new_list.append(item)
    return new_list

@Repair
def repair(self, file=None, folder=None, queue=None):
    if not exists(build_folder):
        self.cleanup()
        main()
        return
    
    repair_dir = join(build_folder, "_repair")
    if not queue is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, join_lists(queue["files"], queue["folders"]))
        
        for item in listdir(repair_dir):
            new_dir = join(build_folder, item)
            if exists(new_dir):
                rmtree(new_dir)
            move(join(repair_dir, item), build_folder)
        
        if exists(repair_dir): 
            rmdir(repair_dir)
        self.cleanup()
        return

    if not file is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, [file])
        new_dir = join(repair_dir, file)
        if exists(new_dir):
            rmtree(new_dir)
        move(new_dir, build_folder)

        if exists(repair_dir): 
            rmdir(repair_dir)
        self.cleanup()
    elif not folder is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, [folder])
        new_dir = join(repair_dir, folder)
        if exists(new_dir):
            rmtree(new_dir)
        move(new_dir, build_folder)

        if exists(repair_dir): 
            rmdir(repair_dir)
        self.cleanup()

cleanup_exclude = ["Ezruh.exe"]
def create_main_executable():
    import PyInstaller.__main__
    PyInstaller.__main__.run([
        "--distpath",
        join(build_folder, "dist"),
        "--workpath",
        join(build_folder, "build"),
        "--specpath",
        build_folder,
        join(build_folder, required.main),
        "--name",
        "Ezruh"
    ])
    build_dir = join(build_folder, "dist\\Ezruh")
    for item in listdir(build_dir):
        move(join(build_dir, item), build_folder)
        cleanup_exclude.append(item)
    
    mainpy = join(build_folder, required.main)
    if exists(mainpy):
        remove(mainpy)
    repair.cleanup()

def cleanup():
    for item in listdir(build_folder):
        if not item in join_lists(join_lists(required_files, list(required_folders.keys())), cleanup_exclude):
            item_dir = join(build_folder, item)
            try:
                rmtree(item_dir)
            except:
                if isdir(item_dir):
                    rmdir(item_dir)
                elif isfile(item_dir):
                    remove(item_dir)

def main():
    if exists(build_folder):
        try:
            rmtree(build_folder)
        except:
            pass
    create_build_folder() # Create build folder
    install_ezruh_build() # Install files and folders
    install_required_modules() # Install required modules
    # Verify ezruh build folder
    folder_verification = verify.build.folders()
    file_verification = verify.build.files()

    repair_queue = repair.Queue()
    repair_queue.add(files=file_verification["data"], folders=folder_verification["data"])

    if not folder_verification["output"] or not file_verification["output"]:
        repair(queue=repair_queue.setup_for_processing())
    cleanup()

if __name__ == "__main__":
    main()