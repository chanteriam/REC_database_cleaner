# Forefront Racial Equity Collective Database Cleaner
<img width="1149" alt="image" src="https://github.com/chanteriam/REC_database_cleaner/assets/68039600/63157cec-f6c5-4b2d-b3d7-6c5298e4a1ed">

This repository includes scripts for cleaning Forefront's Racial Equity Collective Map survey data.
The scripts allow data cleaning from both the Qualtrics and the Survey Monkey surveys. The cleaner
application is hosted on Render, and it can be launched through this website: https://rec-database-cleaner.onrender.com.

To make edits to the backend code, clone this reposity and add it to your own GitHub account. 

Note that to deploy any edits you make to the Flask application, you will need to create a free [Render](https://render.com/) account and follow the steps [here](https://render.com/docs/projects#:~:text=Creating%20a%20project,to%20name%20your%20first%20environment) to create a new project.

Initialize the poetry environment by running:
```
poetry shell
```

Ensure you are in the project working directory and run the below code to launch the development version of the Flask application:
```
python -m flask run [--debug]
```

Any frontend changes that you make it the code will be reflected in the Flask application if launch the Flask application in debug mode (by using the `--debug` flag).

There is also a command-line argument you can run to process your uncleaned REC Map data. To do so, open the project directory in your code editor and run the following command in the terminal:

```
python -m scripts [Full Path to File Directory] [File Name] [Data Source: qualtrics/survey monkey]
```

For example:

```
python -m scripts '/Users/shaymilner/Documents/NORC/GRA_CER/REC_database_cleaner/input' 'Racial Equity Collective of Illinois Mapping Survey.xlsx' 'survey monkey'
```
