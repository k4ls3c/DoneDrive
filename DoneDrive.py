import requests
import argparse
import time
from datetime import datetime
from tabulate import tabulate

CLIENT_ID = "d3590ed6-52b3-4102-aeff-aad2292ab01c"
AUTHORITY_URL = "https://login.microsoftonline.com/common/oauth2/v2.0"

# Function to read access token and refresh token from file
def read_tokens():
    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().splitlines()
            return tokens[0], tokens[1]  # access_token, refresh_token
    except FileNotFoundError:
        print("Tokens file not found. Please login first using --login.")
        return None, None

# Function to save access token and refresh token to file
def save_tokens(access_token, refresh_token):
    with open('tokens.txt', 'w') as file:
        file.write(access_token + "\n")
        file.write(refresh_token + "\n")

# Function to refresh access token using refresh token
def refresh_access_token(refresh_token):
    body = {
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(f"{AUTHORITY_URL}/token", data=body)
    if response.status_code == 200:
        token_response_json = response.json()
        new_access_token = token_response_json['access_token']
        new_refresh_token = token_response_json['refresh_token']
        save_tokens(new_access_token, new_refresh_token)
        print("[*] Access token refreshed successfully.")
        return new_access_token
    else:
        print("Failed to refresh access token.")
        print(response.json())
        return None

def find_folder_id(folder_name):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    list_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(list_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(list_url, headers=headers)

    if response.status_code == 200:
        children = response.json()
        for item in children['value']:
            if item['name'] == folder_name:
                folder_id = item['id']
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Folder Name: {folder_name}")
                print(f"Folder ID: {folder_id}")
                print(f"Time and Date: {current_time}")
                return folder_id
        print("Folder not found.")
    else:
        print(f"Failed to list children. Status code: {response.status_code}")
        print(response.json())

def list_all_folders():
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    list_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(list_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(list_url, headers=headers)

    if response.status_code == 200:
        children = response.json()
        table_data = []
        for item in children['value']:
            if 'folder' in item:  # Check if the item is a folder
                folder_name = item['name']
                folder_id = item['id']
                table_data.append([folder_name, folder_id])
        
        print(tabulate(table_data, headers=["Folder Name", "Folder ID"], tablefmt="grid"))
    else:
        print(f"Failed to list children. Status code: {response.status_code}")
        print(response.json())

def upload_file(file_path, destination_path):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    with open(file_path, 'rb') as file:
        file_content = file.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/zip"
    }

    upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{destination_path}:/content"
    response = requests.put(upload_url, headers=headers, data=file_content)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/zip"
        }
        response = requests.put(upload_url, headers=headers, data=file_content)

    if response.status_code == 201:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File uploaded successfully.")
        print(f"Filename: {destination_path}")
        print(f"Time and Date: {current_time}")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())

def upload_file_to_folder(folder_id, file_path, filename):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    with open(file_path, 'rb') as file:
        file_content = file.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/zip"
    }

    upload_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{filename}:/content"
    response = requests.put(upload_url, headers=headers, data=file_content)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/zip"
        }
        response = requests.put(upload_url, headers=headers, data=file_content)

    if response.status_code == 201:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File uploaded successfully.")
        print(f"Filename: {filename}")
        print(f"Time and Date: {current_time}")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())

def delete_file_by_name(folder_id, file_name):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    delete_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{file_name}"
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File '{file_name}' deleted successfully.")
        print(f"Folder ID: {folder_id}")
        print(f"Time and Date: {current_time}")
    else:
        print(f"Failed to delete file. Status code: {response.status_code}")
        print(response.json())

