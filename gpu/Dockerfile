FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Zerohertz's Dev Environment"
LABEL license="MIT"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get update && \
    apt-get install -y locales curl wget unzip git gnupg software-properties-common eza tmux neofetch autojump && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    echo "Asia/Seoul" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# ----------------------- C++ ----------------------- #
RUN apt-get install -y build-essential gcc cmake

# ----------------------- Go ----------------------- #
RUN apt-get install -y golang

# ----------------------- Java ----------------------- #
# RUN apt-get install -y openjdk-17-jdk openjdk-21-jdk

# ----------------------- Terraform ----------------------- #
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install -y packer terraform

# ----------------------- Local Test ----------------------- #
# RUN sed -i 's|archive.ubuntu.com|kakao.mirror.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
#     sed -i 's|security.ubuntu.com|kakao.mirror.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
#     apt-get update

# ----------------------- Neovim ----------------------- #
COPY mason.sh /root/mason.sh
RUN wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux-x86_64.tar.gz && \
    tar -xzf nvim-linux-x86_64.tar.gz && \
    cp -r nvim-linux-x86_64/* /usr/local/ && \
    rm nvim-linux-x86_64.tar.gz && rm -rf nvim-linux-x86_64 && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y ripgrep fd-find fzf fish luarocks nodejs && \
    npm install -g neovim tree-sitter-cli && \
    chmod +x /root/mason.sh

# ----------------------- Lazygit ----------------------- #
RUN LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*') && \
    curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz" && \
    tar xf lazygit.tar.gz lazygit && \
    install lazygit /usr/local/bin && rm lazygit*

# ----------------------- ZSH ----------------------- #
RUN apt-get install zsh -y && \
    curl -fsSL https://raw.githubusercontent.com/Zerohertz/dotfiles/main/linux/zsh.sh | bash && \
    chsh -s $(which zsh) root && \
    $HOME/.oh-my-zsh/custom/themes/powerlevel10k/gitstatus/install -f && \
    git clone https://github.com/Zerohertz/dotfiles $HOME/dotfiles && \
    cd $HOME/dotfiles && git submodule update --init -- .config/nvim && \
    mkdir $HOME/.config && make linux

# ----------------------- Rust ----------------------- #
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    zsh -c "source $HOME/.cargo/env && \
    rustup update && rustup component add rust-analyzer && exit"

# ----------------------- Java ----------------------- #
# RUN curl -fsSL https://get.sdkman.io | bash && \
#     zsh -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
#     sdk install gradle && sdk install springboot && exit"

# ----------------------- Python ----------------------- #
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py312_24.7.1-0-Linux-x86_64.sh -O $HOME/miniconda.sh && \
    chmod +x $HOME/miniconda.sh && \
    $HOME/miniconda.sh -b -p $HOME/miniconda && \
    rm $HOME/miniconda.sh && \
    $HOME/miniconda/bin/conda init zsh

# ----------------------- Neovim ----------------------- #
RUN $HOME/miniconda/bin/pip install --no-cache-dir neovim isort black pylatexenc && \
    zsh -c "source $HOME/.zshrc && \
    nvim --headless +qa && \
    $HOME/mason.sh && rm $HOME/mason.sh && \
    nvim --headless +TSUpdateSync '+sleep 20' +qa && exit"

# ----------------------- Dev ----------------------- #
RUN apt-get install libmpich-dev libopenmpi-dev btop -y
COPY requirements.txt /root/requirements.txt
RUN $HOME/miniconda/bin/pip install -r /root/requirements.txt --no-cache-dir && \
    rm /root/requirements.txt
# NOTE: https://github.com/mpi4py/mpi4py/issues/335#issuecomment-1486366039
RUN rm /root/miniconda/compiler_compat/ld && \
    $HOME/miniconda/bin/pip install mpi4py && \
    $HOME/miniconda/bin/pip install flash-attn --no-build-isolation && \
    DS_BUILD_CPU_ADAM=1 $HOME/miniconda/bin/pip install deepspeed==0.16.4

WORKDIR /root/workspace
ENTRYPOINT [ "zsh", "-c" ]
CMD [ "tail -f /dev/null" ]
