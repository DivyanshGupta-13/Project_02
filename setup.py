import sys
import os

try:
    import cx_Freeze
    base = None
    if sys.platform == 'win32':
        base = "Win32GUI"

    executables = [
        cx_Freeze.Executable("frontpage.py", base=base, icon="face-id.ico" if os.path.exists("face-id.ico") else None)
    ]

    include_files = []
    for item in ['face-id.ico', 'HAAR_CASCADE.xml', 'Images for face recognition project', 'SAMPLE_DATA', 'ACTUAL_DATA', 'Attendence folder']:
        if os.path.exists(item):
            include_files.append(item)

    cx_Freeze.setup(
        name = "Facial Recognition Attendance System",
        options = {
            "build_exe": {
                "packages": ["tkinter", "os", "cv2", "numpy", "PIL", "sqlite3", "csv", "datetime"],
                "include_files": include_files
            }
        },
        version = "2.0",
        description = "Face Recognition Automatic Attendance System",
        executables = executables
    )
except ImportError:
    print("cx_Freeze is not installed. To build an executable, run: pip install cx_Freeze")
