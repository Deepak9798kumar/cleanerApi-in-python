import os
import shutil
from flask import Flask, jsonify
from werkzeug.urls import quote

app = Flask(__name__)

# Specify the path to the temp directory on Windows
temp_directory = r'C:\Windows\Temp'

def directory_exists(dir_path):
    try:
        os.access(dir_path, os.F_OK)
        return True
    except FileNotFoundError:
        return False

# Define a route that triggers the file deletion
@app.route('/delete-files')
def delete_files():
    try:
        # Check if the temp directory exists, create if not
        if not directory_exists(temp_directory):
            print(f"Temp directory {temp_directory} does not exist.")
            return jsonify({"error": "Temp directory does not exist"}), 404

        # Read the contents of the temp directory
        files = os.listdir(temp_directory)

        # Delete each file or directory
        for file in files:
            file_path = os.path.join(temp_directory, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"File {file_path} deleted successfully")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Directory {file_path} deleted successfully")
            except PermissionError as perm_error:
                print(f"Permission error deleting {os.path.basename(file_path)}: {perm_error}")
            except Exception as delete_error:
                print(f"Error deleting {os.path.basename(file_path)}: {delete_error}")

        # Send a response once all deletions are attempted
        return 'Deletion attempted for all files and directories'

    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"error": f"Internal Server Error: {str(error)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
