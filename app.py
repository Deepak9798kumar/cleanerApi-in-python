from fastapi import FastAPI, HTTPException
import shutil
import os

app = FastAPI()

# Your code for cleaning temporary files
def clean_temp_files():
    temp_directories = [
        '/private/var/folders',
        '~/Library/Caches',
        '~/Library/Logs',
        '~/Downloads',
        '~/Desktop'
    ]

    extensions = [
        '.log',
        '.cache',
        '.tmp',
        '.dmg',
        '.pkg'
    ]

    for directory in temp_directories:
        for dirpath, dirnames, filenames in os.walk(os.path.expanduser(directory)):
            for filename in filenames:
                if os.path.splitext(filename)[1].lower() in extensions:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        if os.path.isfile(filepath):
                            os.remove(filepath)
                        elif os.path.isdir(filepath):
                            shutil.rmtree(filepath)
                        print(f"Removed {filepath}")
                    except Exception as e:
                        print(f"Error deleting {filepath}: {e}")

# Define an API endpoint for cleaning temporary files
@app.get("/clean_temp_files")
def read_root():
    try:
        clean_temp_files()
        return {"message": "Temporary files cleaned successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
