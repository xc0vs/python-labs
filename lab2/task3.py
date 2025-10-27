input_file_path = "./task3_files/apache_logs.txt"
output_file_path = "./task3_files/frequency_of_allowed_ips.txt"
allowed_ips = ("83.149.9.216", "91.177.205.119")


def filter_ips(input_file_path, output_file_path, allowed_ips): #Треба додати Оброблення можливих винятків
    with open(input_file_path, "rt") as fi:
        with open(output_file_path, "w") as fo:
            frequency = {}
            for line in fi:
                parts = line.split(' ', 1)
                for ip in allowed_ips:
                    if ip == parts[0]:
                        frequency[ip] = frequency.get(ip, 0) + 1
            for ip in allowed_ips:
                fo.write(f"{ip} - {frequency[ip]}\n")
            

filter_ips(input_file_path, output_file_path, allowed_ips)