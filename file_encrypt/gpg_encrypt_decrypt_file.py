import os
from pathlib import Path
import gnupg
import sys
from pwinput import pwinput

def create_config_file():
    #create basic config file
    print('Creating config file...')
    with open('config.txt', 'w') as file:
        file.write('#GNUPG config file\n')
        file.write('#This is a text file used for configuration of the file-gpg-image tool.\n')

def get_gnupg_path():
    '''
    if config file exists, get the gpg directory
    we know a file can't exist without the gpg dir since it is inserted upon creation
    else get the path adn then create the config file, after that add the directory to it
    Finally return gpg directory
    '''
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if 'GPG_DIR=' in line:
                    gpg_dir = line[8:].split('\n')[0]
                    return gnupg.GPG(gnupghome=gpg_dir)
    else:
        if os.name == 'nt':  # Windows
            gpg_dir = Path(os.getenv('APPDATA')) / 'gnupg'
        else:  # Linux, macOS, and other Unix-like systems
            gpg_dir = Path.home() / '.gnupg'
        print(f'''Default GPG directory found as: {gpg_dir}
        If this is not correct, change the directory in config.txt''')
        create_config_file()
        with open("config.txt", "a") as file:
            file.write(f"GPG_DIR={gpg_dir}")
        return gnupg.GPG(gnupghome=gpg_dir)

def generate_keys(gpg):
    '''
    Generate GPG keys, based on user choice
    :param gpg:
    :return: key
    '''
    print('For default press enter.')
    key_type = input('Key type: (default: RSA)')
    key_length = input('Key length: (default: 2048)')
    key_length = 2048 if key_length == '' else int(key_length)
    key_name = input('Your name: (default: Autogenerated Key)')
    key_comment = input('Your comment: (default: Generated by gnupg.py)')
    key_email = input('Your email: (default: <username>@<hostname>)')
    input_data = gpg.gen_key_input(
            key_type=key_type,
            key_length=key_length,
            name_real=key_name,
            name_comment=key_comment,
            name_email=key_email
    )
    generated_key = gpg.gen_key(input_data)
    return generated_key


def keys_list(gpg, private):
    '''
    Gets and lists all key data from all GPG private keys available
    :param gpg:
    :return:
    '''
    key_list  = gpg.list_keys(private)
    all_key_data = []
    for key_data in enumerate(key_list):
        all_key_data.append([key_data[1]['type'], key_data[1]['uids'], key_data[1]['fingerprint']])
    if private is True:
        print('''
All private keys currently available:
KEY ID               | USERID                           | Fingerprint
''')
    else:
        print('''
All public keys currently available:
KEY ID              | USERID                            | Fingerprint
''')
    for key in all_key_data:
        print(key)
    return all_key_data

def delete_menu(gpg):
    key_delete_choice = input('''
1. Delete private GPG key
2. Delete public GPG key
3. Delete public-private keypair
99. Back to Key Handling Menu
''')
    if key_delete_choice == '1':
        all_key_data = keys_list(gpg, True)
        fingerprint = input('Input the key fingerprint (last value):')
        password = pwinput('Input the password of the key:')
        print(str(gpg.delete_keys(fingerprint, True, passphrase=password)))
    elif key_delete_choice == '2':
        all_key_data = keys_list(gpg, False)
        fingerprint = input('Input the key fingerprint (last value):')
        print(str(gpg.delete_keys(fingerprint)))
    elif key_delete_choice == '3':
        all_key_data = keys_list(gpg, True)
        fingerprint = input('Input the key fingerprint (last value):')
        password = pwinput('Input the password of the key:')
        print(str(gpg.delete_keys(fingerprint, True, passphrase=password)))
        print(str(gpg.delete_keys(fingerprint)))
        keys_list(gpg, True)
    elif key_delete_choice == '99':
        key_menu(gpg)
    else:
        print('Incorrect Input. Try Again.')

