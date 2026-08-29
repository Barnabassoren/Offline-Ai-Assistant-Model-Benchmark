import os 

folder_path = "data/docs"
files = os.listdir(folder_path)

for filename in files:
    full_path = os.path.join(folder_path, filename)
    print("Processing:", full_path)