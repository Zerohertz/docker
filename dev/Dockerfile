FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -g 1000 zerohertz && useradd -r -u 1000 -g zerohertz zerohertz
WORKDIR /home/zerohertz

RUN apt-get update && \
    apt-get install -y sudo locales curl wget unzip git software-properties-common tree && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    echo "Asia/Seoul" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    echo "zerohertz ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chown -R zerohertz:zerohertz /home/zerohertz
USER zerohertz

# ZSH
RUN curl -sL https://raw.githubusercontent.com/Zerohertz/etc/master/Util/ZSH/install.sh | bash && \
    curl https://raw.githubusercontent.com/Zerohertz/etc/master/Util/ZSH/.zshrc > $HOME/.zshrc && sed -i '/kube/d' $HOME/.zshrc && \
    sudo chsh -s $(which zsh) && ~/.oh-my-zsh/custom/themes/powerlevel10k/gitstatus/install -f

# Python
RUN sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt-get update && \
    sudo apt-get install -y python3.11 python3.11-venv && \
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11 && \
    sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.11 1 && \
    pip install zerohertzLib[all]

# C++
RUN sudo sudo apt-get install -y build-essential gcc

# Go
RUN wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz && rm go1.22.4.linux-amd64.tar.gz

# Neovim
RUN curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - && \
    sudo apt-get install -y python3-apt python3-launchpadlib nodejs && \
    sudo add-apt-repository -y ppa:neovim-ppa/unstable && sudo apt-get update && \
    sudo apt-get install -y neovim && \
    git clone https://github.com/Zerohertz/nvim ~/.config/nvim && \
    nvim --headless +qa && nvim --headless +'TSUpdateSync' +'sleep 20' +qa && \
    echo 'export SHELL=/bin/zsh' >> ~/.zshrc

WORKDIR /home/zerohertz/workspace

CMD ["zsh"]
