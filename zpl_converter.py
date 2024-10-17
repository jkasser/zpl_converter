from pathlib import Path
import requests
import shutil

# DIRS
ROOT_DIR = Path.cwd()
OUT_FILES = (ROOT_DIR / 'pdfs')

# API Params
BASE_URL = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/'
HEADERS = {'Accept': 'application/pdf'}


def read_file_into_string(file):
    with open(file, 'r') as zpl_file:
        zpl_content = zpl_file.read()
    return zpl_content


def send_file_to_converter(file_contents, output_name):
    files = {'file': file_contents}
    response = requests.post(BASE_URL, headers=HEADERS, files=files, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        if not OUT_FILES.exists():
            Path(OUT_FILES).mkdir(parents=True)
        with open(f'{str(OUT_FILES)}\\{output_name}.pdf', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)


def main():
    for file in ROOT_DIR.iterdir():
        if str(file).endswith('.zpl'):
            contents = read_file_into_string(file)
            send_file_to_converter(contents, file.stem)


if __name__ == '__main__':
    main()
