# DoneDrive
![image](https://github.com/k4ls3c/DoneDrive/assets/148506834/60753c4e-07cb-42fc-a582-f9dd0bb194c5)

## Overview

DoneDrive uses the Graph API to manage files on OneDrive. It was developed during one of the red team engagements and is heavily inspired by GraphRunner :).

## Getting Started

**Clone the repository:**
```bash
git clone https://github.com/k4ls3c/DoneDrive.git
```
## Features
The built-in refresh access token function will check for expired tokens, update them automatically, and save them in the tokens.txt file.

## Usage
Initiate a device code login:
```
python3 ./DoneDrive.py --login
```
![image](https://github.com/k4ls3c/DoneDrive/assets/148506834/3f98de5a-2e1b-46c4-8ef9-c35a527e8bcf)


Options
```
python3 ./DoneDrive.py --login
python3 ./DoneDrive.py --find "Folder Name"
python3 ./DoneDrive.py --list
python3 ./DoneDrive.py --up "path/to/local/file.zip" --filename "file.zip"
python3 ./DoneDrive.py --up "path/to/local/file.zip" --filename "file.zip" --folder "FOLDER_ID"
python3 ./DoneDrive.py --delete "file_name.txt" --folder "FOLDER_ID"
python3 ./DoneDrive.py --download "file_name.zip" --folder "FOLDER_ID" --dest "path/to/save/file.zip"
python3 ./DoneDrive.py --fileid "FILE_ID" --dest "path/to/save/file.zip"
python3 ./DoneDrive.py --search "keyword"
```
Example
List all folders and their IDs
```
python3 ./DoneDrive.py --list
```
![image](https://github.com/k4ls3c/DoneDrive/assets/148506834/888558bb-17ad-4a75-95da-285f93f47ce1)

Upload file
```
python3 ./DoneDrive.py --up "path/to/local/file.zip" --filename "file.zip"
or
python3 ./DoneDrive.py --up "path/to/local/file.zip" --filename "file.zip" --folder "FOLDER_ID"
```
Download file
```
python3 ./DoneDrive.py --download "file_name.zip" --folder "FOLDER_ID" --dest "path/to/save/file.zip"
```
Download a File by File ID
```
python3 ./DoneDrive.py --fileid "FILE_ID" --dest "path/to/save/file.zip"
``` 
Delete file
```
python3 ./DoneDrive.py --delete "file_name.txt" --folder "FOLDER_ID"
```
Search 
```
python3 ./DoneDrive.py --search "keyword"
```

## Disclaimer

The author is not responsible for unauthorized use of this tool. Use responsibly and ensure compliance with legal and ethical standards.

## Reference
- https://github.com/dafthack/GraphRunner
