import requests as req
import re
import time
from PIL import Image


def image_to_text(image_path):
    image = Image.open('image.jpg')
    width, height = image.size
    print(width, height)
    image = image.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
    image.save('image_new.jpg')
    with open('image_new.jpg', 'rb') as f:
        image_data = f.read()
    post_data = b"------WebKitFormBoundary\r\nContent-Disposition: form-data; name=\"encoded_image\"; filename=\"download.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n" + image_data + b"\r\n------WebKitFormBoundary--\r\n"
    headers = {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
        'Content-Length': str(len(post_data)),
        'Referer': 'https://lens.google.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    response = req.post(f'https://lens.google.com/v3/upload?hl=en-VN&re=df&stcs={time.time_ns() // 10**6}&ep=subb', headers=headers, data=post_data)
    with open('response.html', 'w') as f:
        f.write(response.text)
    # Match text which start with '"vi", [[[' from the response
    text = re.findall(r'\"vi\".*?]\]\]', response.text)
    for res in text:
        if 'SV' in res:
            text = eval(re.findall(r'\[\".*?]', res)[0])
            break
    else:
        return {"text": "No text found"}
    # Đoạn này sẽ work nếu bắt được all text từ ảnh
    text = {
        'Ngành': text[0].split(' - ')[0],
        'Mã ngành': text[0].split(' - ')[1],
        'Họ và tên': text[2],
        'Ngày sinh': text[3],
        'Mã sinh viên': text[4][-6:],
        'Năm học': text[5],
    }
    return text