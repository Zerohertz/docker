FROM ubuntu:24.04

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Zerohertz's Dev Environment"
LABEL license="MIT"

ENV DEBIAN_FRONTEND=noninteractive

# groupadd -g 1000 zerohertz && useradd -r -u 1000 -g zerohertz zerohertz
RUN groupmod -n zerohertz ubuntu && usermod -l zerohertz ubuntu && usermod -d /home/zerohertz -m zerohertz && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get update && \
    apt-get install -y sudo locales curl wget unzip git gnupg software-properties-common eza tmux python3-opencv neofetch autojump bat git-delta && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    echo "Asia/Seoul" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    ln -s /usr/bin/batcat /usr/bin/bat && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    echo "zerohertz ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /workspace && chown -R zerohertz:zerohertz /home/zerohertz /workspace

# ----------------------- C++ ----------------------- #
RUN apt-get install -y build-essential gcc clang clangd cmake

# ----------------------- Go ----------------------- #
RUN apt-get install -y golang

# ----------------------- Java ----------------------- #
RUN apt-get install -y openjdk-17-jdk openjdk-21-jdk

# ----------------------- Node ----------------------- #
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    nvm install 24 && \
    npm install -g neovim tree-sitter-cli && \
    chown -R zerohertz:zerohertz $HOME/.nvm && \
    mv $HOME/.nvm /home/zerohertz/.nvm && \
    ln -sf /home/zerohertz/.nvm $HOME/.nvm

# ----------------------- Python ----------------------- #
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx
# curl -LsSf https://astral.sh/uv/install.sh | sh && \
#     source $HOME/.local/bin/env && \
ENV PATH="/opt/venv/main/bin:$PATH" \
    UV_PYTHON_INSTALL_DIR=/opt/venv
RUN uv python install 3.12 && \
    uv venv /opt/venv/main --python 3.12 --prompt "main" --seed --color always && \
    chown -R zerohertz:zerohertz /opt/venv

# ----------------------- Terraform ----------------------- #
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install -y packer terraform

# ----------------------- Neovim ----------------------- #
COPY mason.sh /home/zerohertz/mason.sh
RUN wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux-x86_64.tar.gz && \
    tar -xzf nvim-linux-x86_64.tar.gz && \
    cp -r nvim-linux-x86_64/* /usr/local/ && \
    rm nvim-linux-x86_64.tar.gz && rm -rf nvim-linux-x86_64 && \
    apt-get install -y ripgrep fd-find fzf fish luarocks && \
    chmod +x /home/zerohertz/mason.sh

# ----------------------- Lazygit ----------------------- #
RUN LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*') && \
    curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz" && \
    tar xf lazygit.tar.gz lazygit && \
    install lazygit /usr/local/bin && rm lazygit*

# ----------------------- Local Test ----------------------- #
# RUN sed -i 's|archive.ubuntu.com|kakao.mirror.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
#     sed -i 's|security.ubuntu.com|kakao.mirror.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
#     apt-get update

USER zerohertz

# ----------------------- ZSH ----------------------- #
RUN curl -fsSL https://raw.githubusercontent.com/Zerohertz/dotfiles/main/linux/zsh.sh | bash && \
    sudo chsh -s $(which zsh) $(whoami) && sudo chsh -s $(which zsh) root && \
    $HOME/.oh-my-zsh/custom/themes/powerlevel10k/gitstatus/install -f && \
    git clone https://github.com/Zerohertz/dotfiles $HOME/dotfiles && \
    cd $HOME/dotfiles && git submodule update --init -- .config/nvim && \
    mkdir $HOME/.config && make linux

# ----------------------- Rust ----------------------- #
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    zsh -c "source $HOME/.cargo/env && \
    rustup update && rustup component add rust-analyzer && exit"

# ----------------------- Java ----------------------- #
RUN curl -fsSL https://get.sdkman.io | bash && \
    zsh -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
    sdk install gradle && sdk install springboot && exit"

# ----------------------- Python ----------------------- #
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py312_24.7.1-0-Linux-x86_64.sh -O $HOME/miniconda.sh && \
#     chmod +x $HOME/miniconda.sh && \
#     $HOME/miniconda.sh -b -p $HOME/miniconda && \
#     rm $HOME/miniconda.sh && \
#     $HOME/miniconda/bin/conda init zsh

# ----------------------- Neovim ----------------------- #
RUN uv pip install --no-cache-dir neovim pylatexenc && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    zsh -c "source $HOME/.zshrc && \
    nvim --headless +qa && \
    /home/zerohertz/mason.sh && rm /home/zerohertz/mason.sh && \
    nvim --headless +TSUpdateSync '+sleep 20' +qa && exit"

# ----------------------- zerohertzLib ----------------------- #
RUN uv pip install --no-cache-dir zerohertzLib[all]==1.2.0

WORKDIR /workspace
ENTRYPOINT [ "zsh", "-c" ]
CMD [ "tail -f /dev/null" ]
