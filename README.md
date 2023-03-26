# swe7101
Attendance Management System

## Setting Up the Virtual Environment

### For Windows
   `py -3 -m venv venv`

### For MacoS/Linux
   `python3 -m venv venv`

## To Activate the Virtual Environment

### for Windows
   `source venv\Scripts\activate`
   
### for MacOS/Linus
   `. venv/bin/activate`

## To Start the Application 
   `flask --app ams run --debug`

## To Install All Application Dependencies
   `pip install -r requirements.txt`

## to Update the requirements.txt
   `pip freeze > requirements.txt`

# Git Command

## Step in Using Version Control
1. Create branch - `git checkout -b <branch_name>`
2. Staging - `git add .`
3. Commit - `git commit -m 'Commit message'`
3. push - `git push`

## Runing Flask Test
 `pytest -v`

## Running flask test with Coverage
`coverage run -m pytest`

## Viewing Flast test coverage report
`coverage report`

## generating the test report
`coverage html`