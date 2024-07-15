FROM ubuntu:20.04

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Zerohertz's Dev Environment"
LABEL license="MIT"

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -g 1000 zerohertz && useradd -r -u 1000 -g zerohertz zerohertz && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get update && \
    apt-get install -y sudo locales curl wget unzip git software-properties-common tree tmux python3-opencv && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    echo "Asia/Seoul" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    echo "zerohertz ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir /home/zerohertz && chown -R zerohertz:zerohertz /home/zerohertz

# C++
RUN apt-get install -y build-essential gcc

# Go
RUN wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz && rm go1.22.4.linux-amd64.tar.gz

# Java
RUN apt-get install -y openjdk-17-jdk

# Neovim
COPY mason.sh /home/zerohertz/mason.sh
RUN wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux64.tar.gz && \
    tar -xzf nvim-linux64.tar.gz && \
    cp -r nvim-linux64/* /usr/local/ && \
    rm nvim-linux64.tar.gz && rm -rf nvim-linux64 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y ripgrep fish nodejs luarocks && \
    npm install -g neovim && \
    chmod +x /home/zerohertz/mason.sh

USER zerohertz

# ZSH
RUN curl -fsSL https://raw.githubusercontent.com/Zerohertz/etc/master/Util/sh/install_zsh.sh | bash && \
    sudo chsh -s $(which zsh) && $HOME/.oh-my-zsh/custom/themes/powerlevel10k/gitstatus/install -f && \
    mkdir -p $HOME/.config && git clone https://github.com/Zerohertz/dotfiles $HOME/dotfiles --recurse-submodules && cd $HOME/dotfiles  && \
    make

# Python
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py311_24.5.0-0-Linux-x86_64.sh -O $HOME/miniconda.sh && \
    chmod +x $HOME/miniconda.sh && \
    $HOME/miniconda.sh -b -p $HOME/miniconda && \
    rm $HOME/miniconda.sh && \
    $HOME/miniconda/bin/conda init zsh

# Neovim
RUN /home/zerohertz/miniconda/bin/pip install --no-cache-dir neovim && \
    zsh -c "source $HOME/.zshrc && \
    nvim --headless +qa && \
    /home/zerohertz/mason.sh && rm /home/zerohertz/mason.sh && \
    nvim --headless +TSUpdateSync '+sleep 20' +qa"

# zerohertzLib
RUN /home/zerohertz/miniconda/bin/pip install --no-cache-dir zerohertzLib[all]

WORKDIR /home/zerohertz/workspace
CMD ["zsh"]
