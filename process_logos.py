#!/usr/bin/env python3
"""
Decodes all base64 logo files from tmp paths and saves them to logos/ directory.
Run after all Drive downloads complete.
Usage: python3 process_logos.py
"""
import json, base64, os, glob, re

LOGOS_DIR = "/Users/suvd/Desktop/shambala-2056/logos"

# Map: tmp filename substring → target logos/ filename
# Will be populated by the download session
PENDING = {}  # populated below

def decode_and_save(src_path, dst_path):
    with open(src_path, 'r') as f:
        text = f.read()
    # Try JSON
    try:
        data = json.loads(text)
        b64 = data.get('content', '')
    except:
        # Try regex
        m = re.search(r'"content"\s*:\s*"([A-Za-z0-9+/=\n]+)"', text, re.DOTALL)
        b64 = m.group(1) if m else text.strip()

    b64 = b64.replace('\n', '').replace(' ', '')
    raw = base64.b64decode(b64)

    with open(dst_path, 'wb') as f:
        f.write(raw)
    print(f"  ✓ {dst_path} ({len(raw)} bytes)")

if __name__ == '__main__':
    # Find all pending tmp files and process them
    tmp_files = glob.glob('/tmp/mcp-claude_ai_Google_Drive-download_file_content-*.txt')
    print(f"Found {len(tmp_files)} tmp files")

    for src in sorted(tmp_files):
        ts = os.path.basename(src).replace('mcp-claude_ai_Google_Drive-download_file_content-', '').replace('.txt', '')
        if ts in PENDING:
            dst = os.path.join(LOGOS_DIR, PENDING[ts])
            print(f"Processing {ts} → {dst}")
            try:
                decode_and_save(src, dst)
            except Exception as e:
                print(f"  ERROR: {e}")
        else:
            print(f"No mapping for tmp: {ts}")
