#!/bin/zsh

packages=(
    buf
    clangd
    cmakelang
    cmakelint
    codelldb
    docker-compose-language-service
    dockerfile-language-server
    eslint-lsp
    gofumpt
    goimports
    gomodifytags
    gopls
    gradle-language-server
    hadolint
    helm-ls
    impl
    java-test
    jdtls
    json-lsp
    lua-language-server
    markdownlint
    neocmakelsp
    prettier
    pyright
    ruff
    shfmt
    sqlfluff
    stylua
    svelte-language-server
    tailwindcss-language-server
    taplo
    terraform-ls
    tflint
    vtsls
    yaml-language-server
)

for package in "${packages[@]}"; do
    nvim --headless +"lua require('mason').setup()" +":MasonInstall $package --force" +qa
done
