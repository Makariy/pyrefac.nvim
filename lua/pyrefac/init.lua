local M = {}

function M.setup(opts)
    opts = opts or {} 

    local default_opts = {
        pyrefac_command = 'pyrefac',
       	format_command = nil
    }

    local config = vim.tbl_deep_extend('force', {}, default_opts, opts)
    vim.g.pyrefac_config = config
end

return M 

