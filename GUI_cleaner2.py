from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import PyPDF2 
from tkinter import ttk
from docx import Document  
from PIL.ExifTags import TAGS, GPSTAGS
import piexif 

class MetadataCleanerApp:
    def __init__(self, master):
        self.master = master
        master.title("Privacy-Focused Metadata Cleaner")
        master.geometry("650x550") 
        master.resizable(False, False)

        # --- Variables to store paths and cleaning options ---
        self.input_dir_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.clean_jpeg = tk.BooleanVar(value=True) # NEW: Checkbox for JPEG
        self.clean_pdf = tk.BooleanVar(value=False) # NEW: Checkbox for PDF
        self.clean_docx = tk.BooleanVar(value=False)
        self.remove_gps = tk.BooleanVar(value=True)
        self.remove_camera = tk.BooleanVar(value=True)

        # --- UI Elements ---

        # Input Directory Section
        tk.Label(master, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.input_dir_path, width=50, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_input_dir).grid(row=0, column=2, padx=5, pady=5)

        # Output Directory Section
        tk.Label(master, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.output_dir_path, width=50, state="readonly").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)

        # NEW: Cleaning Options Section
        tk.Label(master, text="Clean File Types:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Checkbutton(master, text="JPEG (.jpg, .jpeg)", variable=self.clean_jpeg).grid(row=2, column=1, sticky="w", padx=5)
        tk.Checkbutton(master, text="PDF (.pdf)", variable=self.clean_pdf).grid(row=3, column=1, sticky="w", padx=5)
        tk.Checkbutton(master, text="Word (.docx)", variable=self.clean_docx).grid(row=4, column=1, sticky="w", padx=5)

        tk.Label(master, text="JPEG Metadata to Remove:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        tk.Checkbutton(master, text="GPS Data", variable=self.remove_gps).grid(row=5, column=1, sticky="w", padx=5)
        tk.Checkbutton(master, text="Camera Model", variable=self.remove_camera).grid(row=6, column=1, sticky="w", padx=5)

        # Clean Button
        tk.Button(master, text="Clean Selected Files", command=self.start_cleaning,
                  bg="lightblue", fg="black", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

        # Status/Log Area
        tk.Label(master, text="Activity Log:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.log_text = scrolledtext.ScrolledText(master, width=75, height=15, wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=500, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=3, padx=10, pady=10)


    # --- Helper Functions for UI Interaction (same as before) ---

    def browse_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir_path.set(directory)
            self.log_message(f"Input folder selected: {directory}")

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_path.set(directory)
            self.log_message(f"Output folder selected: {directory}")

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    # --- Core Cleaning Logic ---

    def clean_single_image(self, input_file_path, output_directory):
        """
        Opens an image, strips its EXIF metadata, and saves it to the specified output directory.
        Returns True on success, False on failure.
        """
        try:
            os.makedirs(output_directory, exist_ok=True)
            file_name = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_directory, f"cleaned_{file_name}")

            with Image.open(input_file_path) as img:
                exif_data = img.info.get('exif')
                if exif_data:
                     
                    exif_dict = piexif.load(exif_data)
                    if self.remove_gps.get():
                        exif_dict.pop('GPS', None)
                    if self.remove_camera.get():
                        if '0th' in exif_dict:
                            for tag in list(exif_dict['0th']):
                                tag_name = TAGS.get(tag, tag)
                                if tag_name in ['Model', 'Make']:
                                    exif_dict['0th'].pop(tag)
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(output_file_path, exif=exif_bytes)
                else:
                    img.save(output_file_path)
                self.log_message(f"  - Saved JPEG: '{file_name}' to '{output_file_path}'")
                return True

        except FileNotFoundError:
            self.log_message(f"  - Error: JPEG file '{input_file_path}' not found. Skipping.")
            return False
        except Exception as e:
            self.log_message(f"  - An error occurred cleaning JPEG '{input_file_path}': {e}. Skipping.")
            return False

    # NEW FUNCTION: For cleaning PDF metadata
    def clean_single_pdf(self, input_file_path, output_directory):
        """
        Reads a PDF, removes its metadata, and saves it to a new file.
        Returns True on success, False on failure.
        """
        try:
            os.makedirs(output_directory, exist_ok=True)
            file_name = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_directory, f"cleaned_{file_name}")

            reader = PyPDF2.PdfReader(input_file_path)
            writer = PyPDF2.PdfWriter()

            # Copy all pages from the reader to the writer
            for page in reader.pages:
                writer.add_page(page)

            # Remove metadata by setting an empty dictionary.
            # PyPDF2 handles the standard PDF metadata fields here.
            writer.add_metadata({}) # This is the core metadata stripping step

            with open(output_file_path, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)

            self.log_message(f"  - Cleaned PDF: '{file_name}' to '{output_file_path}'")
            return True

        except FileNotFoundError:
            self.log_message(f"  - Error: PDF file '{input_file_path}' not found. Skipping.")
            return False
        except PyPDF2.errors.PdfReadError:
            self.log_message(f"  - Error: '{input_file_path}' is not a valid PDF file. Skipping.")
            return False
        except Exception as e:
            self.log_message(f"  - An error occurred cleaning PDF '{input_file_path}': {e}. Skipping.")
            return False

    def clean_single_docx(self, input_file_path, output_directory):
        try:
            os.makedirs(output_directory, exist_ok=True)
            file_name = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_directory, f"cleaned_{file_name}")

            doc = Document(input_file_path)
            # Remove core properties (author, etc.)
            core_props = doc.core_properties
            core_props.author = ""
            core_props.last_modified_by = ""
            core_props.comments = ""
            core_props.keywords = ""
            core_props.title = ""
            core_props.subject = ""
            core_props.category = ""
            core_props.content_status = ""
            core_props.identifier = ""
            core_props.language = ""
            core_props.version = ""
            doc.save(output_file_path)
            self.log_message(f"  - Cleaned DOCX: '{file_name}' to '{output_file_path}'")
            return True
        except Exception as e:
            self.log_message(f"  - Error cleaning DOCX '{input_file_path}': {e}")
            return False

    def start_cleaning(self):
        input_directory = self.input_dir_path.get()
        output_directory = self.output_dir_path.get()

        # Check if at least one file type is selected
        if not (self.clean_jpeg.get() or self.clean_pdf.get() or self.clean_docx.get()):
            messagebox.showerror("Error", "Please select at least one file type (JPEG, PDF, or DOCX) to clean.")
            return

        # Validate directories
        if not input_directory:
            messagebox.showerror("Error", "Please select an input folder.")
            return
        if not output_directory:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        if not os.path.isdir(input_directory):
            messagebox.showerror("Error", f"Input folder '{input_directory}' does not exist or is not a directory.")
            return

        self.log_message("\n--- Starting batch processing ---")
        self.log_message(f"Input: {input_directory}")
        self.log_message(f"Output: {output_directory}")

        processed_count = 0
        skipped_count = 0
        cleaned_jpegs = 0
        cleaned_pdfs = 0
        cleaned_docx = 0

        files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
        total_files = len(files)
        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        # Loop through all files in the input directory
        for idx, filename in enumerate(files, start=1):
            input_file_path = os.path.join(input_directory, filename)

            if os.path.isfile(input_file_path): # Ensure it's a file
                file_extension = filename.lower().split('.')[-1]

                if self.clean_jpeg.get() and file_extension in ['jpg', 'jpeg']:
                    if self.clean_single_image(input_file_path, output_directory):
                        processed_count += 1
                        cleaned_jpegs += 1
                    else:
                        skipped_count += 1
                elif self.clean_pdf.get() and file_extension == 'pdf':
                    if self.clean_single_pdf(input_file_path, output_directory):
                        processed_count += 1
                        cleaned_pdfs += 1
                    else:
                        skipped_count += 1
                elif self.clean_docx.get() and file_extension == 'docx':
                    if self.clean_single_docx(input_file_path, output_directory):
                        processed_count += 1
                        cleaned_docx += 1
                    else:
                        skipped_count += 1
                else:
                    self.log_message(f"  - Skipping '{filename}': Not a selected file type or not recognized.")
            else:
                self.log_message(f"  - Skipping '{filename}': Not a file (it's a directory).")

            self.progress["value"] = idx
            self.master.update_idletasks()
            self.log_message(f"Processing file {idx} of {total_files}: {filename}")

        self.progress["value"] = 0  # Reset after completion

        self.log_message("\n--- Batch Processing Complete ---")
        self.log_message(f"Total Processed: {processed_count} files")
        self.log_message(f"  - JPEGs Cleaned: {cleaned_jpegs}")
        self.log_message(f"  - PDFs Cleaned: {cleaned_pdfs}")
        self.log_message(f"  - DOCX Cleaned: {cleaned_docx}")
        self.log_message(f"Total Skipped: {skipped_count} files (due to errors or non-selected format)")
        messagebox.showinfo("Processing Complete",
                            f"Finished cleaning {processed_count} files.\n"
                            f"JPEGs: {cleaned_jpegs}, PDFs: {cleaned_pdfs}, DOCX: {cleaned_docx}\n"
                            f"Skipped: {skipped_count}.")


# --- Main Application Setup ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataCleanerApp(root)
    root.mainloop()