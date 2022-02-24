from os.path import join, exists, abspath, dirname
from os import mkdir, system, environ, remove

required_modules = [
    "gitpython",
    "shutil",
    "tempfile"
]

def install_required_modules():
    for module in required_modules:
        system(f"python3 -m pip install {module}")

try:
    from tempfile import mkdtemp
    from shutil import rmtree, move
    from git import Repo
except ImportError:
    install_required_modules()
    from tempfile import mkdtemp
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

git_url = "https://github.com/DaMuffinDev/ezruh.git"

def clone(des, base_des=None):
    des = des if not base_des else f"{build_folder}/{des}"
    if exists(des):
        try: rmtree(des)
        except: remove(des)
    Repo.clone_from(git_url, des)

def clone_file(file_name, des):
    temporary_dir = mkdtemp()
    if exists(join(build_folder, temporary_dir)):
        rmtree(join(build_folder, temporary_dir))
    clone(temporary_dir, base_des=False)
    move(join(temporary_dir, file_name), des)
    try: rmtree(temporary_dir)
    except: return

def clone_folder(folder_name, des):
    temporary_dir = mkdtemp()
    if exists(join(build_folder, temporary_dir)):
        rmtree(join(build_folder, temporary_dir))
    clone(temporary_dir, base_des=False)
    move(join(temporary_dir, folder_name), des)
    try: rmtree(temporary_dir)
    except: return

def find(file):
    if file in required_files:
        return build_folder
    
    for folder in required_folders:
        if file in required_folders[folder]:
            return join(build_folder, folder)
    
    return join(build_folder, "broken")

def create_build_folder():
    if exists(build_folder): return
    mkdir(build_folder)

def build_required_files():
    clone(build_folder, base_des=False)
    for file in ["README.md", ".gitignore"]:
        remove(join(build_folder, file))

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
        if not exists(join(build_folder, folder)):
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
        modules = file.read().split("\n")

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
    print("Creating Ezruh Build Folder...")
    create_build_folder() # Create the ezruh program file
    print("Creating Ezruh Files...")
    build_required_files() # Create the required files
    print("Installing Dependencies...")
    install_required_modules() # Install required python modules
    print("Verifying Ezruh Build Folder...")
    if not verify_build_folder(): # Verify everything is installed
        print("Invalid Ezruh Build Folder...")
        print("Repairing Build Folder...")
        repair("build_folder")

if __name__ == "__main__":
    main()