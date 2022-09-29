# Programming in Python (& R) for optics

## Activate

Run the following to activate your virtual environment

```
python3 -m venv env
source ./env/bin/activate
```

Run the following to install dependencies inside the environment


```
source ./env/bin/activate
python -m pip install -r requirements.txt
```

## Running jupyter notebooks

```bash
# Enable Python extension
# https://docs.rstudio.com/rsconnect-jupyter/#installing-jupyter-within-a-virtual-environment
jupyter-serverextension enable --sys-prefix --py rsconnect_jupyter
```
