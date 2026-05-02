"""Generate a PDF from LaTeX text using pdflatex.

This script reads LaTeX source from input/latex.txt, writes it to a .tex file,
runs pdflatex, and leaves all generated files in the selected output directory.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


class LatexBuildError(RuntimeError):
    """Raised when pdflatex is unavailable or compilation fails."""


DEFAULT_INPUT_FILE = Path("input") / "latex.txt"


def _tail(text: str, lines: int = 40) -> str:
    """Return the last few lines of command output for readable error messages."""
    return "\n".join(text.splitlines()[-lines:])


def find_pdflatex() -> str | None:
    """Find pdflatex on PATH or in common Windows LaTeX install folders."""
    pdflatex_path = shutil.which("pdflatex")
    if pdflatex_path is not None:
        return pdflatex_path

    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        / "MiKTeX"
        / "miktex"
        / "bin"
        / "x64"
        / "pdflatex.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
        / "MiKTeX"
        / "miktex"
        / "bin"
        / "pdflatex.exe",
        Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        / "Programs"
        / "MiKTeX"
        / "miktex"
        / "bin"
        / "x64"
        / "pdflatex.exe",
    ]

    texlive_root = Path(r"C:\texlive")
    if texlive_root.exists():
        # TeX Live includes the install year in the path, such as C:\texlive\2026.
        candidates.extend(
            texlive_dir / "bin" / "windows" / "pdflatex.exe"
            for texlive_dir in texlive_root.iterdir()
            if texlive_dir.is_dir()
        )

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return None


def read_latex_file(input_file: str | Path = DEFAULT_INPUT_FILE) -> str:
    """Read LaTeX source from a text file."""
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"LaTeX input file was not found: {input_path}. "
            "Create the file and add a complete LaTeX document."
        )

    if not input_path.is_file():
        raise ValueError(f"LaTeX input path is not a file: {input_path}")

    return input_path.read_text(encoding="utf-8")


def latex_to_pdf(
    latex_code: str,
    output_dir: str | Path = "output",
    filename: str = "example",
) -> Path:
    """Compile a LaTeX string into a PDF and return the generated PDF path.

    Args:
        latex_code: Complete LaTeX document source as a string.
        output_dir: Folder where the .tex, .pdf, .log, and auxiliary files go.
        filename: Base filename to use without an extension.

    Raises:
        ValueError: If latex_code is empty or filename is invalid.
        LatexBuildError: If pdflatex is missing or the LaTeX document fails.
    """
    if not latex_code.strip():
        raise ValueError("latex_code must contain a complete LaTeX document.")

    if Path(filename).name != filename or not filename.strip():
        raise ValueError("filename must be a simple file name without folders.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    tex_path = output_path / f"{filename}.tex"
    pdf_path = output_path / f"{filename}.pdf"

    # Write the source before checking pdflatex so users can inspect or compile
    # the .tex file manually if the LaTeX toolchain is not installed yet.
    tex_path.write_text(latex_code, encoding="utf-8")

    pdflatex_path = find_pdflatex()
    if pdflatex_path is None:
        raise LatexBuildError(
            "pdflatex was not found on PATH. Install a LaTeX distribution such "
            "as MiKTeX, TeX Live, or MacTeX, then restart your terminal. The "
            "script also checked common Windows MiKTeX and TeX Live folders. "
            f"The LaTeX source was saved to: {tex_path}"
        )

    command = [
        pdflatex_path,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        tex_path.name,
    ]

    try:
        result = subprocess.run(
            command,
            cwd=output_path,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise LatexBuildError(f"Failed to run pdflatex: {exc}") from exc

    if result.returncode != 0:
        log_path = output_path / f"{filename}.log"
        details = _tail(result.stdout or result.stderr)
        raise LatexBuildError(
            "LaTeX compilation failed.\n"
            f"Log file: {log_path}\n"
            f"pdflatex output:\n{details}"
        )

    if not pdf_path.exists():
        raise LatexBuildError(
            f"pdflatex finished, but the expected PDF was not created: {pdf_path}"
        )

    return pdf_path


def main() -> int:
    """Read LaTeX from a file and compile it to PDF."""
    parser = argparse.ArgumentParser(
        description="Generate a PDF from a LaTeX text file using pdflatex."
    )
    parser.add_argument(
        "--input-file",
        default=DEFAULT_INPUT_FILE,
        help="Text file containing a complete LaTeX document.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Folder for generated .tex, .pdf, .log, and auxiliary files.",
    )
    parser.add_argument(
        "--filename",
        default="example",
        help="Base output filename without extension.",
    )
    args = parser.parse_args()

    try:
        latex_code = read_latex_file(args.input_file)
        pdf_path = latex_to_pdf(
            latex_code,
            output_dir=args.output_dir,
            filename=args.filename,
        )
    except (OSError, ValueError, LatexBuildError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"PDF generated successfully: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
