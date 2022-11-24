import os, shutil, errno, sys

def copy_filedir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

if len(sys.argv) > 1:
    unity_path = str(sys.argv[1])
else:
    print("ERROR: You need to pass the path to Unity editor executable.")
    exit()

nodisplay =  "-nodisplay" in sys.argv
package_name = 'UnityAsyncTextureImport.unitypackage'
plugin_folder_name = 'UnityAsyncTextureImport'
unity_project_dir = 'unity-async-textureimport'

export_project_path = "tmp-package-export"

if os.path.exists(export_project_path):
    shutil.rmtree(export_project_path)
os.mkdir(export_project_path)

assets = ["Assets", "ACKNOWLEDGEMENTS.txt", "ACKNOWLEDGEMENTS.txt", "LICENSE", "README.md", "FreeImage-license-GPLv3"]

for asset in assets:
    src_asset = os.path.join(unity_project_dir, asset)
    dest_asset = os.path.join(export_project_path, "Assets", plugin_folder_name, asset)
    copy_filedir(src_asset, dest_asset)

# Copy binaries
freeImage_bin_dir = os.path.join(export_project_path, "Assets", plugin_folder_name, "Assets", "Plugins", "FreeImage")
os.mkdir(os.path.join(freeImage_bin_dir, "Android"))
os.mkdir(os.path.join(freeImage_bin_dir, "Android", "arm64-v8a"))
copy_filedir(os.path.join("binaries", "arm64-v8a", "libFreeImage.so"), os.path.join(freeImage_bin_dir, "Android", "arm64-v8a", "libFreeImage.so"))
os.mkdir(os.path.join(freeImage_bin_dir, "Android", "armeabi-v7a"))
copy_filedir(os.path.join("binaries", "armeabi-v7a", "libFreeImage.so"), os.path.join(freeImage_bin_dir, "Android", "armeabi-v7a", "libFreeImage.so"))
#os.mkdir(os.path.join(freeImage_bin_dir, "Linux"))
copy_filedir(os.path.join("binaries", "linux", "libFreeImage.so"), os.path.join(freeImage_bin_dir, "Linux", "libFreeImage.so"))
# Copy meta files
shutil.copy(os.path.join("bin-meta", "arm64-v8a.meta"), os.path.join(freeImage_bin_dir, "Android", "arm64-v8a", "libFreeImage.so.meta"))
shutil.copy(os.path.join("bin-meta", "armeabi-v7a.meta"), os.path.join(freeImage_bin_dir, "Android", "armeabi-v7a", "libFreeImage.so.meta"))
shutil.copy(os.path.join("bin-meta", "linux.meta"), os.path.join(freeImage_bin_dir, "Linux", "libFreeImage.so.meta"))

command_string = "\"{unity_path}\" -projectPath {project_path} -exportPackage Assets {package_name} -batchmode -nographics -silent-crashes -quit".format(unity_path=unity_path, project_path=export_project_path, package_name=package_name)
# Run through cvfb if no display available (building in container, etc.).
if nodisplay:
    command_string = "xvfb-run --auto-servernum --server-args=\'-screen 0 640x480x24\' " + command_string
print(command_string)
os.system(command_string)

shutil.copy(os.path.join(export_project_path, package_name), package_name)

shutil.rmtree(export_project_path)
