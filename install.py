from os import system, mkdir, environ, listdir, remove, rmdir, walk, chmod
from os.path import join, exists, isdir

def install_required_modules():
    for module in ["gitpython", "shutil"]:
        system(f"python3 -m pip install {module}")

try:
    from shutil import move, rmtree
    from git.util import rmtree as git_rmtree
    from git import Repo
except ImportError:
    install_required_modules()
    from shutil import move, rmtree
    from git.util import rmtree as git_rmtree
    from git import Repo

destination = join(environ["LOCALAPPDATA"], "Programs")
build_folder = join(destination, "ezruh")

required_folders = {
    "Modules": ["mailer.py", "text.py"],
    "Resources": ["Imports.py"],
    "Assets": ["ezruh.ico"]
}

required_files = [
    "main.py",
    "install.py",
    "requirements.txt",
    "LICENSE",
]

git_url = "https://github.com/DaMuffinDev/ezruh.git"

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
    clone(join(build_folder, "build"))
    for item in listdir(join(build_folder, "build")):
        move(join(join(build_folder, "build"), item), build_folder)

    for file in [".gitignore", "README.md"]:
        if exists(join(build_folder, file)):
            remove(join(build_folder, file))

class Verification:
    def __init__(self, getitem):
        self.__doc__ = getitem.__doc__

    class Build:
        def __init__(self, getitem):
            self.__doc__ = getitem.__doc__
        
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
    raise TypeError(f"{self} is not subscriptable.")

class Repair:
    def __init__(self, getitem, **kwargs):
        self.__doc__ = getitem.__doc__
        self.__getitem = getitem
    
    def __call__(self, file=None, folder=None, queue=None):
        self.__getitem(self, file=file, folder=folder, queue=queue)
    
    def reinstall(self):
        rmtree(build_folder)
        main()

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
            else:
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
        main()
        return
    
    repair_dir = join(build_folder, "_repair")
    if not queue is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, join_lists(queue["files"], queue["folders"]))
        
        for item in listdir(repair_dir):
            move(join(repair_dir, item), build_folder)
        
        if exists(repair_dir): 
            rmdir(repair_dir)
        return

    if not file is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, [file])

        move(join(repair_dir, file), build_folder)

        if exists(repair_dir): 
            rmdir(repair_dir)
    elif not folder is None:
        clone(repair_dir)
        remove_dir_items(repair_dir, [folder])
        move(join(repair_dir, folder), build_folder)

        if exists(repair_dir): 
            rmdir(repair_dir)

def main():
    # Setup the build folder
    # Install ezruh folders
    # Install ezruh files
    # Verify build folder
    # Install required modules
    create_build_folder()
    install_ezruh_build()
    folder_verification = verify.build.folders()
    file_verification = verify.build.files()

    repair_queue = repair.Queue()
    repair_queue.add_files(file_verification["data"])
    repair_queue.add_folders(folder_verification["data"])

    if not folder_verification["output"] or not file_verification["output"]:
        repair(queue=repair_queue.setup_for_processing())

if __name__ == "__main__":
    main()