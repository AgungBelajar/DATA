import os

def combine_files_from_directory(directory, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                with open(file_path, 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Tambahkan baris baru di antara file jika diperlukan
            else:
                print(f"{filename} bukan file teks atau tidak ditemukan")

# Direktori yang berisi file-file teks
directory_path = 'D:\Agung\Python\Olah Data\LOG'  # Ganti dengan path ke direktori Anda
output_filename = 'data.txt'

combine_files_from_directory(directory_path, output_filename)
print(f"File berhasil digabungkan menjadi {output_filename}")
