import os
import shutil
import kagglehub

project_dir = (
    os.getcwd()
) 
raw_data_dir = os.path.join(project_dir, "data", "raw")
os.makedirs(raw_data_dir, exist_ok=True)

dataset_path = kagglehub.dataset_download("amirmotefaker/ab-testing-dataset")
print("Dataset downloaded to temporary location:", dataset_path)

filename = os.path.basename(dataset_path)
destination_path = os.path.join(raw_data_dir, filename)
shutil.move(dataset_path, destination_path)

print("Dataset has been moved to:", destination_path)
