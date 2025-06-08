import ast
from pynvim import Nvim

from mover import PyrefacMover
from formatter import PyrefacFormatter
from file_updater import NvimFileUpdater
from cleaner import PyrefacCleaner

from utils import (
    get_buff_relative_path,
    get_module_symbols,
    get_selected_string_from_buffer,
)


class PyrefacMoveExecutor:
    def __init__(
        self, nvim: Nvim, pyrefac_path: str, format_command: str | None = None
    ) -> None:
        self._nvim = nvim
        self._mover = PyrefacMover(nvim, pyrefac_path)
        self._cleaner = PyrefacCleaner(
            nvim=self._nvim,
            formatter=PyrefacFormatter(format_command),
            file_updater=NvimFileUpdater(self._nvim),
        )

    def execute(self, selection: tuple[int, int]) -> None:
        data = get_selected_string_from_buffer(self._nvim.current.buffer, selection)
        symbols = list(get_module_symbols(ast.parse(data)))
        self._nvim.out_write(f"\nGoing to move: {symbols}\n")

        source = get_buff_relative_path(self._nvim)
        dest = self._prompt_dest_file()
        if dest is None or not dest.endswith(".py"):
            self._nvim.out_write("\nNo correct filename provided\n")
            return

        files = self._mover.move_symbols(symbols, source, dest)
        self._cleaner.clean(source, files)

    def _prompt_dest_file(self) -> str | None:
        dest: str = self._nvim.call("input", "Enter dest filename: ", "", "file")
        if not dest or not dest.endswith(".py"):
            return None
        return dest
