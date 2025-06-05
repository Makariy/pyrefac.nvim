from typing import Any, cast
import pynvim
import subprocess
import ast


def _get_module_symbols(tree: ast.Module) -> set[str]:
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

        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            symbols.add(node.name)

        elif isinstance(node, ast.ClassDef):
            symbols.add(node.name)

    return symbols


def get_nvim_cwd(nvim: pynvim.Nvim) -> str:
    return nvim.funcs.getcwd()


class RefacMoveExecutor:
    def __init__(
        self,
        nvim: pynvim.Nvim,
        pyrefac_path: str,
        format_command: str | None = None
    ) -> None:
        self._nvim = nvim
        self._pyrefac_path = pyrefac_path
        self._format_command = format_command

    def execute(self, selection: tuple[int, int]) -> None:
        data = self._get_selected_string(selection)

        symbols = list(_get_module_symbols(ast.parse(data)))
        self._print_selected_symbols(symbols)

        dest = self._prompt_dest_file()
        if dest is None:
            self._nvim.out_write("File does not exist\n")
            return

        self._move_symbols(symbols, dest)
        self._nvim.out_write("\nMoving symbols succeed\n")

        self._nvim.command('edit!')
        self._nvim.out_write(f"\nFile '{self._nvim.current.buffer.name}' reloaded.\n")

    def _format_files_if_needed(self, source: str, dest: str) -> None:
        if self._format_command is None:
            return 
        cwd = get_nvim_cwd(self._nvim) 
        self._run_format_file(source, cwd)
        self._run_format_file(dest, cwd)

    def _get_selected_string(self, selection: tuple[int, int]) -> str:
        start_line = selection[0]
        end_line = selection[1]

        current_buffer = self._nvim.current.buffer

        selected_lines = current_buffer[start_line - 1 : end_line]
        return "\n".join(selected_lines)

    def _print_selected_symbols(self, symbols: list[str]) -> None:
        self._nvim.out_write(
            f"Going to process:\n" 
            f"[{', '.join(symbols)}]\n"
        )

    def _prompt_dest_file(self) -> str | None:
        dest: str = self._nvim.call("input", "Enter dest filename: ", "", "file")
        if not dest or not dest.endswith(".py"):
            return None
        return dest 

    def _get_source_relative_path(self) -> str:
        cwd = get_nvim_cwd(self._nvim)
        return self._nvim.current.buffer.name.removeprefix(cwd + "/")

    def _move_symbols(self, symbols: list[str], dest: str):
        cwd = get_nvim_cwd(self._nvim)
        source = self._get_source_relative_path()        
        for symbol in symbols:
            self._run_move(symbol, source, dest, cwd)

    def _run_move(self, symbol: str, source: str, dest: str, cwd: str) -> None:
        command = [self._pyrefac_path, "move-symbol", source, symbol, dest]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,          
                check=True,         
                cwd=cwd
            )
            output = result.stderr or result.stdout
            if output:
                raise RuntimeError(output)

        except Exception as e:
            self._nvim.err_write(str(e)) 

    def _run_format_file(self, path: str, cwd: str) -> None:
        assert self._format_command is not None
        try:
            result = subprocess.run(
                self._format_command.format(path),
                text=True,
                check=True,
                capture_output=True,
                cwd=cwd
            )
            output = result.stdout or result.stderr
            if output:
                raise RuntimeError(output)
        except Exception as e:
            self._nvim.err_write(f"And error occurred formatting file: {e}")


@pynvim.plugin
class RefacPlugin:
    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim
        self._config: dict[str, str] = cast(
            dict[str, Any],
            self._nvim.vars.get("pyrefac_config") or {
                "pyrefac_path": "pyrefac"
            }
        )

    @pynvim.command('RefacMove', range=True, sync=True)
    def process_selected_code_command(
        self,
        selection: tuple[int, int],
    ):
        self._nvim.out_write(self._config.__str__() + "\n")
        RefacMoveExecutor(
            nvim=self._nvim,
            pyrefac_path=self._config["pyrefac_path"],
            format_command=self._config.get("format_command")
        ).execute(selection)

