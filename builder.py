import os
import struct
import subprocess
import sys
import zipfile
import io

def compile():
    path   = "payloads/elf/template.s"
    output = "tiny"
    
    subprocess.check_call(["gcc", "-nostdlib", "-no-pie", "-Wl,-n", path, "-o", output])
    subprocess.check_call(["strip", "-s", output])
    
    return output

def babel():
    elf_path = compile()
    with open(elf_path, "rb") as f:
        elfD = f.read()
    print(f"ELF size: {len(elfD)} bytes")

    if os.path.exists(elf_path):
        os.remove(elf_path)

    with open("payloads/c/template.c", "r") as f:
        cT = f.read()

    with open("payloads/pdf/template.pdf", "r") as f:
        pdfT = f.read()
    
    pdf_c_content = cT.replace('(', '\\(').replace(')', '\\)').replace('\n', ') Tj T* (')
    pdf_content = pdfT.format(length=len(pdf_c_content) + 50, content=pdf_c_content)
    pdf_data = pdf_content.encode('utf-8')

    with open("payloads/python/__main__.py", "r") as f:
        pT = f.read()

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("__main__.py", pT)
        zf.writestr("template.c", cT)
    zip_data = buffer.getvalue()

    with open("babel", "wb") as f:
        f.write(elfD)
        f.write(b"\n")
        f.write(pdf_data)
        f.write(zip_data)

    os.chmod("babel", 0o755)

if __name__ == "__main__":
    babel()
