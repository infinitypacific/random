import sys
import os
from PIL import Image

def resizeImages(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
            print("[INFO]: Skipping "+filename+", not an image")
            continue
        img = Image.open(os.path.join(input_dir, filename))
        width, height = img.size
        side = min(width, height)
        hside = side // 2
        left = (width//2 - hside)
        top = (height//2 - hside)
        base_name = filename.split(".")[0]
        out_path = os.path.join(output_dir, base_name+".webp")
        img.crop((left, top, left + side, top + side)).resize((500, 500), Image.Resampling.LANCZOS).save(out_path, "WEBP")
        print("[INFO]: Resized "+filename+" to "+out_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python resize.py <input_directory> <output_directory>')
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        resizeImages(sys.argv[1], sys.argv[2])
    else:
        print('[ERROR]: Invalid directory: '+sys.argv[1], file=sys.stderr)
        sys.exit(1)