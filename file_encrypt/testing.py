import os
from pathlib import Path
import gnupg


def create_config_file():
    print('Creating config file...')
    with open('config.txt', 'w') as file:
        file.write('#GNUPG config file\n')
        file.write('#This is a text file used for configuration of the file-gpg-image tool.\n')


def get_gnupg_path(config_file):
    if config_file is True:
        with open('config.txt', 'r') as file:
            for line_number, line in enumerate(file, start=1):
                print('aconf')
                if 'GPG_DIR=' in line:
                    gpg_dir = line[8:].split('\n')[0]
                    return gpg_dir
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
            return gpg_dir
def gpg_config():

    if os.path.exists('config.txt'):
        gpg_dir = get_gnupg_path(True)
        print('y')
    else:
        gpg_dir = get_gnupg_path(False)
        print('n')
    return gnupg.GPG(homedir=gpg_dir)

def main():
    gpg_config()


if __name__ == '__main__':
    main()