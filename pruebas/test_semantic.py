import pytest
from pathlib import Path

from core.lexer import Lexer
from core.parser import parse_tokens
from core.semantic import check, SemanticError


def parse_and_check(src: str):
    tokens = Lexer(src).tokenize()
    ast = parse_tokens(tokens)
    check(ast)


def test_variable_used_before_set_raises():
    src = 'log "Hola ${X}"\n'
    with pytest.raises(SemanticError):
        parse_and_check(src)


def test_interpolation_with_definition_ok():
    src = 'set nombre = "Nicky"\nlog "Hola ${nombre}"\n'
    # no debería lanzar
    parse_and_check(src)


def test_copy_nonexistent_literal_raises():
    # elegir un nombre de archivo que es muy improbable que exista
    fname = 'archivo_no_existe.tmp'
    src = f'copy "{fname}" to "dest.tmp"\n'
    with pytest.raises(SemanticError):
        parse_and_check(src)


def test_copy_with_variable_literal_propagation(tmp_path: Path):
    src_file = tmp_path / 'src_tmp.txt'
    src_file.write_text('hola')

    # asignar variable a una ruta literal y luego usarla en copy
    src = f'set s = "{src_file}"\ncopy s to "dest.tmp"\n'
    # no debería lanzar porque el analizador semántico propaga la literal
    parse_and_check(src)
    

def parse_and_check(src: str):
    tokens = Lexer(src).tokenize()
    ast = parse_tokens(tokens)
    check(ast)


def test_run_empty_literal_raises():
    src = 'run ""\n'
    with pytest.raises(SemanticError):
        parse_and_check(src)


def test_delete_variable_nonexistent_raises():
    # variable asignada a una literal inexistente debe causar error semántico en delete
    fname = 'no_existe_archivo.tmp'
    src = f'set x = "{fname}"\ndelete x\n'
    with pytest.raises(SemanticError):
        parse_and_check(src)


def test_copy_destination_parent_missing_raises(tmp_path: Path):
    # crear un archivo de origen real
    src_file = tmp_path / 'creando_archivo_temp.txt'
    src_file.write_text('hiiii')

    # destino con carpeta padre inexistente
    dest = 'no_existe/sub/dest.txt'
    src = f'copy "{src_file}" to "{dest}"\n'
    with pytest.raises(SemanticError):
        parse_and_check(src)


def test_move_with_variable_propagation_ok(tmp_path: Path):
    # asegurar que move pasa cuando la variable src está asignada a una ruta que existe
    src_file = tmp_path / 'mv_src.txt'
    src_file.write_text('x')
    src = f'set a = "{src_file}"\nmove a to "dest.txt"\n'
    # no debería lanzar
    parse_and_check(src)

