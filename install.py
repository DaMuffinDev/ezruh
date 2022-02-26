from Resources._variables import rv_install, required, hash, float_numbers, \
    getitem_call, getitem_init, join_lists, mkfile, remove_spaces
from Resources.required_modules import pymodules
from os import environ, mkdir, listdir, remove, rmdir
from os.path import exists, join, isdir, isfile, basename
from subprocess import call as system
import platform
import sys

# Module Installation
python = sys.executable
modules = rv_install.Modules()

def install_module(module):
    system(f"{python} -m pip install {module}")
    modules.update()

def install_modules(modules):
    for module in modules:
        install_module(module)

pymodules.install(pymodules.presets.installer)

from git import Repo
from git.util import rmtree as git_rmtree
from shutil import move, rmtree

# -- END --

if platform.system() == "Windows":
    base_build_directory = join(environ["LOCALAPPDATA"], "Programs")
elif platform.system() == "Linux" or platform.system() == "Darwin":
    base_build_directory = "/usr/local"
build_folder = join(base_build_directory, "ezruh")

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

exec_required_path = join(build_folder, "exec_required.txt")

def update_required_exec_files():
    if exists(exec_required_path):
        with open(exec_required_path, "r") as file:
            return remove_spaces(file.read().split("\n")) 
    return []

required_exec_files = update_required_exec_files()

class __cleanup:
    __init__ = getitem_init
    __call__ = getitem_call

    class Exclude:
        def __init__(self, _list: list = None):
            self.__exclude = [] if _list is None else _list

        def get(self, item = None):
            return self.__exclude if item is None else self.__getitem__(item)

        def add(self, item):
            self.__exclude.append(item)
        
        def remove(self, index):
            del self.__exclude[index]

        def __getitem__(self, index):
            return self.__exclude[index]

def os_list_join(dir, _list: list):
    path_list = []
    for item in _list:
        path_list.append(join(dir, item))
    return path_list

@__cleanup
def cleanup(self, exclude=[]):
    cleanup_list = join_lists([
        os_list_join(build_folder, required_files), 
        os_list_join(build_folder, list(required_folders.keys())), 
        os_list_join(build_folder, exclude)
    ])
    for item in listdir(build_folder):
        item_dir = join_build_path(item)
        if not item_dir in cleanup_list:
            safe_remove(item_dir)

cleanup_exclude = cleanup.Exclude()
cleanup_exclude.add("exec_required.txt")

git_url = "https://github.com/DaMuffinDev/ezruh.git"
def clone(des):
    if exists(des):
        des = hash(f"{des}{__import__('random').choice(float_numbers)}")
    Repo.clone_from(git_url, des)
    git_rmtree(join(des, ".git"))
    return des

class __verification:
    __init__ = getitem_init
    __call__ = getitem_call

    def ezruh_folder(self):
        if not exists(build_folder):
            main()
    
    def ezruh_installed(self):
        if not exists(build_folder):
            return False

        required_exec_files = update_required_exec_files()

        required_items = join_lists([
            required_files,
            list(required_folders.keys()),
            cleanup_exclude.get(),
            required_exec_files
        ])

        found_items = 0
        for item in listdir(build_folder):
            item = basename(item)

            if item in required_items:
                found_items += 1
        
        return found_items == len(required_items)
    
    def required_modules(self):
        if modules.missing:
            return True
        return False

    class __build:
        __init__ = getitem_init
        __call__ = getitem_call

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
            
            return missing_folders

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

            return missing_files

    @__build
    def build(self):
        raise TypeError(f"{self} is not subscriptable.")

@__verification
def verify(self):
    """Used for verification of either (a) certain file(s) or folder(s)"""
    if not verify.build.files() or not verify.build.folders():
        return False
    return True

def join_build_path(item):
    return join(build_folder, item)

def safe_move(path, new_path, override=False):
    if exists(join(build_folder, basename(path))):
        if override:
            safe_remove(join(build_folder, basename(path)))
        else: return
    move(path, new_path)

def safe_remove(path):
    if exists(path):
        try:
            rmtree(path)
        except Exception:
            if isdir(path):
                rmdir(path)
            elif isfile(path):
                remove(path)

