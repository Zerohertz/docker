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
    nvim --headless +":MasonInstall $package --force" +qa
done