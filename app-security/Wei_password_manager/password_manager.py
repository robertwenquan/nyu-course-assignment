#@PydevCodeAnalysisIgnore
import os

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

from binascii import b2a_hex, a2b_hex



STORE_DATA='password_result.txt'
global KEY
global cipher_CTR
IV = 'SIXTEEN_BYTE_KEY'

def my_encryption(plaintext, mode):
    encrypt_mode = AES.MODE_CBC
    if mode == 'CBC':
    	encrypt_mode = AES.MODE_CBC
    elif mode == 'CTR':
        encrypt_mode = AES.MODE_CTR
    elif mode == 'ECB':
    	encrypt_mode = AES.MODE_ECB
    else:
    	pass
    if mode != 'CTR':
        cipher = AES.new(KEY, encrypt_mode, IV)
    else:
        cipher = cipher_CTR
    length = 16
    count = len(plaintext)
    add = length - (count % length)
    plaintext = plaintext + ('\0' * add)
    ciphertext = cipher.encrypt(plaintext)
    result = b2a_hex(ciphertext)
    #print len(result),result
    return result

def my_decryption(text, mode):
    encrypt_mode = AES.MODE_CBC
    if mode == 'CBC':
        encrypt_mode = AES.MODE_CBC
    elif mode == 'CTR':
        encrypt_mode = AES.MODE_CTR
    elif mode == 'ECB':
        encrypt_mode = AES.MODE_ECB
    else:
        pass
    if mode != 'CTR':
        cipher = AES.new(KEY, encrypt_mode, IV)
    else:
        cipher = cipher_CTR
    #print text,len(text)
    plain_text = cipher.decrypt(a2b_hex(text))
    return plain_text.rstrip('\0')

def check_exist(username, pwd, content):
    usr_dict={}
    for item in content:
        tmp_row = item.split(' ')
        usr_dict[tmp_row[0]]=[tmp_row[1],tmp_row[2]]
        
    if username in usr_dict:
        print 'username already exists',
        curr_c_pwd = usr_dict[username][1]
        curr_c_mode = usr_dict[username][0]
        curr_p_pwd = my_decryption(curr_c_pwd, curr_c_mode)
        #print curr_c_mode,curr_c_pwd,curr_p_pwd
        if curr_p_pwd == pwd:
            print 'password match'
        else:
            print 'wrong password'
    else:
        print 'store new pair of username and password'
        return False


def check_input_legal(input_string):
    tmp_cnt=0
    for x in input_string:
        if x == ' ':
            tmp_cnt+=1
    if tmp_cnt!=1:
        return False
    return True

def check_mode_legal(input_mode):
    if len(input_mode) != 3:
        return False
    if input_mode not in ['CBC', 'CTR', 'ECB']:
        return False
    return True

def ctr_secret():
    return 'countersecretttt'
ctr_counter=ctr_secret()

def get_master_key():
    if not os.path.exists('./.master_key'):
        key=b2a_hex(os.urandom(16))
        f=file('./.master_key','wb')
        f.write(key)
        f.close()
        return key
    else:
        key=file('./.master_key','rb').read()
        if len(key)==0:
            key=b2a_hex(os.urandom(16))
            f=file('./.master_key','wb')
            f.write(key)
            f.close()
        return key
    
def main():
    global KEY
    KEY=get_master_key()
    global cipher_CTR
    cipher_CTR=AES.new(KEY, AES.MODE_CTR, counter=lambda: ctr_counter)
    
    print 'Program start, press CTRL+D to exit'
    print "Notice: the string of 'username' and 'password' should not contains space"
    if os.path.exists(STORE_DATA):
        file_r = open(STORE_DATA, 'rb+')
        content = [item.rstrip('\n') for item in file_r.readlines()]
        file_r.close()
    else:
        content = []

    file_w = open(STORE_DATA, 'ab+')

    while True:
    	try:
    	    # input username password
     	    input_string=raw_input("please input username password,(there is a space between the username and password)\n")
     	    if not check_input_legal(input_string):
                print 'Wrong input, the format must be username password'
                continue
            usr,pwd=input_string.split(' ')[0],input_string.split(' ')[1]
            result=check_exist(usr,pwd,content)
            if result == False:
                # choose encryption mode
                input_mode=raw_input('please input encrypt mode: ECB, CTR or CBC\n')
                if not check_mode_legal(input_mode):
            	    print 'Wrong mode, only support ECB, CTR, CBC',
            	    continue
                encrypt_pwd=my_encryption(pwd,input_mode)
                curr_row=usr+' '+input_mode+' '+encrypt_pwd
                content.append(curr_row)
                d=file_w.write(curr_row+'\n')
     	       	   
        except EOFError:
            print 'End'
            file_w.close()
            break

main()
