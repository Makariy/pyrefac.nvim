import subprocess

from pynvim import Nvim

from utils import get_nvim_cwd


class PyrefacMover:
    def __init__(
        self,
        nvim: Nvim,
        pyrefac_command: str,
    ) -> None:
        self._nvim = nvim
        self._pyrefac_command = pyrefac_command

    def move_symbols(
        self,
        symbols: list[str],
        source: str,
        dest: str,
    ) -> list[str]:
        cwd = get_nvim_cwd(self._nvim)
        self._nvim.out_write(
            f"\nGoing to move symbols: {symbols} from {source} to {dest}"
        )

        modified_files: set[str] = set()

        for symbol in symbols:
            symbol_modified_files = self._run_move(symbol, source, dest, cwd)
            modified_files = modified_files.union(symbol_modified_files)

        self._nvim.out_write("\nMoving symbols succeed\n")
        return list(modified_files)

    def _run_move(self, symbol: str, source: str, dest: str, cwd: str) -> list[str]:
        command = [
            *self._pyrefac_command.split(),
            "--show-files",
            "move-symbol",
            source,
            symbol,
            dest,
        ]
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            cwd=cwd,
        )
        if result.stderr:
            raise RuntimeError(result.stderr + "\n")

        if not result.stdout:
            raise RuntimeError("No files modified")

        modified_files = result.stdout[:-1].split(",")
        return modified_files