def import_menu(gpg):
    import_choice = input('1. Import from ASCII\n2. Import from file\n')
    if import_choice == '1':
        print("Enter your input (Ctrl+D to finish or Ctrl+Z+Enter on Windows):")
        to_import = sys.stdin.read()
    elif import_choice == '2':
        key_file = input('Enter the filepath: ')
        with open(key_file, 'r') as file:
            to_import = file.read()
    else:
        print('Incorrect Input. Try Again')
        import_menu(gpg)
    key_import = gpg.import_keys(to_import).counts
    all_key_data = keys_list(gpg, False)
    all_key_data = keys_list(gpg, True)
    if key_import['count'] != 0:
        print(f'Key import succesfull. Number of imported keys: {key_import["count"]}')
    else:
        print(
            'Key import failed. Either the key is already imported or another error occured. Check if the key is present in either of the lists below.')




def key_menu(gpg):
    if len(gpg.list_keys()) == 0:
        choice = input('''
Key Handling Menu:    
1. Generate new GPG key
2. Import existing GPG keys
''')
    else:
        print('GPG keys found: ')
        print(gpg.list_keys(True).uids)
        choice = input('''
Key Handling Menu:    
1. Generate new GPG key
2. Import existing GPG keys
3. Delete existing GPG keys
4. List all GPG keys
99. Back to Main Menu
''')
    if choice == '1':
        generated_key = generate_keys(gpg)
        all_key_data = keys_list(gpg, True)
        print(f'Generated Key:{[all_key_data[-1][0], all_key_data[-1][1], all_key_data[-1][2]]}')
    elif choice == '2':
        import_menu(gpg)
    elif choice == '3':
        delete_menu(gpg)
    elif choice == '4':
        print('Public keys:')
        keys_list(gpg, False)
        print('Private keys:')
        keys_list(gpg, True)
    elif choice == '99':
        main_menu(gpg)
    else:
        print('Incorrect Input. Try Again.')
        key_menu(gpg)
def encrypt_decrypt_file(gpg, encrypt):
    if encrypt is True:
        filepath = input('Input path of file to encrypt: ')
        keys_list(gpg, False)
        fingerprint = input('Input fingerprint of the key that will be used for encryption: ')
        byte_output = gpg.encrypt_file(filepath, fingerprint, armor=False)
        new_filepath = filepath + '.gpg'
    else:
        filepath = input('Input path of file to decrypt: ')
        keys_list(gpg, True)
        fingerprint = input('Input fingerprint of the key that will be used for decryption: ')
        byte_output = gpg.decrypt_file(filepath, fingerprint)
        #seperate the fp (filepath) at each '/', ommit the last part (filename), add it together, add a slash to that,
        #add the filename while erasing the .gpg in order to have just file.pdf instead of file.pdf.gpg.pdf
        new_filepath = '/'.join(filepath.split('/')[:-1])+'/'+'.'.join(filepath.split('/')[-1].split('.')[:-1])
    if byte_output.ok is True:
        print('Operation Successful')
        with open(new_filepath, 'wb') as file:
            file.write(byte_output.data)
        print(f'The file can be found in {new_filepath}')
        print('DO NOT CHANGE THE EXTENSION OF THE FILE, THIS WILL STOP IT FROM BEING DECRYPTED CORRECTLY IN THE FUTURE')
    else:
        print('Something went wrong, try again')


def main_menu(gpg):
    print('GPG Menu')
    print(
        '''
        1. GPG keys handling (Generate, Import, etc.)
        2. Encrypt file
        3. Decrypt file
        99. Quit
        '''
    )
    choice = input('')
    if choice == '1':
        key_menu(gpg)
    if choice == '2':
        encrypt_decrypt_file(gpg, True)
    if choice == '3':
        encrypt_decrypt_file(gpg, False)
    if choice == '99':
        confirm = input('Do you want to quit? (y/n) ')
        if confirm == 'y':
            quit()
        else:
            main_menu(gpg)
    else:
        print('Incorrect Input. Try Again')

def main():
    while True:
        gpg = get_gnupg_path()
        if len(gpg.list_keys()) == 0:
            print('No GPG keys found. Taking you to the key handling menu.')
            key_menu(gpg)
        main_menu(gpg)



if __name__ == '__main__':
    main()