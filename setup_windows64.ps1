rm -r venv
rm -r __pycache__
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install libs\windows64\GDAL-3.3.3-cp310-cp310-win_amd64.whl
pip install libs\windows64\rasterio-1.2.10-cp310-cp310-win_amd64.whl
pip install libs\windows64\pyproj-3.2.1-cp310-cp310-win_amd64.whl
pip install matplotlib