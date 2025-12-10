from pathlib import Path
import time
import csv

from encoder.compressor import encode_file
from decoder.decompressor import decode_file


def roundtrip(input_path: Path, results: list) -> None:
    """
    Compress then decompress a file and assert exact byte equality.
    Also measures sizes and timings.
    """
    output_dir = Path("io/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    compressed = output_dir / (input_path.stem + ".huff")
    decompressed = output_dir / (input_path.stem + "_decoded" + input_path.suffix)

    # ----- Compression -----
    t0 = time.time()
    encode_file(input_path, compressed)
    t1 = time.time()

    # ----- Decompression -----
    t2 = time.time()
    decode_file(compressed, decompressed)
    t3 = time.time()

    # ----- Validation -----
    original = input_path.read_bytes()
    recovered = decompressed.read_bytes()

    ok = (original == recovered)

    if not ok:
        raise AssertionError(f"Roundtrip FAILED for {input_path}")

    orig_size = len(original)
    comp_size = compressed.stat().st_size
    ratio = comp_size / orig_size if orig_size > 0 else 0

    # Append results for CSV export
    results.append({
        "file": input_path.name,
        "original_size": orig_size,
        "compressed_size": comp_size,
        "ratio": ratio,
        "compression_ms": (t1 - t0) * 1000,
        "decompression_ms": (t3 - t2) * 1000,
    })

    print(f"[OK] {input_path.name} | ratio={ratio:.5f} | "
          f"comp={comp_size}B / orig={orig_size}B")


def scan_folder(folder: Path):
    return list(folder.glob("*.txt"))


def save_results_csv(results: list, output="compression_report.csv"):
    """Save test results to CSV for plotting."""
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[INFO] Results saved to {output}")


if __name__ == "__main__":
    input_dir = Path("io/input")
    txt_files = scan_folder(input_dir)

    if not txt_files:
        print("[WARN] No .txt files found in io/input")
        raise SystemExit(0)

    results = []

    print("========== ROUNDTRIP TESTS ==========\n")

    for file in txt_files:
        print(f"[TEST] {file.name}")
        roundtrip(file, results)

    save_results_csv(results)

    print("\n========== DONE ==========\n")
