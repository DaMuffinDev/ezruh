from os.path import join, exists, abspath, dirname
from os import mkdir, system, environ

required_modules = [
    "gitpython",
    "shutil"
]

def install_required_modules():
    for module in required_modules:
        system(f"python3 -m pip install {module}")

try:
    from shutil import rmtree
    from git import Repo, move
except ImportError:
    install_required_modules()
    from shutil import rmtree, move
    from git import Repo

here = abspath(dirname(__file__))
destination = join(environ["LOCALAPPDATA"], "Programs")
build_folder = join(destination, "ezruh")

required_folders = {
    "Assets": ["ezruh.ico"],
    "Modules": ["mailer.py", "text.py"],
    "Resources": ["Imports.py"]
}

required_files = [
    "install.py",
    "main.py",
    "requirements.txt",
    "LICENSE"
]

git_url = "https://github.com/DaMuffinDev/ezruh"

def clone(des):
    Repo.clone_from(git_url, f"{build_folder}/{des}")

def clone_file(file_name, des):
    temporary_repo = f"./ezruh_{file_name}"
    clone(temporary_repo)
    move(join(temporary_repo, file_name), des)
    rmtree(temporary_repo)

def clone_folder(folder_name, des):
    temporary_repo = f"./ezruh_{folder_name}"
    clone(temporary_repo)
    move(join(temporary_repo, folder_name), des)
    rmtree(temporary_repo)

def find(file):
    if file in required_files:
        return build_folder
    
    for folder in required_folders:
        if file in required_folders[folder]:
            return join(build_folder, folder)
    
    return join(build_folder, "broken")

def create_build_folder():
    mkdir(build_folder)

def build_required_files():
    for file in required_files:
        clone(file)

def verify_build_file(des):
    if not exists(build_folder):
        return False
    
    if not exists(join(build_folder, des)):
        return False
    
    return True

def verify_build_folder(folder=None):
    if not exists(build_folder):
        return False
    
    if not folder is None:
        if not exists(build_folder, folder):
            return False
        return True
    
    for file in required_files:
        if not verify_build_file(file):
            return False
    
    for folder in required_folders.keys():
        if not exists(join(build_folder, folder)):
            return False
        for file in required_folders[folder]:
            if not exists(join(join(build_folder, folder), file)):
                return False
    return True

def install_required_modules():
    with open(join(build_folder, "requirements.txt"), "r") as file:
        modules = file.read().split("\n").remove("")

    for module in modules:
        system(f"python3 -m pip install {module}")

def repair(obj, des=None):
    if obj == "build_folder":
        if exists(build_folder): rmtree(build_folder)
        main()
        return
    
    if obj in required_files:
        if des is None:
            des = find(obj)
        clone_file(obj, join(build_folder, des))
        return
    
    def __module_repair():
        clone_folder("Module", build_folder)
    
    def __asset_repair():
        clone_folder("Assets", build_folder)
    
    def __resource_repair():
        clone_folder("Resources", build_folder)

    {
        "Modules": __module_repair,
        "Assets": __asset_repair,
        "Resources": __resource_repair
    }[obj]()

def main():
    create_build_folder() # Create the ezruh program file
    build_required_files() # Create the required files
    install_required_modules() # Install required python modules
    if not verify_build_folder(): # Verify everything is installed
        repair("build_folder")

if __name__ == "__main__":
    main()