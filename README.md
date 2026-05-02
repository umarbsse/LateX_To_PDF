# LaTeX to PDF with Python

This project generates a PDF from LaTeX source stored in `input/latex.txt`. The
script reads that file, writes the LaTeX to a `.tex` file, compiles it with
`pdflatex`, and keeps the generated PDF plus build files in an `output/` folder.

## Files

- `latex_to_pdf.py`: Python script with a reusable `latex_to_pdf()` function.
- `input/latex.txt`: LaTeX source used by the default example run.
- `output/`: Created when the script runs. Contains `.tex`, `.pdf`, `.log`, and
  auxiliary LaTeX build files.

## Required Dependencies

- Python 3.10 or newer.
- `pdflatex`, provided by a LaTeX distribution.

No external paid APIs are used.

## Install LaTeX / pdflatex

Install one of these LaTeX distributions, then restart your terminal. The script
first checks `PATH`, then common Windows MiKTeX and TeX Live install folders.

### Windows

- Install MiKTeX: <https://miktex.org/download>
- Or install TeX Live: <https://tug.org/texlive/windows.html>

After installation, confirm it works:

```powershell
pdflatex --version
```

### macOS

- Install MacTeX: <https://tug.org/mactex/>

Confirm it works:

```bash
pdflatex --version
```

### Linux

Debian or Ubuntu:

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-extra
```

Fedora:

```bash
sudo dnf install texlive-scheme-basic texlive-collection-latexextra
```

Confirm it works:

```bash
pdflatex --version
```

## How to Run

From the project folder:

```powershell
python latex_to_pdf.py
```

The script reads this file by default:

```text
input/latex.txt
```

The included input file has a working example with the equation:

```latex
\[
    E = mc^2
\]
```

You can also choose the input file, output folder, and filename:

```powershell
python latex_to_pdf.py --input-file input/latex.txt --output-dir output --filename example
```

## Use from Another Python File

```python
from latex_to_pdf import latex_to_pdf, read_latex_file

latex_code = read_latex_file("input/latex.txt")
pdf_path = latex_to_pdf(latex_code, output_dir="output", filename="pythagoras")
print(pdf_path)
```

## Output Location

By default, generated files are saved in:

```text
output/
```

For the built-in example, the expected PDF is:

```text
output/example.pdf
```

The folder may also contain files such as `example.tex`, `example.log`,
`example.aux`, and other LaTeX build artifacts.

## Troubleshooting

### `pdflatex was not found on PATH`

Install MiKTeX, TeX Live, or MacTeX. If it is already installed, restart your
terminal and run:

```powershell
pdflatex --version
```

If that command still fails, the script will still try common Windows install
folders automatically. If it cannot find `pdflatex`, add the LaTeX
distribution's binary folder to your system `PATH`, such as:

```text
C:\Program Files\MiKTeX\miktex\bin\x64
C:\Users\John\AppData\Local\Programs\MiKTeX\miktex\bin\x64
C:\texlive\2026\bin\windows
```

### LaTeX compilation failed

Open the generated `.log` file in `output/` and look for the first LaTeX error.
Common causes include:

- Missing LaTeX packages.
- Invalid LaTeX syntax.
- Unescaped special characters such as `%`, `$`, `_`, `&`, or `#` in normal text.

### Missing packages on MiKTeX

MiKTeX can install missing packages automatically. If prompted, allow package
installation, then rerun:

```powershell
python latex_to_pdf.py
```

### No PDF appears

Check that:

- `pdflatex --version` works.
- The script was run from the project folder.
- `input/latex.txt` exists and contains the LaTeX source.
- The LaTeX document includes `\documentclass{...}` and `\begin{document}` /
  `\end{document}`.
