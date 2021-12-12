FROM gitpod/workspace-full
                
RUN python3 -m pip install --upgrade pip
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN source $HOME/.poetry/env