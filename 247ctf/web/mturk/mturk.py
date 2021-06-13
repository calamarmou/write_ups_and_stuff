#!/usr/bin/env python3

import requests, pytesseract, sys
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

host = "https://0de706d721b0eab6.247ctf.com/"

s = requests.Session()
got_flag = False
unwanted_colors = [[140, 140, 140], [245, 245, 245]]

def clean_that_shit(n) :

    n = n.replace(' ', '').replace('\n', '')
    n = n.replace('!', '1').replace('g', '9').replace('Z', '2')
    n = n.replace('°', '0').replace('\\', '1')
    n = n.replace('A', '4').replace('B', '3')

    return n

def calcul(req_number) :
        r = s.get(host + "mturk.php")
        image = r.content

        with open(f"captcha{req_number}.png", 'wb') as f :
            f.write(image)

        captcha_file = Image.open(f"captcha{req_number}.png")
        captcha_data = captcha_file.load()
        width, height = captcha_file.size

        try :
            new_size = (200, 40)
            new_im = Image.new("RGB", new_size, color = "white")
            new_im.paste(captcha_file, ((new_size[0] - width) // 2, (new_size[1] - height) // 2))

            img_without_lines = f"captcha_without_lines{req_number}.png"
            new_im.save(img_without_lines)

            captcha_file = Image.open(img_without_lines)
            captcha_data = captcha_file.load()
            width, height = captcha_file.size
        except Exception as e :
            print(e)

        try :
            for w in range(width) :
                for h in range(height) :
                    r, g, b = captcha_data[w, h]
                    if [r, g, b] in unwanted_colors:
                        captcha_data[w, h] = 255, 255, 255 
                    else :
                        captcha_data[w, h] = (r, g, b)
        except Exception as e :
            print(e) 

        try :
            captcha_file.save(img_without_lines)
        except Exception as e :
            print(e)

        captcha_text = pytesseract.image_to_string(img_without_lines)
        captcha_text = captcha_text.replace('*', '+')
        print(captcha_text)
        if '+' in captcha_text :
            captcha_text = captcha_text.split('+')
        else :
            return 0


        n1 = clean_that_shit(captcha_text[0])
        n2 = clean_that_shit(captcha_text[1])
        print("********************")
        print(f"Tesseract output for {req_number}: {captcha_text}")
        print(f"n1 : {n1}, n2 : {n2}")
        print("***************")
        exit()
        if any(n not in "0123456789" for n in n1) :
            return 0 
        if any(n not in "0123456789" for n in n2) :
            return 0

        print(f"Après le split + : {n1, n2}")
        print(int(n1) + int(n2))
        
        data = {"captcha" : int(n1) + int(n2)}
        r = s.post(host, data = data)
        if "Valid CAPTCHA!" in r.text :
            print(r.text)
            return 1

if __name__ == "__main__" :

    req_number = 1
    total_valid = 0

    while got_flag == False :
        with ThreadPoolExecutor(max_workers = 40) as executor :
            if executor.submit(calcul, req_number % 40) == 1 :
                total_valid += 1
            if total_valid == 100 :
                got_flag = True
            req_number += 1
            if req_number == 20 :
                got_flag = True

   #calcul(req_number)
