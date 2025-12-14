from pathlib import Path
import time
import csv
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# ------------------------------------------------------------------------

from encoder.compressor import encode_file
from decoder.decompressor import decode_file


def roundtrip(input_path: Path, results: list) -> None:
    """
    Compress then decompress a file and assert exact byte equality.
    Also measures sizes and timings.
    """
    # Création du dossier de sortie
    output_dir = Path("io/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    compressed = output_dir / (input_path.stem + ".huff")
    decompressed = output_dir / (input_path.stem + "_decoded" + input_path.suffix)

    print(f"[TEST] Processing {input_path.name}...")

    try:
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
            print(f"   [ECHEC] Contenu different pour {input_path.name}")
            return # On arrête là pour ce fichier

        orig_size = len(original)
        comp_size = compressed.stat().st_size
        
        # Calcul du ratio
        ratio = comp_size / orig_size if orig_size > 0 else 1.0
        gain_percent = (1 - ratio) * 100

        # Append results for CSV export
        results.append({
            "file": input_path.name,
            "original_size": orig_size,
            "compressed_size": comp_size,
            "ratio": ratio,
            "compression_ms": (t1 - t0) * 1000,
            "decompression_ms": (t3 - t2) * 1000,
        })

        print(f"   [OK] ratio={ratio:.5f} ({gain_percent:.2f}%) | "
              f"comp={comp_size}B / orig={orig_size}B")

    except Exception as e:
        print(f"   [ERREUR] Exception sur {input_path.name} : {e}")
    # -------------------------------------------------------------------


def scan_folder(folder: Path):
    return list(folder.glob("*.txt"))


def save_results_csv(results: list, output="compression_report.csv"):
    """Save test results to CSV for plotting."""
    if not results:
        return
    output_path = Path(output)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parent / output_path

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[INFO] Results saved to {output_path}")


if __name__ == "__main__":
    input_dir = Path("io/input")
    
    if not input_dir.exists():
        input_dir.mkdir(parents=True)
        print(f"[INFO] Dossier {input_dir} cree. Mettez vos fichiers .txt dedans.")
        sys.exit(0)

    txt_files = scan_folder(input_dir)

    if not txt_files:
        print("[WARN] No .txt files found in io/input")
        raise SystemExit(0)

    results = []

    print("========== ROUNDTRIP TESTS ==========\n")

    for file in txt_files:
        roundtrip(file, results)

    save_results_csv(results)

    print("\n========== RESUME GLOBAL ==========")
    if results:
        total_orig = sum(r["original_size"] for r in results)
        total_comp = sum(r["compressed_size"] for r in results)
        
        if total_orig > 0:
            global_gain = (1 - (total_comp / total_orig)) * 100
        else:
            global_gain = 0
            
        print(f"Fichiers testés avec succès : {len(results)}")
        print(f"Volume Total Original       : {total_orig} octets")
        print(f"Volume Total Compressé      : {total_comp} octets")
        print(f"GAIN GLOBAL PONDERE         : {global_gain:.2f}%")
    else:
        print("Aucun resultat valide.")
    print("===================================\n")