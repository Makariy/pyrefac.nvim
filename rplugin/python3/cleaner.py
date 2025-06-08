from pynvim import Nvim
from formatter import PyrefacFormatter
from utils import get_nvim_cwd
from file_updater import NvimFileUpdater


class PyrefacCleaner:
    def __init__(
        self, nvim: Nvim, formatter: PyrefacFormatter, file_updater: NvimFileUpdater
    ) -> None:
        self._nvim = nvim
        self._formatter = formatter
        self._file_updater = file_updater

    def clean(self, source_file: str, modified_files: list[str]) -> None:
        self._format_files_if_needed(modified_files)
        self._update_files(source_file, modified_files)

    def _format_files_if_needed(self, files: list[str]) -> None:
        if not self._formatter.is_format_enabled():
            return None

        cwd = get_nvim_cwd(self._nvim)
        self._formatter.run_format_files(files, cwd)
        self._nvim.out_write(f"Formatted {files}\n")

    def _update_files(self, source_file: str, modified_files: list[str]) -> None:
        self._nvim.out_write(f"\nOpening files: {modified_files}\n")
        self._file_updater.reopen_files(modified_files)
        self._nvim.out_write(f"\nOpening source path: {source_file}\n")
        self._file_updater.reopen_file(source_file)
