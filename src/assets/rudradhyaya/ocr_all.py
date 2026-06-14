#!/usr/bin/env python3
"""OCR all page-*.jpg files using Claude via CLI stream-json.
Skips already-done pages, detects rate limits, waits for reset, then resumes."""

import base64
import glob
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta

import pytz  # pip3 install pytz

IMG_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT = (
    "Perform OCR on this image. Extract all text exactly as it appears, "
    "preserving line breaks and layout. Output only the extracted text, nothing else."
)


def ocr_image(img_path: str) -> str:
    with open(img_path, "rb") as f:
        img_b64 = base64.standard_b64encode(f.read()).decode()

    msg = {
        "type": "user",
        "message": {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_b64,
                    },
                },
                {"type": "text", "text": PROMPT},
            ],
        },
    }

    result = subprocess.run(
        [
            "claude",
            "-p",
            "--dangerously-skip-permissions",
            "--input-format",
            "stream-json",
            "--output-format",
            "stream-json",
            "--verbose",
        ],
        input=json.dumps(msg).encode(),
        capture_output=True,
        timeout=120,
    )

    text_parts = []
    for line in result.stdout.decode(errors="replace").split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if obj.get("type") == "assistant":
                for block in obj.get("message", {}).get("content", []):
                    if block.get("type") == "text":
                        text_parts.append(block["text"])
        except Exception:
            pass

    return "\n".join(text_parts)


def parse_reset_time(text: str):
    """Parse reset time from e.g. 'resets 10:20pm (America/Los_Angeles)'"""
    m = re.search(r"resets\s+(\d+:\d+(?:am|pm))\s+\(([^)]+)\)", text, re.IGNORECASE)
    if not m:
        return None
    time_str, tz_name = m.group(1), m.group(2)
    try:
        tz = pytz.timezone(tz_name)
    except Exception:
        tz = pytz.timezone("America/Los_Angeles")
    now_local = datetime.now(tz)
    reset_naive = datetime.strptime(time_str.upper(), "%I:%M%p")
    reset_local = now_local.replace(
        hour=reset_naive.hour,
        minute=reset_naive.minute,
        second=0,
        microsecond=0,
    )
    # If reset time is in the past, it's the next day
    if reset_local <= now_local:
        reset_local += timedelta(days=1)
    return reset_local.astimezone(pytz.utc)


def wait_for_reset(text: str, page_name: str) -> None:
    reset_utc = parse_reset_time(text)
    now_utc = datetime.now(pytz.utc)
    if reset_utc:
        wait_secs = max(0, (reset_utc - now_utc).total_seconds()) + 30  # 30s buffer
        reset_local_str = reset_utc.astimezone(
            pytz.timezone("America/Los_Angeles")
        ).strftime("%I:%M%p %Z")
        print(
            f"\nRATE LIMITED at {page_name}. "
            f"Resets at {reset_local_str}. "
            f"Waiting {wait_secs/60:.1f} min..."
        )
    else:
        wait_secs = 3600  # default 1 hour if we can't parse
        print(f"\nRATE LIMITED at {page_name}. Could not parse reset time. Waiting 60 min...")

    # Print countdown every 5 minutes
    waited = 0
    while waited < wait_secs:
        chunk = min(300, wait_secs - waited)
        time.sleep(chunk)
        waited += chunk
        remaining = wait_secs - waited
        if remaining > 0:
            print(f"  ... {remaining/60:.0f} min remaining until retry", flush=True)

    print("Rate limit window passed. Resuming...", flush=True)


def main():
    images = sorted(glob.glob(os.path.join(IMG_DIR, "page-[0-9][0-9][0-9].jpg")))
    total = len(images)
    print(f"Found {total} images to process.")

    for i, img_path in enumerate(images, 1):
        base = os.path.splitext(img_path)[0]
        txt_path = base + ".txt"

        if os.path.exists(txt_path):
            print(f"[{i:3}/{total}] SKIP {os.path.basename(img_path)} (already done)")
            continue

        print(f"[{i:3}/{total}] OCR  {os.path.basename(img_path)} ... ", end="", flush=True)
        while True:
            try:
                text = ocr_image(img_path)
                if "hit your limit" in text or "rate limit" in text.lower():
                    wait_for_reset(text, os.path.basename(img_path))
                    continue  # retry same page after waiting
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                lines = text.count("\n")
                print(f"done ({lines} lines)", flush=True)
                break
            except Exception as e:
                print(f"ERROR: {e} — retrying in 60s", file=sys.stderr, flush=True)
                time.sleep(60)

    print(f"\nAll {total} pages done.")


if __name__ == "__main__":
    main()
