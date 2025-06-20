
# pyrefac.nvim 
Simple neovim plugin for Python refactoring, such as moving 
functions/classes/variables from one file to another. \
It uses [pyrefac](https://github.com/Makariy/pyrefac) which is *based* 
(and also based on rope). 

The greatest essential feature that it implements is moving multiple symbols 
from one module to another with adjusted imports.

### Usage example video:
[![Usage example](https://img.youtube.com/vi/HlCnVxZpR2Q/maxresdefault.jpg)](https://youtu.be/HlCnVxZpR2Q)


## Configuration
Default configuration is the next:
```{lua}
require("pyrefac").setup({
    -- Set custom command for pyrefac
    -- You can specify other arguments such as --project-root
    -- or exclude in this same command. (rope automatically excludes 
    -- .venv and a lot of other directories, so no need to specify those)
    pyrefac_command = 'pyrefac',  
    -- pyrefac_command = 'pyrefac --exclude datasets --project-root src',  
                                

    -- Formatting command. For example: "ruff format {}" 
    format_command = nil       
})

vim.keymap.set("x", "<leader>ms", ":PyrefacMove<CR>", { desc = "Move symbols" })
```

After the installation and configuration, you can select the symbols (functions,
classes or variables) to move, press `<leader>ms` and input the destination filename.
Done!


### Note: 
If you are moving some symbols to a directory, it must be a module (have \_\_init\_\_.py file)

