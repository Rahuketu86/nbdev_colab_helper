# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['IN_COLAB', 'setup_git', 'git_push', 'setup_project']

# Cell
IN_COLAB = 'google.colab' in str(get_ipython())

# Cell
import os, subprocess, urllib, shlex

def _run_commands(commands, password=None):
  for cmd in commands:
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output, err = process.communicate()
    if password: cmd = cmd.replace(password, '*****')
    print(cmd)
    if output or err:
      print('  ', output.decode('utf8').strip() if output else '', err or '')

def setup_git(git_url:str, git_branch:str, name:str, password:str, email:str):
  "Link your mounted drive to GitHub"
  password = urllib.parse.quote(password)
  _run_commands([
      f"git config --global user.email {email}",
      f"git config --global user.name {name}",
      f"git init",
      f"git remote rm origin",
      f"git remote add origin {git_url.replace('://git', f'://{name}:{password}@git')}",
      f"git pull origin {git_branch} --allow-unrelated-histories"],
      password)

def git_push(git_branch:str, message:str):
  "Convert the notebooks to scripts and then push to the library"
  _run_commands([
      f'nbdev_install_git_hooks',
      f'nbdev_build_lib',
      f'git add *',
      f'git commit -m "{message}"',
      f'git push origin {git_branch}'])

# Cell
from google.colab import drive
from configparser import ConfigParser
from pathlib import Path

def setup_project(project_name):
  global config, project_config, git_url, git_branch
  drive.mount('/content/drive')
  config_path = Path('/content/drive/My Drive/nbdev_colab_projects.ini')
  config = ConfigParser()
  config.read(config_path)
  if project_name not in config:
    print(f'Error: [{project_name}] section not found in {config_path}')
    print(f'Please add a section for [{project_name}] and run `setup_project` again')
    # TODO: add link to help page
    return
  project_config = config[project_name]
  project_path = Path(project_config['project_parent'])/project_name
  git_url, git_branch = project_config['git_url'], project_config['git_branch']
  if project_path.is_dir():
    print(f'Clone of {project_name} already exists in {project_path.parent}')
  else:
    project_path.parent.mkdir(parents=True, exist_ok=True)
    cd(project_path.parent)
    !git clone $git_url
  cd(project_path)
  !pip install git+https://github.com/fastai/nbdev.git
  setup_git(git_url, git_branch, project_config['git_user_name'],
            project_config['git_user_password'], project_config['git_user_email'])