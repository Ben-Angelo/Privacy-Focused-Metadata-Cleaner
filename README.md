Privacy-Focused Metadata Cleaner
Project Overview
This is a user-friendly, privacy-focused desktop application developed with Python that allows you to easily remove sensitive metadata from your digital photos (JPEG) and documents (PDF) in a batch.

Metadata, like EXIF data in images (camera model, date taken, even GPS coordinates) or author information in PDFs, can unintentionally expose personal details. This tool provides a simple graphical interface to sanitize your files before sharing them.

Features
Intuitive GUI: Built with Tkinter for an easy-to-use graphical interface.
Batch Processing: Clean multiple JPEG and PDF files from a selected input folder at once.
Metadata Stripping: Effectively removes EXIF data from JPEGs using Pillow and standard metadata from PDFs using PyPDF2.
Selective File Type Cleaning: Choose to clean only JPEGs, only PDFs, or both.
Progress Tracking: Includes a progress bar and activity log to monitor the cleaning process.
Output Management: Saves cleaned files to a specified output folder, preserving your original files.
Standalone Executable: Can be packaged into an executable for easy distribution and use without needing Python installed (using PyInstaller).
Technologies Used
Python 3.x: The core programming language.
Tkinter: Python's standard GUI toolkit for building the desktop interface.
Pillow: For opening, processing, and saving JPEG images, specifically for EXIF metadata handling.
PyPDF2: For reading, manipulating, and writing PDF files, enabling metadata removal.
PyInstaller: (Optional) For packaging the Python application into a standalone executable (.exe for Windows, .app for macOS).
