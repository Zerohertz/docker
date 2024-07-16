#!/bin/zsh

packages=(
    black
    clangd
    docker-compose-language-service
    dockerfile-language-server
    gofumpt
    goimports
    gomodifytags
    gopls
    hadolint
    impl
    isort
    java-test
    jdtls
    json-lsp
    lua-language-server
    markdownlint
    prettier
    pyright
    ruff-lsp
    shfmt
    stylua
    yaml-language-server
)

for package in "${packages[@]}"; do
    nvim --headless +"lua require('mason').setup()" +":MasonInstall $package --force" +qa
done
