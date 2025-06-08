from pynvim import Nvim
from pynvim.api import Buffer
import ast


def get_module_symbols(tree: ast.Module) -> set[str]:
    symbols: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbols.add(target.id)
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            symbols.add(elt.id)

        elif isinstance(node, ast.FunctionDef) or isinstance(
            node, ast.AsyncFunctionDef
        ):
            symbols.add(node.name)

        elif isinstance(node, ast.ClassDef):
            symbols.add(node.name)

    return symbols


def get_nvim_cwd(nvim: Nvim) -> str:
    return nvim.funcs.getcwd()


def get_buff_relative_path(nvim: Nvim) -> str:
    cwd = get_nvim_cwd(nvim)
    return nvim.current.buffer.name.removeprefix(cwd + "/")


def get_selected_string_from_buffer(buffer: Buffer, selection: tuple[int, int]) -> str:
    start_line = selection[0]
    end_line = selection[1]

    selected_lines = buffer[start_line - 1 : end_line]
    # Wrap in \n for ast to not cause errors
    return "\n" + "\n".join(selected_lines) + "\n"
