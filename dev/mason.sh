#!/bin/zsh

packages=(
    black
    clangd
    cmakelang
    cmakelint
    codelldb
    docker-compose-language-service
    dockerfile-language-server
    gofumpt
    goimports
    gomodifytags
    gopls
    hadolint
    helm-ls
    impl
    isort
    java-test
    jdtls
    json-lsp
    lua-language-server
    markdownlint
    neocmakelsp
    prettier
    pyright
    ruff-lsp
    shfmt
    sqlfluff
    stylua
    taplo
    terraform-ls
    tflint
    vtsls
    yaml-language-server
)

for package in "${packages[@]}"; do
    nvim --headless +"lua require('mason').setup()" +":MasonInstall $package --force" +qa
done
