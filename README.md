# Smart Document Manager

## Environment Variables
* Setup environment variables in file '.flaskenv'
* Install Python library to enable local development
```
pip install python-dotenv
```

## Custon domain setup in Azure Web App
In Microsoft Entra, update application registration for a Callback URL
```
https://search.froim.zone/.auth/login/aad/callback
```

## Dependencies
### Option 1 (preferred)
If in active virtual environment, collect all present dependencies:
```
pip freeze > requirements.txt
```

### Option 2
Install package:
```
pip install pipreqs
```
Run:
```
python -m pipreqs.pipreqs .
```
or
```
python -m pipreqs.pipreqs --encoding=utf8 --force
```

## Virtual Environment
### Create
Command line:
```
python -m venv .venv
```
For Anaconda environment:
```
~\anaconda3\python -m venv .venv
```
Where '.venv' - folder name, where the new environment will be located

### Activate
Activate virtual environment
```
/.venv/Scripts/Activate.ps1
```


## Known issues
### Execution policy error on script execution
Error text like:
```
...see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170
```

Run PowerShell (or Code) as administration and execute:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
