import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"E:\2026\project2\ocr\tesseract.exe"
print(pytesseract.get_tesseract_version())