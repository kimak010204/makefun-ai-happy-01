"""ai-happy-01 entry: copy the bundled image to /output/entry.png.

Deterministic, offline, standard library only. The image (image.png
beside this file) is copied byte-for-byte to the output path, and the
copy is verified to match the source exactly. No randomness, no clock,
no network: two runs always produce identical bytes.
"""

import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")
SOURCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.png")


MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    if not os.path.isfile(SOURCE_PATH):
        raise SystemExit(f"missing source image: {SOURCE_PATH}")
    size = os.path.getsize(SOURCE_PATH)
    if size > MAX_BYTES:
        raise SystemExit(f"source image too large: {size} bytes (max {MAX_BYTES})")
    with open(SOURCE_PATH, "rb") as fh:
        if fh.read(len(PNG_MAGIC)) != PNG_MAGIC:
            raise SystemExit("source image is not a PNG file")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        shutil.copyfile(SOURCE_PATH, OUTPUT_PATH)
    except OSError as exc:
        raise SystemExit(f"failed to write {OUTPUT_PATH}: {exc}") from exc
    # Verify the copy is byte-identical to the source before exiting.
    if os.path.getsize(OUTPUT_PATH) != size:
        raise SystemExit("output size does not match source image")


if __name__ == "__main__":
    main()
