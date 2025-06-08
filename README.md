
# pyrefac.nvim 
Simple neovim plugin for Python refactoring. \
It uses [pyrefac](https://github.com/Makariy/pyrefac) which is *based* 
(and also based on rope). 

The greatest essential feature that it implements is moving multiple symbols 
from one module to another correcting its usages. 

### Usage example:
[![Usage example](https://img.youtube.com/vi/HlCnVxZpR2Q/maxresdefault.jpg)](https://youtu.be/HlCnVxZpR2Q)


## Configuration
Default configuration is the next:
```{lua}
require("pyrefac").setup({
    -- Set custom command for pyrefac
    pyrefac_path = 'pyrefac',  

    -- Formatting command. For example: "ruff format {}" 
    format_command = nil       
})

vim.keymap.set("x", "<leader>ms", ":PyrefacMove<CR>", { desc = "Move symbols" })
```

After the installation and configuration, you can select the symbols (functions,
classes or variables) to move, press "<leader>ms" and input the destination filename.
And done!


### Note: 
If you are moving some symbols to a directory, it must be a module (have \_\_init\_\_.py file)

