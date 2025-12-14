from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from encoder.compressor import encode_file


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 2:
        print("Usage: compresser <input.txt> <output.huff>", file=sys.stderr)
        return 1

    input_arg, output_arg = argv
    input_path = Path(input_arg)
    output_path = Path(output_arg)

    start = time.perf_counter()
    encode_file(input_path, output_path)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    input_size = os.path.getsize(input_path)
    output_size = os.path.getsize(output_path)
    ratio = (output_size / input_size) if input_size else 0.0

    with open("compression.txt", "a", encoding="utf-8", newline="\n") as f:
        f.write(
            f"{input_arg};{output_arg};{input_size};{output_size};{ratio:.5f};{elapsed_ms:.0f}\n"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
