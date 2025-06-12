import zipfile
import shutil
import os
from utils.exceptions import ZipExtractionError, handle_exception

@handle_exception
def extract_zip(zip_path: str, dest_folder: str):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dest_folder)
    except zipfile.BadZipFile:
        raise ZipExtractionError("Standard ZIP extraction failed.")

@handle_exception
def fallback_extract_zip(zip_path: str, dest_folder: str):
    try:
        shutil.unpack_archive(zip_path, dest_folder)
    except Exception:
        raise ZipExtractionError("Fallback ZIP extraction failed.")

@handle_exception
def extract_zip_with_fallback(zip_path: str, dest_folder: str):
    try:
        extract_zip(zip_path, dest_folder)
    except ZipExtractionError:
        fallback_extract_zip(zip_path, dest_folder)