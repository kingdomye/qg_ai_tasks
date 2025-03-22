import datetime
import yagmail
import hashlib
import base64
import random
import time
import uuid
import os
import re

class SimpleAct:
    def __init__(self):
        self.subjects=['语文', '数学','英语','日语','俄语','德语','法语','西班牙语','物理', '化学', '生物', '政治', '历史', '地理', '通用','信息']
        self.schedule=['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '通用','信息', '体育','音乐', '美术', '班会']
        self.arrange=['1','2','3','4','5','','1','2','3','','1','2','3','4','5']
    def Random_File_Name(self,filename):
        ext = os.path.splitext(filename)[1]
        new_filename = uuid.uuid4().hex + ext
        return new_filename
    def Upload_Check(self,filename,type):
        file_type=filename.split('.')[-1]
        file_type_lower=file_type.lower()
        if file_type_lower==type:
            return True
        return False
    def Random_Password(self):
        password=''
        for num in range(6):
            item=random.randint(0,9)
            password+=str(item)
        return password
    def Send_Email(self,e_mail):
        email_password=self.Password_Decrypt('fntpdn1ld3J2ZX5xcW9rbA==')
        mail=yagmail.SMTP('yrclass@foxmail.com',email_password,'smtp.qq.com')
        password=self.Random_Password()
        content=f'亲爱的用户：您好！\n这是您在YR-CLASS的动态口令码:{password}\n温馨提示：口令码涉及更改账号内容，请误交给他人'
        mail.send(e_mail,'找回账号和密码',content)
        mail.close()
        return password
    def Password_Encrypt(self,password):
        key=hashlib.md5(password.encode()).hexdigest()
        encrypt_first=''
        for item in key:
            if '0'<=item<='9':
                encrypt_first+=item
        encrypt_second=''
        for num,word in zip(encrypt_first[:len(password)],password):
            encrypt_second+=chr(int(num)+ord(word))
        with open('key.key','wb') as f:
            f.write(base64.b64encode(encrypt_first.encode()))
        return base64.b64encode(encrypt_second.encode())
    def Password_Decrypt(self,ciphertext):
        key=b'ODQ0MjkwNDQ1MTgxNzgxMjE2NDUz'
        decrypt_first=str(base64.b64decode(ciphertext.encode()).decode())
        key=str(base64.b64decode(key).decode())
        decrypt_second=''
        for index,item in enumerate(decrypt_first):
            decrypt_second+=chr(ord(item)-int(key[index]))
        return decrypt_second
    def Now_time(self):
        return int(time.time())
    def IF_Email(self,e_mail):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, e_mail):
            return True
        else:
            return False
    def Random_Class_Num(self):
        class_num=''
        for num in range(8):
            item = random.randint(0, 9)
            class_num += str(item)
        return class_num
    def File_Extension(self,filename):
        extension=os.path.splitext(filename)
        if extension[1]=='':
            return False
        return extension[1]
    def File_Size(self,filepath):
        size=os.path.getsize(filepath)
        kb=str(round(size/8/1024,2))+'kb'
        return kb
    def Now_Date(self):
        return datetime.date.today()
    def Date_Stamp(self,date_str):
        date=time.strptime(date_str, '%Y-%m-%d')
        timestamp=time.mktime(date)
        return timestamp

if __name__ == '__main__':
    a=SimpleAct()
    print(a.Password_Decrypt('fntpdn1ld3J2ZX5xcW9rbA=='))
