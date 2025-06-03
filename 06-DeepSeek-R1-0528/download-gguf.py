from huggingface_hub import hf_hub_download, list_repo_files # Import list_repo_files
import os

# Configuration
repo_id = "unsloth/DeepSeek-R1-0528-GGUF"
folder_in_repo = "Q4_K_M"
file_extension = ".gguf"
# Expand the tilde (~) to the user's home directory
local_base_dir = os.path.expanduser("~/dev-ai/models/unsloth/DeepSeek-R1-0528-GGUF")

# Create base directory
# The hf_hub_download function will create the directory if it doesn't exist
# when local_dir_use_symlinks=False. However, explicit creation is fine.
os.makedirs(local_base_dir, exist_ok=True)

# Download files
print(f"Listing files from {repo_id} in folder {folder_in_repo} with extension {file_extension}...")
try:
    all_repo_files = list_repo_files(repo_id, repo_type='model')
    files_to_download = [
        f for f in all_repo_files
        if f.startswith(folder_in_repo + "/") and f.endswith(file_extension)
    ]

    if not files_to_download:
        print(f"No files found in '{folder_in_repo}' with extension '{file_extension}'.")
    else:
        print(f"Found {len(files_to_download)} file(s) to download.")

    for filename_in_repo in files_to_download:
        print(f"Downloading {filename_in_repo}...")
        # The filename parameter in hf_hub_download should be the path within the repo
        # The local_dir parameter specifies where the file (maintaining its repo path structure)
        # will be saved under.
        # For example, if filename_in_repo is "UD-Q4_K_XL/file.gguf",
        # it will be saved as local_base_dir/UD-Q4_K_XL/file.gguf
        try:
            downloaded_file_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename_in_repo, # This is the path of the file within the repository
                local_dir=local_base_dir,
                local_dir_use_symlinks=False,
                # Set resume_download=True if you want to resume interrupted downloads
                # resume_download=True,
            )
            # The hf_hub_download function returns the full path to the downloaded file.
            # The way files are saved when local_dir is used can be tricky.
            # If filename_in_repo is "folder/file.txt", it will be saved as "local_dir/folder/file.txt".
            # If you want all files directly in local_base_dir without the repo's folder structure,
            # you would need to adjust the local_dir or rename/move the file post-download.
            # However, for GGUF files from a specific folder, saving them under that folder structure locally is usually fine.

            print(f"Successfully downloaded and saved to: {downloaded_file_path}")
            # If you want to confirm the exact path as per your original print statement's intent:
            # expected_local_path = os.path.join(local_base_dir, filename_in_repo)
            # print(f"Saved to: {expected_local_path}")


        except Exception as e:
            print(f"Error downloading {filename_in_repo}: {str(e)}")

except Exception as e:
    print(f"Error listing files from repository: {str(e)}")

print("Download process complete.")
