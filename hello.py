import hashlib
import pefile
import ssdeep
import pandas as pd
import os
import concurrent.futures

def generate_hashes(file_path):
    # Tính toán giá trị băm MD5 của tệp
    with open(file_path, 'rb') as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()

    # Tính toán giá trị băm ImpHash của tệp
    pe = pefile.PE(file_path)
    imphash = pe.get_imphash()

    # Tính toán giá trị băm pehash của tệp
    pehash = hashlib.sha1(pe.dump_info().encode('utf-8')).hexdigest()

    # Tính toán giá trị ssdeep của tệp
    with open(file_path, 'rb') as f:
        ssdeep_hash = ssdeep.hash(f.read())

    # Tính toán giá trị ssdeep của phần Resource section trong tệp
    resources_section = pe.sections[-1]  # Lấy phần Resource section trong tệp
    resources_data = resources_section.get_data()  # Lấy dữ liệu của phần Resource section
    rs_ssdeep_hash = ssdeep.hash(resources_data)

    file_name = os.path.split(file_path)[1]

    # Trả về danh sách chứa tên, loại và các giá trị hash tương ứng với từng tệp
    return [file_name, md5_hash, imphash, pehash, ssdeep_hash, rs_ssdeep_hash]

def generate_hash_dataset(dir_path):
    # Khởi tạo dataframe trống
    df = pd.DataFrame(columns=["file name", "MD5", "ImpHash", "PEHash", "ssdeep", "rs_ssdeep"])
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
    # Lặp qua tất cả các tệp trong thư mục và tính toán các giá trị băm
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)

                # Kiểm tra xem đường dẫn tới file có tồn tại hay không
                if os.path.exists(file_path):
                    try:
                        hashes = generate_hashes(file_path)

                        # Thêm các giá trị hash vào dataframe
                        df.loc[len(df)] = hashes
                        print(f"{file_path} đã lưu.")
                    except:
                        print(f"Lỗi khi tính toán các giá trị băm cho file {file_path}.")
                else:
                    print(f"Đường dẫn tới file {file_path} không tồn tại.")

    # Lưu dataframe vào file CSV, loại bỏ các dòng trùng lặp
    csv_filename = os.path.join(dir_path, "dataset.csv")
    df.drop_duplicates().to_csv(csv_filename, index=False)

    print(f"Đã lưu dataset hash vào file CSV {csv_filename} thành công!")


# Thực hiện tính toán các giá trị băm cho các tệp trong thư mục "data"
dir_paths = ["D:\\python\\folder1", "D:\\python\\folder2", "D:\\python\\folder3"]

for dir_path in dir_paths:
    generate_hash_dataset(dir_path)