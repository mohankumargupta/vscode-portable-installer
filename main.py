import requests
from pathlib import Path
from zipfile import ZipFile
import sys
import easygui

VSCODE_URL = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"
#OUTPUT_FOLDER = "vscode-php`"

def download_file(url: str, output_file: Path):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            easygui.msgbox("Problem dowloading vscode from Microsoft", "VScode Portable Installer")
        r.raise_for_status()
        #with open(output_file, 'wb') as f:
        with output_file.open('wb') as f:
            for chunk in r.iter_content(chunk_size=4096): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def mkdir(dirname):
    Path(dirname).mkdir(parents=True, exist_ok=False)

def unzip(filename: Path, dirname: Path):
    with ZipFile(filename) as f:
        f.extractall(dirname)

def makeDataDirectories(dirname):
    datadir = Path(dirname).joinpath("data")
    tmpdir = datadir.joinpath("tmp")
    mkdir(datadir)
    mkdir(tmpdir)

def downloadsDirectory():
    homedirectory = Path.home()
    downloads = homedirectory.joinpath("Downloads")
    return downloads

if __name__ == "__main__":
    tempzip = "vscode-portable.zip"    
    tempfolder = "vscode-portable"

    OUTPUT_FOLDER = easygui.enterbox("Enter directory name eg. vscode-boo", "VSCode Portable Installer")
    print(OUTPUT_FOLDER)
    if not OUTPUT_FOLDER:
        sys.exit(1)
       
    fullpath = downloadsDirectory().joinpath(OUTPUT_FOLDER)
    mkdir(fullpath)
    vscode_zip = fullpath.joinpath("vscode.zip")
    vscode_zip.touch()
    download_file(VSCODE_URL, vscode_zip)
    unzip(vscode_zip, fullpath)
    makeDataDirectories(fullpath)
    vscode_zip.unlink()
        
    