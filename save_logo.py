#!/usr/bin/env python3
"""Usage: python3 save_logo.py <tmp_file_path> <output_path>
Reads a Drive MCP download JSON (with 'content' base64 field) and saves to output_path."""
import sys, json, base64, os, re

def extract_b64(text):
    # Try JSON parse
    try:
        data = json.loads(text)
        if 'content' in data:
            return data['content']
    except:
        pass
    # Try regex for "content": "..." field
    m = re.search(r'"content"\s*:\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    # Maybe it's raw base64
    text = text.strip()
    if re.match(r'^[A-Za-z0-9+/=\n]+$', text):
        return text
    return None

if len(sys.argv) < 3:
    print("Usage: save_logo.py <tmp_file> <output_path>")
    sys.exit(1)

tmp_path = sys.argv[1]
out_path = sys.argv[2]

with open(tmp_path, 'r') as f:
    text = f.read()

b64 = extract_b64(text)
if not b64:
    print(f"ERROR: Could not extract base64 from {tmp_path}")
    sys.exit(1)

b64 = b64.replace('\n', '').replace(' ', '')
data = base64.b64decode(b64)

os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else '.', exist_ok=True)
with open(out_path, 'wb') as f:
    f.write(data)

print(f"Saved {len(data)} bytes to {out_path}")
