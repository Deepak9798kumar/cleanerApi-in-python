from fastapi import FastAPI, HTTPException
import shutil
import os
import uvicorn

app = FastAPI()

# API endpoint for cleaning temporary files
@app.get("/")
def read_root():
    return {"message": "Hello, it works!"}
@app.get("/clean")
def clean_temp_files():
    temp_directory = 'C:\\Windows\\Temp'
    deleted_files = []

    print(f"Cleaning temporary files in directory: {temp_directory}")

    try:
        for dirpath, dirnames, filenames in os.walk(temp_directory):
            for filename in filenames + dirnames:
                filepath = os.path.join(dirpath, filename)
                try:
                    if os.path.exists(filepath):
                        if os.path.isfile(filepath):
                            os.unlink(filepath)  # Use os.unlink to delete files
                            deleted_files.append(filepath)
                            print(f"Removed file: {filepath}")
                        elif os.path.isdir(filepath):
                            shutil.rmtree(filepath)
                            deleted_files.append(filepath)
                            print(f"Removed directory: {filepath}")
                    else:
                        print(f"Item does not exist: {filepath}")
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    return {"message": "Temporary files cleaned successfully.", "deleted_files": deleted_files}

if __name__ == "__main__":
    # Get the port from the PORT environment variable, default to 10000 if not set
    port = int(os.environ.get("PORT",8007))
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
