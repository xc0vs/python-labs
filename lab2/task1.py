log_file_path = "./task1_files/apache_logs.txt"

def analyze_log_file(log_file_path):
    status_codes = {}
    try:
        with open(log_file_path, "rt") as f: 
            for line in f:
                parts = line.split('"')
                code = parts[2].strip().split(' ')[0]
                if code.isdigit():
                    status_codes[code] = status_codes.get(code, 0) + 1
        return status_codes
    except FileNotFoundError:
        print("File Not Found Error")
    except IOError:
        print("IO Error")
    except:
        print("An undefined error has occurred")


codes = analyze_log_file(log_file_path)
print(codes)
