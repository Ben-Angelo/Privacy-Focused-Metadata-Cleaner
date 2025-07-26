# Privacy-Focused Metadata Cleaner

**Privacy-Focused Metadata Cleaner** is a user-friendly desktop application developed in Python that helps you easily remove sensitive metadata from your digital photos (JPEG) and documents (PDF) in bulk.

Metadata such as EXIF data in images (camera model, date taken, GPS coordinates) or author information in PDFs can unintentionally expose personal details. This tool provides a simple graphical interface so you can sanitize your files before sharing them.

---

## Features

- **Intuitive GUI:** Easy-to-use graphical interface built with Tkinter.
- **Batch Processing:** Clean multiple JPEG and PDF files from a selected input folder at once.
- **Metadata Stripping:**
  - Removes EXIF data from JPEGs using [Pillow](https://python-pillow.org/).
  - Removes standard metadata from PDFs using [PyPDF2](https://pypdf2.readthedocs.io/).
- **Selective File Type Cleaning:** Choose to clean only JPEGs, only PDFs, or both.
- **Progress Tracking:** Progress bar and activity log to monitor the cleaning process.
- **Output Management:** Saves cleaned files to a specified output folder, preserving your original files.
- **Standalone Executable:** Can be packaged into an executable for easy distribution and use without needing Python installed (using [PyInstaller](https://pyinstaller.org/)).

---

## Technologies Used

- **Python 3.x** – Core programming language.
- **Tkinter** – Standard GUI toolkit for building the desktop interface.
- **Pillow** – For processing JPEG images and handling EXIF metadata.
- **PyPDF2** – For manipulating PDF files and removing metadata.
- **PyInstaller (optional)** – For packaging the Python application into a standalone executable (`.exe` for Windows, `.app` for macOS).

---

## Screenshots

<!-- Add screenshots here if available -->
<!-- ![App Screenshot](path/to/screenshot.png) -->
<img width="1366" height="768" alt="1" src="https://github.com/user-attachments/assets/4cf6495d-629a-4728-af82-9abbacbb7208" />



---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Ben-Angelo/Privacy-Focused-Metadata-Cleaner.git
```

### Install Dependencies

```bash
pip install Pillow PyPDF2
```

### Run the Application

```bash
python main.py
```

### (Optional) Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

---

## License

MIT License
