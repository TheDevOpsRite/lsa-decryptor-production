import os
import filetype
from Crypto.Cipher import AES
from Crypto.Util import Counter

sAesIv = 22696201676385068962342234041843478898
secretKey = b'0\x82\x04l0\x82\x03T\xa0\x03\x02\x01\x02\x02\t\x00'


def decrypt_file_header(filename: str | os.PathLike):
    with open(filename, 'rb') as file:
        size = os.path.getsize(filename)
        header_size = max(min(1024, size), 16)
        counter = Counter.new(128, initial_value=sAesIv)
        aes = AES.new(secretKey, mode=AES.MODE_CTR, counter=counter)
        return aes.decrypt(file.read(header_size)) + file.read(size - header_size)


def decrypt_file(filename: str | os.PathLike):
    with open(filename, 'rb') as file:
        counter = Counter.new(128, initial_value=sAesIv)
        aes = AES.new(secretKey, mode=AES.MODE_CTR, counter=counter)
        return aes.decrypt(file.read())


def main(path):
    if os.path.isdir(path):
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            filename = filename.split('.')
            if filename[-1] == 'lsa':
                data = decrypt_file(filepath)
            elif filename[-1] == 'lsav':
                data = decrypt_file_header(filepath)
            else:
                continue
            ext = filetype.guess_extension(data[:1024]) or 'unknown'
            outpath = os.path.join(path, f'{filename[0]}.{ext}')
            with open(outpath, 'wb') as file:
                file.write(data)
                print(f'{".".join(filename)} has been decrypted successfully')
    else:
        basename = os.path.basename(path).split('.')
        dirname = os.path.dirname(path)
        if basename[-1] == 'lsa':
            data = decrypt_file(path)
        elif basename[-1] == 'lsav':
            data = decrypt_file_header(path)
        else:
            print('Provided file must be .lsa or .lsav')
            return
        ext = filetype.guess_extension(data[:1024]) or 'unknown'
        outpath = os.path.join(dirname, f'{basename[0]}.{ext}')
        with open(outpath, 'wb') as file:
            file.write(data)
        print(f'{".".join(basename)} has been decrypted successfully')


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f'Usage:\n\t'
              f'python ./miui-cloud-decrypt.py <file .lsa or .lsav / directory of files>\n'
              f'Example:\n\t'
              f'python ./miui-cloud-decrypt.py ./01234.56789.lsa\n\t'
              f'or\n\t'
              f'python ./miui-cloud-decrypt.py ./MyLsavFiles')
