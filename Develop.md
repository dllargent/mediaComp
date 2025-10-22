# Contributing

## Setting up your environment

- Install the necessary dependencies found on the README.md
- Clone the repository
- Open in VSCode
- From the root of the repository make a branch 
    - ```git checkout -b <new-branch-name>```
    - This is the branch you will make your changes in
- Make a virtual python enviornment in the repository
    - ```python -m venv dev```
- Load into the environment
    - ```dev/Scripts/activate```
    - You should see (dev) to the left of your terminal 
- Install the local library in the environment
    - ```pip install -e .```
- Any changes now made in the local version of the package will be on the branch and reflected in the environment

## Developing
- Before changing code, verify that you're writing on a branch other than ```main``` and that your command line is in the virtual enviornment 
- Develop and make some changes
- To test the package features create a file in the root of the repository called ```test.py```
- In ```test.py``` import mediaComp with ```from mediaComp import *```
- Test the features you were working on and continue developing, making commits when progess is made
- When finished working on a feature, push the branch to GitHub and open a pull request to merge your branch into ```main```
