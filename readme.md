# MIUI-LSA Decryptor

This project provides a simple tool to decrypt MIUI LSA image files from Xiaomi devices.

## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine:

```powershell
git clone <repository-url>
```
Replace `<repository-url>` with the actual URL of this repository.

### 2. Install Requirements

Navigate to the project directory and install the required Python packages:

```powershell
cd "c:\Users\Shivam\Desktop\Devops basics\miui-lsa"
pip install -r requirements.txt
```

### 3. Prepare Your LSA Files

Place your `.lsa` or `.lsav` files in a directory of your choice. Note the full file path or directory where your files are stored.

### 4. Decrypt Images

To decrypt a single file:

```powershell
python decryptor.py <filepath>
```
Replace `<filepath>` with the path to your `.lsa` or `.lsav` file. Example:

```powershell
python decryptor.py IMG_20230312_194242.3e751332435bfad27569ca4efed1b602.lsa
```

To decrypt all files in a directory:

```powershell
python decryptor.py <directory_path>
```

The decrypted image(s) will be saved in the same directory as the input file(s).

## Decryption Keys

The script uses hardcoded decryption keys:

```python
sAesIv = 22696201676385068962342234041843478898
secretKey = b'0\x82\x04l0\x82\x03T\xa0\x03\x02\x01\x02\x02\t\x00'
```

These keys work for most MIUI LSA files. If your file does not decrypt correctly, you may need to extract the key from your device's Gallery APK certificate. See below for instructions.

### How to Get Your Own Key

If the default key does not work, extract the first 16 bytes of the Gallery APK's certificate:

1. Use `keytool` to print the certificate:
	```powershell
	keytool.exe -printcert -rfc -jarfile com.miui.gallery.apk
	```
2. Copy the certificate block and convert it from base64 to hex (the first 16 bytes).
3. Use it in Python:
	```python
	secretKey = bytes.fromhex('<your_hex_key>')
	```

## Notes
- Ensure you have Python installed on your system.
- The output will be a decrypted image file (e.g., `.jpg`).
- The encrypted file name should be in the format `<filename>.<md5_of_key>.lsa`.
- If the MD5 of the key is `3e751332435bfad27569ca4efed1b602`, it should work for most files.

## Source & Credits

This project is inspired by:
- https://github.com/ObikBobik/miui-cloud-decryptor

## License
Specify your license here.

<!-- Follow these steps to get your key if the above on enot works in your case  -->
First, install requirements

pip install -r requirements.txt
And then

python ./miui-cloud-decrypt.py <one single file .lsa or .lsav / directory of .lsa and .lsav files>
Important note
The encrypted file must have the following name: <file name>.<md5 of key>.lsa and if the md5 of the key is 3e751332435bfad27569ca4efed1b602 it probably will be 100% decrypted but if not it probably won't decrypt the file correctly. You'll have to change secretKey to the first 16 bytes of the gallery apk's certificate:

keytool.exe -printcert -rfc -jarfile com.miui.gallery.apk
Outputs:

Certificate #1:
Certificate owner: EMAILADDRESS=miui@xiaomi.com, CN=MIUI, OU=MIUI, O=Xiaomi, L=Beijing, ST=Beijing, C=CN

-----BEGIN CERTIFICATE-----
MIIEbDCCA1SgAwIBAgIJAOVSqOy5ARt8MA0GCSqGSIb3DQEBBQUAMIGAMQswCQYD
VQQGEwJDTjEQMA4GA1UECBMHQmVpamluZzEQMA4GA1UEBxMHQmVpamluZzEPMA0G
A1UEChMGWGlhb21pMQ0wCwYDVQQLEwRNSVVJMQ0wCwYDVQQDEwRNSVVJMR4wHAYJ
KoZIhvcNAQkBFg9taXVpQHhpYW9taS5jb20wHhcNMTExMjA2MDMyNjI2WhcNMzkw
NDIzMDMyNjI2WjCBgDELMAkGA1UEBhMCQ04xEDAOBgNVBAgTB0JlaWppbmcxEDAO
BgNVBAcTB0JlaWppbmcxDzANBgNVBAoTBlhpYW9taTENMAsGA1UECxMETUlVSTEN
MAsGA1UEAxMETUlVSTEeMBwGCSqGSIb3DQEJARYPbWl1aUB4aWFvbWkuY29tMIIB
IDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAx4ZWipr/JTrXTF0+b7/6Ev7U
TNMkTxiWDsVRG7VR5BMRUZcjSEURLMPfm7rNPg9LNSjNh+05fVd9yQCOnLxqJfwG
ZNOj9EAkN4bbiyUNQPbxSMmjzW+8LdjSQDm9aolyob3uKMMIeYv6m7O1SYd7EPmO
Jl8RjAXyZFN9leKTORV7nSoxSF4MgjUhzKbQtyGoQyYAB21mniCsQ6pYi1LBHCpR
8ExrsxrWroVzmRr+jklX1UlZH8uD7GLR2jWxcn3GtjABpe84e1pxhsHmjaEyV3K1
MHsbxznvI2ue/gbVLcrx4ydo40A+VePsVgKM9WgM+zOXHM94cFcrxH0+Ov+jhQIB
A6OB6DCB5TAdBgNVHQ4EFgQUka4vjHLjBfkqqfdFLioxYLhBoVwwgbUGA1UdIwSB
rTCBqoAUka4vjHLjBfkqqfdFLioxYLhBoVyhgYakgYMwgYAxCzAJBgNVBAYTAkNO
MRAwDgYDVQQIEwdCZWlqaW5nMRAwDgYDVQQHEwdCZWlqaW5nMQ8wDQYDVQQKEwZY
aWFvbWkxDTALBgNVBAsTBE1JVUkxDTALBgNVBAMTBE1JVUkxHjAcBgkqhkiG9w0B
CQEWD21pdWlAeGlhb21pLmNvbYIJAOVSqOy5ARt8MAwGA1UdEwQFMAMBAf8wDQYJ
KoZIhvcNAQEFBQADggEBADs6aZzrSXMA8quGy9QcUTRAv2CqXEOYTrHaFA7zBUTZ
+7s3M98ksm8nA9f/xkW/WYpeYCNZapR+kXMVQvLCadCBamnJLfm/6LHJvDxUxGwS
NVu0Yp/mAgyp0V+NYVXcVYb1YW24BuzqLQa9g+MrXxP1oE/j5apRTwXfPVVVJsY9
PWKs8Are6JS5I8JpjcVxvFLHVv+noiIdg00Qy3F1yGTDCHL+IXwxRC3/AECmei+x
yLpj6sLVuj2OdrT/Kkmw24oz70rg3QqEDdKocUy1UxpWt4aBnsnrEFHZGyP94GvZ
0HCPFQxPnv5qQWykpeDCOpUq+TGtNXn7SosZ3pj2S9k=
-----END CERTIFICATE-----
And after converting from base 64 to hex: 3082046c30820354a003020102020900...... Now use it in python:

secretKey = bytes.fromhex('3082046c30820354a003020102020900')
Thank you for reading <3



The Source help me in this video 
https://github.com/ObikBobik/miui-cloud-decryptor