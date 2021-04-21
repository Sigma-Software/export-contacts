brew install python3
brew update
brew install pyenv
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -k -v 3.7.5
pip install pipenv
pipenv install --dev