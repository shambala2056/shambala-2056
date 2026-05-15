#!/usr/bin/env python3
"""
Save base64 image data and convert to WebP.
Usage: python3 save_and_convert.py <source> <logos_name>
  source: either a tmp file path containing MCP JSON, or 'stdin' to read from stdin
  logos_name: target filename stem (e.g. 'callpro' → saves logos/callpro.png and logos/callpro.webp)
"""
import sys, json, base64, os, re
from PIL import Image
import io

LOGOS = "/Users/suvd/Desktop/shambala-2056/logos"

def extract_b64(text):
    try:
        data = json.loads(text)
        if 'content' in data:
            return data['content']
    except:
        pass
    m = re.search(r'"content"\s*:\s*"([A-Za-z0-9+/=\r\n]+)"', text, re.DOTALL)
    if m:
        return m.group(1)
    text = text.strip()
    if len(text) > 20 and re.match(r'^[A-Za-z0-9+/=\r\n]+$', text):
        return text
    return None

def save_logo(b64_str, stem):
    b64_str = b64_str.replace('\n','').replace('\r','').replace(' ','')
    raw = base64.b64decode(b64_str)

    # Save original format as PNG
    png_path = os.path.join(LOGOS, f"{stem}.png")
    webp_path = os.path.join(LOGOS, f"{stem}.webp")

    img = Image.open(io.BytesIO(raw))
    img = img.convert("RGBA")  # ensure alpha channel preserved

    img.save(png_path, "PNG")
    img.save(webp_path, "WEBP", quality=90, method=6)

    print(f"✓ {stem}: {img.size[0]}x{img.size[1]} → {png_path}, {webp_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: save_and_convert.py <tmp_file_or_stdin> <stem>")
        sys.exit(1)

    source = sys.argv[1]
    stem = sys.argv[2]

    if source == 'stdin':
        text = sys.stdin.read()
    else:
        with open(source, 'r') as f:
            text = f.read()

    b64 = extract_b64(text)
    if not b64:
        print(f"ERROR: Could not extract base64 from {source}", file=sys.stderr)
        sys.exit(1)

    save_logo(b64, stem)
