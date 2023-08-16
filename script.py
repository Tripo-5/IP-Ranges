import pandas as pd
import os
import ipaddress

# Load the Excel file into a DataFrame
df = pd.read_excel('your_file.xlsx', header=None)  # Assume no headers in the Excel file

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    start_ip = ipaddress.ip_address(row[0])  # Assuming the IP addresses are in the first column (column 0)
    end_ip = ipaddress.ip_address(row[1])    # Assuming the IP addresses are in the second column (column 1))

    # Create a folder based on the first prefix of the start IP
    folder_name = str(start_ip).split('.')[0]
    folder_path = os.path.join('output_folder', folder_name)

    # Create the main folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create a text file within the folder
    text_file_path = os.path.join(folder_path, f'{start_ip} - {end_ip}.txt')
    with open(text_file_path, 'w') as file:
        file.write(f'IP Range: {start_ip} - {end_ip}\n')

        # Write each IP address within the range on a new line
        current_ip = start_ip
        while current_ip <= end_ip:
            file.write(str(current_ip) + '\n')
            current_ip += 1
