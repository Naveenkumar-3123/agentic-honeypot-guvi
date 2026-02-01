import zipfile
import os

def create_submission_zip():
    files_to_include = [
        "main.py",
        "requirements.txt",
        "mock_scammer_simulation.py",
        "IMPLEMENTATION.md",
        ".env.example"  # Example only, not real keys
    ]
    dirs_to_include = [
        "app"
    ]
    output_filename = "Scam_Detection_Submission.zip"

    print(f"Creating {output_filename}...")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file in files_to_include:
            if os.path.exists(file):
                print(f"Adding {file}")
                zipf.write(file, file)
            else:
                print(f"Warning: {file} not found!")

        # Add directories recursively
        for directory in dirs_to_include:
            if os.path.exists(directory):
                print(f"Adding folder {directory}")
                for root, _, files in os.walk(directory):
                    for file in files:
                        if "__pycache__" in root or file.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.getcwd())
                        print(f"  Adding {arcname}")
                        zipf.write(file_path, arcname)
            else:
                print(f"Warning: {directory} folder not found!")

    print("\n✅ Submission Zip Created Successfully!")

if __name__ == "__main__":
    create_submission_zip()
