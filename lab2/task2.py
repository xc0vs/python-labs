from hashlib import sha256 

file_paths = ["./task2_files/lorem", "./task2_files/steam.exe", "./task2_files/video.dll"]

def generate_file_hashes(*file_paths):
    dic_hashes = {}
    for path in file_paths:
        try:
            with open(path, "rb") as f:
                file_data = f.read()
                dic_hashes[path] = sha256(file_data).hexdigest()
        except FileNotFoundError:
            print(f"File Not Found Error: '{path}'")
        except IOError:
            print(f"IO Error: '{path}'")
        except:
            print(f"An undefined error has occurred: '{path}'")
    return dic_hashes


hashes = generate_file_hashes(*file_paths)
print(hashes)