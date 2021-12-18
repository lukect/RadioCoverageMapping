Remove-Item venv -Recurse -ErrorAction Ignore
Remove-Item __pycache__ -Recurse -ErrorAction Ignore
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install libs\windows64\GDAL-3.3.3-cp310-cp310-win_amd64.whl
pip install libs\windows64\rasterio-1.2.10-cp310-cp310-win_amd64.whl
pip install libs\windows64\pyproj-3.2.1-cp310-cp310-win_amd64.whl
pip install -r requirements.txt