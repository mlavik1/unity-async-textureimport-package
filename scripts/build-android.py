import os, shutil, errno, sys

def build(build_folder, abi):
  if os.path.exists(build_folder):
      shutil.rmtree(build_folder)
  os.mkdir(build_folder)
  os.chdir(build_folder)

  if len(sys.argv) > 1:
      android_ndk_path = str(sys.argv[1] + "/Data/PlaybackEngines/AndroidPlayer/NDK")

  cmd_configure = """cmake ../FreeImage \
    -G"Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_TOOLCHAIN_FILE="{android_ndk_path}/build/cmake/android.toolchain.cmake" \
    -DCMAKE_MAKE_PROGRAM="{android_ndk_path}/prebuilt/linux-x86_64/bin/make" \
    -DANDROID_NDK="{android_ndk_path}" \
    -DANDROID_NATIVE_API_LEVEL=android-9 \
    -DANDROID_ABI={abi} \
    -DFREEIMAGE_LIB=OFF \
    -DSUPPORT_FMT_TIFF=ON \
    -DSUPPORT_FMT_JPEG=ON""".format(android_ndk_path=android_ndk_path, abi=abi)

  os.system(cmd_configure)
  os.system("cmake --build .")

build("build-arm64-v8a", "arm64-v8a")
os.chdir("..")
build("build-armeabi-v7a", "armeabi-v7a")
