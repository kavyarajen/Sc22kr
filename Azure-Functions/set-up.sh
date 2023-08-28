# Python Installation

sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3-venv

# Node Installation
sudo apt install nodejs npm

#Installation of nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

#nvm use <version>

# Azure Function setup (TEST ENV)
npm install -g azure-functions-core-tools@3 --unsafe-perm true
func init Data-Movement --worker-runtime python