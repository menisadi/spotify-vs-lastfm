import os
from PIL import Image
import pytesseract


def extract_text_from_images(folder_path: str) -> dict[str, str]:
    results = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    text: str = pytesseract.image_to_string(img)
                    results[filename] = text
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return results


folder_path = "./spotify-screenshots/"
text_results = extract_text_from_images(folder_path)

output_file = os.path.join(folder_path, "extracted_texts.txt")
with open(output_file, "w", encoding="utf-8") as f:
    for image, text in text_results.items():
        f.write(f"--- {image} ---\n")
        f.write(text + "\n\n")

print(f"Text extraction completed. Results saved to {output_file}")
