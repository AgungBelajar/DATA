def split_file(input_file, lines_per_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        
    total_lines = len(lines)
    file_count = (total_lines + lines_per_file - 1) // lines_per_file  # Calculate the number of files needed

    for i in range(file_count):
        start_index = i * lines_per_file
        end_index = start_index + lines_per_file
        split_lines = lines[start_index:end_index]
        
        output_file = f"{'data'}{i+1}.txt"
        with open(output_file, 'w') as outfile:
            outfile.writelines(split_lines)
        
        print(f"Created {output_file} with lines {start_index+1} to {min(end_index, total_lines)}")

# File input dan jumlah baris per file
input_filename = 'data.txt'  # Ganti dengan nama file gabungan Anda
lines_per_file = 200

split_file(input_filename, lines_per_file)
print("Pembagian file selesai.")