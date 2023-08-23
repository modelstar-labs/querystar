import types
import sys
from querystar.commands.run.utils import open_source_file


def compile_source_code(target_path: str):
    with open_source_file(target_path) as f:
        source_code = f.read()

    # https://docs.python.org/3/library/functions.html#compile
    bytecode = compile(
        source_code,
        # Source code file path, shows up exceptions.
        target_path,
        # Need "exec" mode to compile entire script with multiple code blocks
        # ("eval": for single expression,
        # "single": for single interactive/ expression statement that evaluate to something).
        mode="exec",
        # flags or "future" srtatements are not inherited on compile.
        flags=0,
        dont_inherit=1,
        # Default optimization.
        optimize=-1,
    )

    return bytecode


def build_source_module(target_path: str):

    module = types.ModuleType("__main__")
    # sys.modules["__main__"] = module
    module.__dict__["__file__"] = target_path

    return module
