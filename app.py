import tempfile
import time
from flask import Flask, render_template, request, send_file
from itertools import permutations
from ch2en import ch2en
from gregorian2lunar import gregorian2lunar
import subprocess
import requests
import asyncio
import websockets

app = Flask(__name__, template_folder='./templates')


def gen_name_list(names):
    name_list = []
    for n in names:
        try:
            name_list += [ch2en.zhuen(n)] # 全名
            name_list += [ch2en.zhuen(n[1])] # 只有姓
            name_list += [ch2en.zhuen(n[1:])] # 沒有姓

            name_list += [ch2en.cangjie(n).lower()]
            name_list += [ch2en.cangjie(n[1]).lower()]
            name_list += [ch2en.cangjie(n[1:]).lower()]
        except:
            name_list += n
    return name_list


def format_num(n):
    if n <10:
        return [f'0{n}',f'{n}']
    else:
        return [f'{n}']


def gen_birth(birth):
    birth_list = []
    lunar = []
    for b in birth:
        b = [int(i) for i in b.split('/')]
        b += [b[0] - 1911]
        birth_list += b
        lunar += gregorian2lunar.lunar([b[0],b[1],b[2]])[1:]
    lst = []
    for i in lunar + birth_list:
        lst += format_num(i)
    return lst

def gen_phone(phones):
    phone_list = []
    for p in phones:
        for i in range(8):
            for j in range(2,7):
                phone_list += [p[i:i+j]]
    return phone_list


def gen_id(user_ids):
    print(user_ids)

    uid_list = list()

    for uid in user_ids:
        # print(uid)
        print(uid)
        uid_list += [uid]
        for i in range(len(uid)):
                for j in range(2,len(uid)):
                    uid_list += [uid[i:i+j]]
    # print(uid_list)
    return list(set(uid_list))





@app.route('/')
def index():
    return render_template('home.html')

@app.route('/osint', methods=['GET', 'POST'])
def osint():
    if request.method == 'GET':
        return render_template('osint.html', osint_result='GET', data={})
    elif request.method == 'POST':
        print(request)
        data = {}
        for key in request.form:
            if key:
                data[key] = [x.strip() for x in request.form[key].split(',') if x.strip()][:10]
            else:
                data[key] = []        

        if request.form['action'] == 'GENERATE':


            name_list = gen_name_list(data.get('name'))
            birth_list = gen_birth(data.get('birth'))
            phone_list = gen_phone(data.get('phone'))
            other_list = data.get('other')
            id_list = gen_id(data.get('id'))
            
            # print(id_list)
            all_list = [name_list,birth_list,phone_list,id_list,other_list]
            lst = []

            for i,j in permutations(all_list,2):
                for k,l in permutations(i+j,2):
                    lst += [k+l]
                for k,l,m in permutations(i+j,3):
                    lst += [k+l+m]
                for k,l,m,n in permutations(i+j,4):
                    lst += [k+l+m+n]
                    
            lst = list(set(lst))
            txt = tempfile.TemporaryFile()
            ret = '\n'.join(lst)
            txt.write(str.encode(ret))
            txt.seek(0)
            return send_file(txt, as_attachment=True, attachment_filename='password.txt')
        else:
            return render_template('osint.html', osint_result=data, data=data)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',port=9000)
