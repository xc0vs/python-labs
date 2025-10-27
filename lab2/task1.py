log_file_path = "./apache_logs.txt"

def analyze_log_file(log_file_path):
    status_codes = {" 200 " : 0, " 301 " : 0, " 302 " : 0, " 304 " : 0, " 404 " : 0, " 500 " : 0, " 502 " : 0, " 503 " : 0, " 504 " : 0}
    try:
        # Треба переробити повністю логіку

        with open(log_file_path, "rt") as f: 
            for line in f:
                for code in status_codes:
                    if code in line:
                        status_codes[code] += 1
        return status_codes
    except FileNotFoundError:
        return "File Not Found Error"
    except IOError:
        return "IO Error"
    except:
        "An undefined error has occurred"

    
print(analyze_log_file(log_file_path))
