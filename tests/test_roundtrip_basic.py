from pathlib import Path

from encoder.compressor import encode_file
from decoder.decompressor import decode_file


def roundtrip(input_path: Path) -> None:
    """Compress then decompress a file and assert exact byte equality."""
    compressed = input_path.with_suffix(input_path.suffix + ".huff")
    decompressed = input_path.with_name(input_path.stem + "_decoded" + input_path.suffix)

    encode_file(input_path, compressed)
    decode_file(compressed, decompressed)

    original = input_path.read_bytes()
    recovered = decompressed.read_bytes()

    assert original == recovered, f"Roundtrip failed for {input_path}"


if __name__ == "__main__":
    base = Path(".")
    candidates = [
        Path("short.txt"),
        Path("Blaise_Pascal.txt"),
    ]

    for p in candidates:
        if p.exists():
            print(f"[TEST] Roundtrip on {p}...")
            roundtrip(p)
            print("  -> OK")
        else:
            print(f"[SKIP] {p} not found.")
