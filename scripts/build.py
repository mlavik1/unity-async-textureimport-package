import os, shutil, errno, sys

def build(build_folder):
  if os.path.exists(build_folder):
      shutil.rmtree(build_folder)
  os.mkdir(build_folder)
  os.chdir(build_folder)

  cmd_configure = """cmake ../FreeImage \
    -G"Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Release \
    -DFREEIMAGE_LIB=OFF \
    -DSUPPORT_FMT_TIFF=ON \
    -DSUPPORT_FMT_JPEG=ON""")

  os.system(cmd_configure)
  os.system("cmake --build .")

build("build")
