import os
import PyInstaller.__main__
import shutil
from distutils.dir_util import copy_tree

# Opticos Program Builder

program_name = "oiw"
main = "main.py"
version = "alpha89"
icon = "assets/icon_centered.ico"
folders = ["assets", "ttkbootstrap"]



print("\nBuilding Dashboard...")
PyInstaller.__main__.run([
    f'{main}',
    f'-i={icon}',
    '-w',
    '-y',
    f'-n={program_name}'
])


print(f"\nCreating dist/{program_name}_{version}")
try:
    os.mkdir(f"dist/{program_name}_{version}")
except:
    print("Deleting Old Build")
    shutil.rmtree(f"dist/{program_name}_{version}")
    os.mkdir(f"dist/{program_name}_{version}")

print("Copying Assets...")

for folder in folders:
    print("Merging:", folder)
    shutil.copytree(folder, f"dist/{program_name}_{version}/" + str(folder))

print("Merging: Main...")
copy_tree(f"dist/{program_name}/", f"dist/{program_name}_{version}/")

#print("Merging: Service...")
#copy_tree("dist/GWSL_service/", f"dist/GWSL_{version}/")
