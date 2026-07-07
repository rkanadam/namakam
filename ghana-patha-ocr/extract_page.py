#!/usr/bin/env python3
"""
Extract Sanskrit text from a single page image using Claude's vision API.
Usage: python3 extract_page.py <page_number> [<end_page_number>]
"""
import sys
import os
import base64
import json
import subprocess

PAGES_DIR = os.path.join(os.path.dirname(__file__), "pages")
TEXT_DIR = os.path.join(os.path.dirname(__file__), "text")

PROMPT = """You are an expert in Sanskrit and Vedic texts. Extract ALL the Sanskrit/Devanagari text from this scanned page image.

CRITICAL INSTRUCTIONS:
1. Reproduce the Devanagari text EXACTLY as printed, character by character
2. Preserve Vedic swara/accent marks:
   - Anudātta (underline below syllable): use the Unicode combining character U+0952 (॒)
   - Svarita (vertical line above syllable): use the Unicode combining character U+0951 (॑)
   - Udātta is unmarked (default tone)
3. Keep line breaks as they appear in the original
4. Keep numbering if present (e.g., row numbers in tables)
5. For any English headers or labels, include them as-is
6. If the page has a table structure, preserve it with clear formatting
7. Include the page number if visible
8. If the page is blank or has only images with no text, output: [BLANK PAGE]

Output ONLY the extracted text, nothing else. No commentary or explanations."""

def extract_page(page_num):
    img_path = os.path.join(PAGES_DIR, f"page_{page_num:03d}.png")
    out_path = os.path.join(TEXT_DIR, f"page_{page_num:03d}.txt")

    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
        return False

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"Page {page_num} already extracted, skipping")
        return True

    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_data
                    }
                },
                {
                    "type": "text",
                    "text": PROMPT
                }
            ]
        }]
    }

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return False

    import urllib.request
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            text = result["content"][0]["text"]
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Page {page_num}: extracted ({len(text)} chars)")
            return True
    except Exception as e:
        print(f"Page {page_num}: ERROR - {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_page.py <start_page> [<end_page>]")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start

    os.makedirs(TEXT_DIR, exist_ok=True)

    success = 0
    for p in range(start, end + 1):
        if extract_page(p):
            success += 1

    print(f"\nDone: {success}/{end - start + 1} pages extracted")
