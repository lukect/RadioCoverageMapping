Remove-Item conda_env -Recurse -ErrorAction Ignore
Remove-Item venv -Recurse -ErrorAction Ignore
Remove-Item __pycache__ -Recurse -ErrorAction Ignore
conda env create --prefix .\conda_env --file environment.yml
& .\activate_env.ps1