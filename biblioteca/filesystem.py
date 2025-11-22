# stdlib/filesystem.py
from pathlib import Path
import shutil
from typing import List

# ROOT puede ajustarse a la raíz del proyecto si quieres:
ROOT = Path.cwd()

def _resolve(path: str, allow_outside_root: bool = False) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    if not allow_outside_root:
        root_res = ROOT.resolve()
        # permitir usar exactamente root también
        if p != root_res and root_res not in p.parents:
            raise PermissionError(f"Acceso fuera del directorio raíz no permitido: {p}")
    return p

def exists(path: str) -> bool:
    p = _resolve(path, allow_outside_root=True)
    return p.exists()

def read_file(path: str, encoding: str = "utf-8") -> str:
    p = _resolve(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {p}")
    return p.read_text(encoding=encoding)

def write_file(path: str, content: str, encoding: str = "utf-8") -> None:
    p = _resolve(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)

def append_file(path: str, content: str, encoding: str = "utf-8") -> None:
    p = _resolve(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding=encoding) as f:
        f.write(content)

def copy(src: str, dst: str) -> None:
    s = _resolve(src)
    d = _resolve(dst)
    if not s.exists():
        raise FileNotFoundError(f"Origen no encontrado: {s}")
    d.parent.mkdir(parents=True, exist_ok=True)
    # Si es directorio -> copia recursiva
    if s.is_dir():
        # si destino existe y es archivo -> error
        if d.exists() and d.is_file():
            raise IsADirectoryError(f"Destino existe como archivo: {d}")
        # usar copytree si destino no existe
        if not d.exists():
            shutil.copytree(s, d)
        else:
            # si destino existe y es dir -> copiar contenido dentro
            for item in s.iterdir():
                target = d / item.name
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
    else:
        shutil.copy2(s, d)

def move(src: str, dst: str) -> None:
    s = _resolve(src)
    d = _resolve(dst)
    if not s.exists():
        raise FileNotFoundError(f"Origen no encontrado: {s}")
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(s), str(d))

def delete(path: str) -> None:
    p = _resolve(path)
    if not p.exists():
        raise FileNotFoundError(f"Ruta no encontrada: {p}")
    if p.is_dir():
        # borrar recursivamente contenido
        shutil.rmtree(p)
    else:
        p.unlink()

def makedir(path: str, exist_ok: bool = True) -> None:
    p = _resolve(path)
    p.mkdir(parents=True, exist_ok=exist_ok)

def list_dir(path: str = ".") -> List[str]:
    p = _resolve(path)
    if not p.exists() or not p.is_dir():
        raise NotADirectoryError(f"No es un directorio válido: {p}")
    return [x.name for x in p.iterdir()]
