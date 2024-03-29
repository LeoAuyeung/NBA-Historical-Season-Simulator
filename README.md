# NBA-Historical-Season-Simulator
## CSCI-35000 Final Project

### Team AI AI Captain
#### Name - Github Username
- Leo Au-Yeung - LeoAuyeung
- Kun Yu - kyu21
- Peter Lee - peterdjlee
- Leman Yan - Leman-y

### Relevant Links
[Slide Deck](https://docs.google.com/presentation/d/1aUGlcTwKs9ySmBIj4wKYZ71T8g1vzD4h7UbpnFzv7tI/edit?usp=sharing)

### Demo
![Demo](demo.gif)


### Technologies
scikit-learn, nba_api, pandas, numpy, matplotlib, seaborn, flask, react

### Install Instructions
This project uses [pipenv](https://github.com/pypa/pipenv) to handle dependencies. Install pipenv and install dependencies by using the following command which will create a local virtual environment to install packages.

````
pipenv install
````

To run in the virtual envionment with installed packages, use the following command to enter the virtual envionment:

````
pipenv shell
````

To manage python versions, you may want to look into [pyenv](https://github.com/pyenv/pyenv) to set a local python version.

Additionally, packages need to be installed for the react portion of the app
````
cd frontend
npm install
````

To run frontend

````
npm start
````

To run backend

````
pipenv shell
flask run --no-debugger
````
