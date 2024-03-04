# https://medium.com/bootdotdev/aes-256-cipher-python-cryptography-examples-b877b9d2e45e
# AES 256 encryption/decryption using pycrypto library
import base64
import hashlib
import os
import sys

from Crypto import Random
from Crypto.Cipher import AES


class PyAES256:
    # constructor
    def __init__(self):
        pass
        
    # pad with spaces at the end of the text
    # becouse AES needs 16 byte blocks
    def pad(self, s):
        block_size = 16
        remainder = len(s) % block_size
        padding_needed = block_size - remainder
        return s + padding_needed * ' '

    # remove the extra spaces at the end
    def unpad(self, s): 
        return s.rstrip()

    def bytes_to_str(self, b):    
        return ''.join([chr(c) for c in b])

    def str_to_bytes(self, b):
        return bytes.fromhex(''.join([hex(ord(c)).replace('x','0')[-2:] for c in b]))    

    # do encryption  
    # @staticmethod  
    def encrypt(self, plain_text, password):
        # generate a random salt    
        salt = os.urandom(AES.block_size)
        # print('salt: ', salt)

        # generate a random iv
        iv = Random.new().read(AES.block_size)
        # print('increment vector: ', iv)

        # use the Scrypt KDF to get a private key from the password
        private_key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
        # print('private key: ', private_key)

        # pad text with spaces to be valid for AES CBC mode
        padded_text = self.pad(plain_text)
                
        # create cipher config
        cipher_config = AES.new(private_key, AES.MODE_CBC, iv)    

        ciper = cipher_config.encrypt(bytes(padded_text,'utf-8'))
        # print('Chipper: ', ciper)
        
        # return a dictionary with the encrypted text
        ciper_text = base64.b64encode(ciper)
        # print('Chipper Text: ', ciper_text)

        url_text = self.bytes_to_str(base64.urlsafe_b64encode(ciper_text))

        return {
            # 'cipher_text': ciper_text,          # convert to url safe
            'url': url_text,                    # set as url encryption
            'salt': base64.b64encode(salt),     # salt & iv save to session 
            'iv': base64.b64encode(iv),                     
        }    

    # do decription
    # @staticmethod
    def decrypt(self, url, salt, iv, password):
        # decode the dictionary entries from base64
        salt = base64.b64decode(salt)
        # print('salt: ', salt)

        ciper_text = base64.b64decode(base64.urlsafe_b64decode(self.str_to_bytes(url)))
        # print('chipper text: ', ciper_text)

        iv = base64.b64decode(iv)
        # print('increment vector: ', iv)

        # url_text = enc_dict['url']
        # print('URL: ', url_text)

        # generate the private key from the password and salt
        private_key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
        # print('private key: ', private_key)

        # create the cipher config
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        # print('chipper: ', cipher)

        # decrypt the cipher text
        decrypted = cipher.decrypt(ciper_text)
        # print('decript: ', decrypted)

        # unpad the text to remove the added spaces
        original = self.unpad(decrypted)
        # print('unpad: ', original)

        return original


# test module level
if __name__=='__main__':
    print('Begin Test ENCRYPT')
    print('------------------')
    secret_text = input("Secret Text: ")
    password = 'g_7me8rl2m#a_h2oresgt2#ni=3_4*!ai*=rtsq)yi!g7_5-51'     

    lib = PyAES256()
    res_enc = lib.encrypt(secret_text, password)
    print('Encrypt result:', res_enc)

    print('')
    print('Begin Test DECRYPT')
    print('------------------')
    
    url = res_enc['url']
    salt = res_enc['salt']
    iv = res_enc['iv']
    print('Parameter')
    print('PASSWORD:', password)
    print('URL:', url)
    print('SALT:', salt)
    print('IV:', iv)    

    res_dec = lib.decrypt(url, salt, iv, password)
    print('Decrypt result:', bytes.decode(res_dec))
    print('')
    