def download_file(folder_id, file_name, destination_path):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{file_name}:/content"
    response = requests.get(download_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            file.write(response.content)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File downloaded successfully.")
        print(f"Filename: {file_name}")
        print(f"Destination Path: {destination_path}")
        print(f"Time and Date: {current_time}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        print(response.json())

def download_file_by_id(file_id, destination_path):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
    response = requests.get(download_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            file.write(response.content)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File downloaded successfully.")
        print(f"File ID: {file_id}")
        print(f"Destination Path: {destination_path}")
        print(f"Time and Date: {current_time}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        print(response.json())

def search_files(keyword):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    search_url = f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{keyword}')"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        results = response.json()
        if results['value']:
            table_data = []
            for item in results['value']:
                file_id = item['id']
                file_path = get_item_path(file_id)
                table_data.append([file_path, file_id])
            
            print(tabulate(table_data, headers=["File Path", "File ID"], tablefmt="grid"))
        else:
            print(f"No files found with keyword '{keyword}'.")
    else:
        print(f"Failed to search files. Status code: {response.status_code}")
        print(response.json())

def get_item_path(item_id):
    access_token, refresh_token = read_tokens()
    if not access_token or not refresh_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("[*] Access token expired. Refreshing access token...")
        access_token = refresh_access_token(refresh_token)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        item = response.json()
        return item['parentReference']['path'] + '/' + item['name']
    else:
        print(f"Failed to get item path. Status code: {response.status_code}")
        print(response.json())
        return None
        
def initiate_device_code_login():
    print("[*] Initiating a device code login.")

    body = {
        "client_id": CLIENT_ID,
        "scope": "https://graph.microsoft.com/.default offline_access"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_response = requests.post(
        f"{AUTHORITY_URL}/devicecode",
        headers=headers,
        data=body
    )
    
    auth_response_json = auth_response.json()
    device_code = auth_response_json['device_code']
    user_code = auth_response_json['user_code']
    verification_url = auth_response_json['verification_uri']
    message = auth_response_json['message']

    #print(message)
    print(f"    Go to {verification_url} and enter the code: {user_code}")

    continue_auth = True
    access_token = None
    refresh_token = None

    while continue_auth:
        body = {
            "client_id": CLIENT_ID,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code
        }
        try:
            token_response = requests.post(
                f"{AUTHORITY_URL}/token",
                headers=headers,
                data=body
            )
            if token_response.status_code == 200:
                token_response_json = token_response.json()
                if 'access_token' in token_response_json and 'refresh_token' in token_response_json:
                    print("[*] Successful auth")
                    access_token = token_response_json['access_token']
                    refresh_token = token_response_json['refresh_token']
                    save_tokens(access_token, refresh_token)
                    print(f"Access Token: {access_token}\n")
                    print(f"Refresh Token: {refresh_token}\n")
                    print(f"Token Type: {token_response_json.get('token_type')}\n")
                    print(f"Scope: {token_response_json.get('scope')}\n")
                    print(f"Expires In: {token_response_json.get('expires_in')}\n")
                    print(f"Ext Expires In: {token_response_json.get('ext_expires_in')}\n")
                    print(f"Expires On: {token_response_json.get('expires_on')}\n")
                    print(f"Not Before: {token_response_json.get('not_before')}\n")
                    print(f"Resource: {token_response_json.get('resource')}\n")
                    print(f"Foci: {token_response_json.get('foci')}\n")
                    print(f"ID Token: {token_response_json.get('id_token')}\n")
                    break
            else:
                error_details = token_response.json()
                if error_details.get('error') == "authorization_pending":
                    time.sleep(3)
                else:
                    print("Failed to authenticate.")
                    print(error_details)
                    continue_auth = False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue_auth = False

    return access_token, refresh_token

def print_banner():
    print(r'''
888~-_                               888~-_          ,e,                     
888   \   e88~-_  888-~88e  e88~~8e  888   \  888-~\  "  Y88b    /  e88~~8e  
888    | d888   i 888  888 d888  88b 888    | 888    888  Y88b  /  d888  88b 
888    | 8888   | 888  888 8888__888 888    | 888    888   Y88b/   8888__888 
888   /  Y888   ' 888  888 Y888    , 888   /  888    888    Y8/    Y888    , 
888_-~    "88_-~  888  888  "88___/  888_-~   888    888     Y      "88___/  
                                                                             
By k4ls3c at Cyderes
''')

    print("")


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="OneDrive File Management Script")
    parser.add_argument('--find', type=str, help='Find folder ID by folder name')
    parser.add_argument('--list', action='store_true', help='List all folders and their IDs')
    parser.add_argument('--up', type=str, help='Path of the file to upload')
    parser.add_argument('--filename', type=str, help='Filename for the uploaded file')
    parser.add_argument('--folder', type=str, help='Folder ID for upload or delete operation', required=False)
    parser.add_argument('--delete', type=str, help='Filename of the file to delete', required=False)
    parser.add_argument('--download', type=str, help='Filename of the file to download from the specified folder', required=False)
    parser.add_argument('--dest', type=str, help='Destination path for the downloaded file', required=False)
    parser.add_argument('--fileid', type=str, help='File ID for downloading the file', required=False)
    parser.add_argument('--search', type=str, help='Keyword to search for in file names')
    parser.add_argument('--login', action='store_true', help='Initiate device code login')

    args = parser.parse_args()

    if args.login:
        initiate_device_code_login()
        
    elif args.find:
        find_folder_id(args.find)
    elif args.list:
        list_all_folders()
    elif args.up and args.filename:
        if args.folder:
            upload_file_to_folder(args.folder, args.up, args.filename)
        else:
            upload_file(args.up, args.filename)
    elif args.delete and args.folder:
        delete_file_by_name(args.folder, args.delete)
    elif args.download and args.folder and args.dest:
        download_file(args.folder, args.download, args.dest)
    elif args.fileid and args.dest:
        download_file_by_id(args.fileid, args.dest)
    elif args.search:
        search_files(args.search)
    else:
        print("Please provide valid arguments. Use --help for more information.")

if __name__ == "__main__":
    main()
