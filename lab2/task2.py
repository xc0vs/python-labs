from hashlib import sha256 

def generate_file_hashes(*file_paths):
    dic_hashes = {}
    for path in file_paths:
        try:
            with open(path, "+br") as f:
                file_data = f.read()
                dic_hashes[path] = sha256(file_data).hexdigest()
        except FileNotFoundError:
            return "File Not Found Error"
        except IOError:
            return "IO Error"
        except:
            return "An undefined error has occurred"
    return dic_hashes

file_paths = ["./task2_files/lorem", "./task2_files/steam.exe", "./task2_files/video.dll"]
print(generate_file_hashes(*file_paths))