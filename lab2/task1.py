log_file_path = "./apache_logs.txt"

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
        return "File Not Found Error"
    except IOError:
        return "IO Error"
    except:
        "An undefined error has occurred"

    
print(analyze_log_file(log_file_path))
