import os
import shutil

src_dir = "D:\\pe-machine-learning-dataset\\whitelist"
dest_dir1 = "D:\\python\\folder2"
dest_dir2 = "D:\\python\\folder3"

# Tính toán số lượng tệp cần chia đều vào từng thư mục đích
file_count = len(os.listdir(src_dir))
file_count1 = file_count // 2
file_count2 = file_count - file_count1

# Chia đều các tệp vào hai thư mục đích
i = 0
for file in os.listdir(src_dir):
    file_path = os.path.join(src_dir, file)
    if os.path.isfile(file_path):
        if i < file_count1:
            shutil.copy(file_path, dest_dir1)
        else:
            shutil.copy(file_path, dest_dir2)
        i += 1