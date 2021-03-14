# applied_rl
Repository for the Applied Reinforcement Internship 2020/2021 at LMU Munich

## Model-based reinforcement learning regarding uncertainty in a cartpole environment

### Instructions

#### Pipenv
1. Make sure Python 3.7 is installed (other Python versions e.g. 3.6 or 3.8 won't work due to compatibility issues with tensorflow)
2. `git clone https://github.com/JonasLewe/applied_rl.git` 
3. `cd applied_rl`
4. Install the pipenv package: `pip install pipenv`
5. Create a virtual environment: `pipenv install`
6. Run pipenv environment: `pipenv shell`
7. Create kernel to be able to import packages in a notebook:

   `python -m ipykernel install --user --name=applied_rl`
8. Start an instance of jupyter notebook and run `ARLProject.ipynb`
9. Select `applied_rl` kernel

#### Google Drive
If pipenv does not work, it is also possible to run the ARLProject.ipynb through Google Collab
1. Add gymSampling to the Google Drive, preferably in an ARL folder at bottom level (/content/drive/MyDrive/ARL)
2. Add `from google.colab import drive`
3. Add `drive.mount('/content/gdrive')`
4. Add `pip install gym_cartpole_swingup`
5. Add `pip install stable_baselines3`
6. Add `pip install -e /content/drive/MyDrive/ARL/gymSampling`
7. Change `googledrive_dir = "ARL/"` to `googledrive_dir = "/content/drive/MyDrive/ARL/"`

#### Jupyter Lab/Notebook
Alternatively it can also be run with any other jupyter notebook instance outside of the pipenv as long as all prerequisites are installed
1. Make sure Python 3.7 is installed
2. Run `pip install -e gymSampling` from the folder that contains gymSampling
3. install all other prerequisites

### Usage
Every code block has information regarding its purposes added in a markdown cell above it.

The code runs in sequential order, but sections may be skipped if needed. Some variables may be required later which would require a check above to see where it was first used and to execute that code block.

Code with a big, italic TRAIN retrains a model and may be time-consuming, it can be skipped in favor of loading blocks that simply load already trained checkpoints.

Code with a big, italic STORE writes a checkpoint or data to the file system and may overwrite existing files.

Code with a big, italic LOAD is used to reload stored checkpoints and data. This is advised even for newly created data as variable names may change due to that. Our checkpoints are provided in the ARL folder. There may be version issues with the PPO checkpoints between different installations. We were unable to pinpoint the package causing this. In case of this error, it will be neccessary to skip the resampling for the graphs until own PPO runs have been made that overwrite the stored checkpoints. The format of these would work with the code afterwards. Some samples could not be uploaded to GitHub due to size restrictions and thus have to be resampled.

### Gruppe 5
Philipp Jahn, Jonas Lewe, Isabelle Mayerhofer


