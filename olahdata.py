import os
import requests
import base64

# Fungsi untuk menemukan removable disk yang mengandung target_directory
def find_directory_on_removable_disk(target_directory):
    for drive_letter in range(ord('D'), ord('Z') + 1):
        drive = f"{chr(drive_letter)}:\\"
        potential_path = os.path.join(drive, target_directory)
        if os.path.exists(potential_path):
            return drive
    return None

# Fungsi untuk menggabungkan file dari direktori
def combine_files_from_directory(directory, output_file):
    combined_directory_path = os.path.join(directory, 'LOG')
    
    if not os.path.exists(combined_directory_path):
        print(f"Directory '{combined_directory_path}' does not exist.")
        return
    
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(combined_directory_path):
            file_path = os.path.join(combined_directory_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                with open(file_path, 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Tambahkan baris baru di antara file jika diperlukan
                print(f"Added '{filename}' to '{output_file}'.")
            else:
                print(f"'{filename}' is not a text file or does not exist.")

# Fungsi untuk membagi file menjadi beberapa file kecil
def split_file(input_directory, input_file, lines_per_file, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    
    input_path = os.path.join(input_directory, input_file)
    
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
        
    total_lines = len(lines)
    file_count = (total_lines + lines_per_file - 1) // lines_per_file

    for i in range(file_count):
        start_index = i * lines_per_file
        end_index = start_index + lines_per_file
        split_lines = lines[start_index:end_index]
        
        output_file = os.path.join(output_directory, f"data{i+1}.txt")
        
        with open(output_file, 'w') as outfile:
            outfile.writelines(split_lines)
        
        print(f"Created '{output_file}' with lines {start_index+1} to {min(end_index, total_lines)}.")
        
        # Upload file yang sudah di-split ke server
        upload_response = upload_file_to_server(output_file, upload_url)
        
        # Cetak kode respons dan teks respons dari server
        print(f"Upload response for '{output_file}':")
        print(f"Status Code: {upload_response.status_code}")
        print(f"Response Text: {upload_response.text}")

# Fungsi untuk mengirim file ke server dengan data base64
def upload_file_to_server(file_path, url):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        data = {'fileData': encoded_data}
        response = requests.post(url, data=data)
        return response

# Target directory in the root of the removable disk
target_directory = 'LOG'
directory_path = find_directory_on_removable_disk(target_directory)

if directory_path:
    print(f"Directory found: {directory_path}")
    
    # Gabungkan file-file dari direktori 'LOG' ke satu file output
    output_filename = os.path.join(directory_path, 'data.txt')
    combine_files_from_directory(directory_path, output_filename)
    print(f"Files successfully combined into '{output_filename}'.")

    # Membagi file gabungan menjadi beberapa file kecil dan upload
    lines_per_file = 200
    output_directory = directory_path  # Output disimpan di direktori input

    # URL untuk mengunggah file
    upload_url = "http://srs-ssms.com/aws_misol/upload-txt-wl.php"
    
    split_file(directory_path, 'data.txt', lines_per_file, output_directory)
    print("File splitting and upload completed.")
else:
    print("Target directory not found on any removable disk.")