def move_dir_items(dirs, new_dir, override=False):
    for dir in dirs:
        safe_move(dir, new_dir, override=override)

# Repair
class __repair:
    __init__ = getitem_init
    __call__ = getitem_call

    def install_missing_modules(self):
        install_modules(modules.missing)

    class Queue:
        def __init__(self, initial_files: list | None = None, initial_folders: list | None = None):
            self.__files = [] if initial_files is None else initial_files
            self.__folders = [] if initial_folders is None else initial_folders
        
        def get(self, _list):
            return {
                "files": self.__files,
                "folders": self.__folders
            }[_list.lower()]
        
        def __add_files(self, items: list):
            for item in items:
                self.__files.append(item)
        
        def __add_folders(self, items: list):
            for item in items:
                self.__folders.append(item)

        def add(self, files=None, folders=None):
            if isinstance(files, list):
                self.__add_files(files)

            if isinstance(folders, list):
                self.__add_folders(folders)
        
        def remove(self, item, _list):
            if _list.lower() in ["files", "file"]:
                if item in self.__files:
                    self.__files.remove(item)
            elif _list.lower() in ["folders", "folder"]:
                if item in self.__folders:
                    self.__folders.remove(item)

        def clear(self, _list):
            if _list.lower() in ["files", "file"]:
                self.__files = []
            elif _list.lower() in ["folders", "folder"]:
                self.__folders = []

        def setup_for_processing(self):
            return {"files": self.__files, "folders": self.__folders}

@__repair
def repair(self, files=None, folders=None, queue=None):
    verify.ezruh_folder()

    def _repair(items):
        repair_dir = clone(join(build_folder, "_repair"))
        for item in listdir(repair_dir):
            if item in items:
                safe_move(join(repair_dir, item), build_folder, override=True)
        cleanup(cleanup_exclude.get())

    if queue is not None:
        files = queue["files"]
        folders = queue["folders"]
        
        _repair(join_lists([files, folders]))
        return
    
    if not files is None:
        _repair(files)
    
    if not folders is None:
        _repair(folders)
    cleanup(cleanup_exclude.get())

# Build
def create_build_folder():
    if exists(build_folder):
        safe_remove(build_folder)
    mkdir(build_folder)

def install_ezruh_build():
    if not exists(build_folder):
        create_build_folder()

    build_dir = clone(join(build_folder, "build"))
    files = os_list_join(build_dir, required_files)
    folders = os_list_join(build_dir, list(required_folders.keys()))
    move_dir_items(join_lists([files, folders]), build_folder, override=True)

    cleanup(cleanup_exclude.get())

def create_main_executable():
    verify.ezruh_folder()
    import PyInstaller.__main__

    dist_path = join(build_folder, "exec_dist")
    work_path = join(build_folder, "exec_build")

    safe_remove(dist_path)
    safe_remove(work_path)

    PyInstaller.__main__.run([
        "--distpath",
        dist_path,
        "--workpath",
        work_path,
        "--specpath",
        build_folder,
        join(build_folder, required.main),
        "--name",
        "Ezruh"
    ])

    if exists(exec_required_path):
        safe_remove(exec_required_path)
    mkfile(exec_required_path)

    with open(exec_required_path, "w") as file:
        for item in listdir(join(dist_path, "Ezruh")):
            new_item_dir, item_dir = join_build_path(item), join(join(dist_path, "Ezruh"), item)
            if exists(new_item_dir):
                safe_remove(new_item_dir)
            else:
                move(item_dir, build_folder)
                file.write(f"{item}\n")
                cleanup_exclude.add(item)
    cleanup(cleanup_exclude.get())

def main():
    if verify.ezruh_installed():
        return
    create_build_folder()
    install_ezruh_build()
    create_main_executable()
    
    if not verify.required_modules():
        install_modules(modules.missing)
    
    # Verify Installation
    missing_files = verify.build.files()
    missing_folders = verify.build.folders()
    
    if missing_files or missing_folders:
        repair_queue = repair.Queue()
        repair_queue.add(files=missing_files, folders=missing_folders)
        repair(queue=repair_queue.setup_for_processing())
    cleanup(cleanup_exclude.get()) # Making sure the ezruh build folder contains no unused files or folders

if __name__ == "__main__":
    main()