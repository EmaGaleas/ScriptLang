# biblioteca/system.py
import os
import shlex
import subprocess
from typing import Tuple, Optional, List

def run_os(command: str) -> int:
    """Ejecuta comando usando os.system. Devuelve código de retorno."""
    return os.system(command)

def run(command: str,
        capture_output: bool = True,
        shell: bool = False,
        timeout: Optional[float] = None,
        check: bool = False) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Ejecuta un comando y devuelve (returncode, stdout, stderr).
    - shell=False por seguridad por defecto.
    - Si shell=False, tokeniza con shlex.split().
    - Si ocurre excepción devuelve (-1, None, str(error)).
    """
    try:
        args = command if shell else shlex.split(command)

        proc = subprocess.run(
            args,
            shell=shell,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=check
        )
        return proc.returncode, (proc.stdout if capture_output else None), (proc.stderr if capture_output else None)
    except subprocess.CalledProcessError as e:
        # comando con check=True que terminó con non-zero exit
        return e.returncode, getattr(e, "output", None), getattr(e, "stderr", None)
    except Exception as e:
        # error inesperado (timeout, OSError, etc.)
        return -1, None, str(e)

def run_with_whitelist(command: str,
                       whitelist: Optional[List[str]] = None,
                       capture_output: bool = True,
                       shell: bool = False,
                       timeout: Optional[float] = None) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Ejecuta comando solo si el ejecutable está en whitelist.
    - whitelist: lista de nombres permitidos (ej: ['ls','python3']).
    - Si whitelist es None se comporta como run().
    - Extra: si command está vacío devuelve (127, None, "Comando vacío").
    """
    if not command or not command.strip():
        return 127, None, "Comando vacío"

    if whitelist is None:
        return run(command, capture_output=capture_output, shell=shell, timeout=timeout)

    try:
        parts = shlex.split(command) if not shell else command.split()
        exe = parts[0] if parts else ""
        if exe not in whitelist:
            return 127, None, f"Comando no permitido: {exe}"
        return run(command, capture_output=capture_output, shell=shell, timeout=timeout)
    except Exception as e:
        return -1, None, str(e)
