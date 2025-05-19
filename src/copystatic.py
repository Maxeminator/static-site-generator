import os
import shutil

def copy_static(src, dst, first_call=True):
    if os.path.exists(dst) and first_call:
        shutil.rmtree(dst)
        print(f"Created new folder {dst}")
        os.mkdir(dst)
    elif not os.path.exists(dst):
        print(f"Created new folder {dst}")
        os.mkdir(dst)
    for entry in os.listdir(src):
        src_path=os.path.join(src, entry)
        dst_path=os.path.join(dst, entry)
        if os.path.isfile(src_path):
            print(f"Copied {src_path} → {dst_path}")
            shutil.copy(src_path,dst_path)
        else:
            print(f"Created new folder {dst_path}")
            os.mkdir(dst_path)
            copy_static(src_path, dst_path,first_call=False)
