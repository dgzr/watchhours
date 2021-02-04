#!/data/data/com.termux/files/usr/bin/python
# pake aja broh, free kok (no password :'v)
# dtz-aditia 2021.02.05
import requests,time,json,bs4

g = "\033[1;32m"
p = "\033[1;37m"
r = "\033[1;31m"

class Watchhours:
	def __init__(self):
		self.home = "https://watchhours.com/index.php"
		self.headers = {
			"Host":"watchhours.com",
			"Connection":"keep-alive",
			"User-Agent":"",
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Referer": self.home,
			"Cookie":"",
		}
		self.banner = (f"""
                -----
            BOT WATCHHOURS
        ---------------------
@author : https://t.me/aditia_dtz
@note : -""")
		self.getCookie()

	def getCookie(self):
		bs4.os.system('clear')
		print(self.banner)
		print(f"""
{g}~{p} 1. Edit Config
{g}~{p} 2. Start Bot
""")
		self.set = int(input(f"\n {g}• {p}Set : "))
		if self.set == 1:
			self.cuki = input(f"\n {g}• {p}Cookie : ")
			self.user_agent = input(f" {g}•{p} User Agent : ")
			if self.cuki and self.user_agent != '':
				with open('.logs.json','w') as f:
					f.write(json.dumps({"cuki":self.cuki,"uwa":self.user_agent}))
				print(f" {g}• {p}Config saved!!")
				time.sleep(0.8)
				self.getCookie()
			else:
				exit(f" {r}• {p}Config jangan komsong !!")
		elif self.set == 2:
			if bs4.os.path.isfile('.logs.json'):
				self.dat = json.loads(open('.logs.json').read())
				self.headers["User-Agent"] = self.dat["uwa"]
				self.headers["Cookie"] = self.dat["cuki"]
				self.login()
			else:
				exit(f" {r}• {p} Edit comnfig sblm run!")
		else:
			exit(f" {r}• {p} Error")

	def waiting(self,x):
		for y in range(x, 0, -1):
			bs4.sys.stdout.write("\r {}• {}{:2d} {}watching videos ".format(g,p,y,g))
			bs4.sys.stdout.flush()
			time.sleep(1)

	def login(self):
		bs4.os.system("clear")
		print(self.banner)
		self.page = requests.get("https://watchhours.com/index.php?page=videos", headers=self.headers).text
#		print(self.page)
		self.soup = bs4.BeautifulSoup(self.page,"html.parser")
		if self.soup.find("div",class_="info") != None:
			self.name = self.soup.find("div",class_="info").findAll('span')[0].text.strip().split('\n')[0] # username
			self.coin = self.soup.find("b",id="c_coins").text
			self.duit = self.soup.find("small",class_="text-success").text.split()[-1]
			self.view = bs4.re.search(r"<span\>(Total\sViews.*?)<\/span>",self.page).group(1)
			print(f"""
~ {g}•{p} Welcome {self.name} 👋
~ {g}•{p} Coins : {self.coin}
~ {g}•{p} Balance : {self.duit}
~ {g}•{p} {self.view}
""")
			print(f" {g}• {p}Bot start!")
			if("There is no video available yet!" not in self.page):
				self.headers["Referer"] = "https://watchhours.com/index.php?page=videos"
				for i,x in enumerate(self.soup.findAll("div",class_="website_block")):
					try:
						self.id = x["id"]
						print(f"\n{p} • ({i+1}) Visit => {g}{self.id}{p}")
						self.url = "https://watchhours.com/?page=videos&vid={}".format(self.id)
						self.pg = requests.get(self.url,headers=self.headers)
						self.soup = bs4.BeautifulSoup(self.pg.text, "html.parser")
						self.count = self.soup.find("div",id="countdown").find("b").text.split('/')[-1].split()[0]
						self.waiting(int(self.count))
						self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
						self.headers["Origin"] = "https://watchhours.com"
						self.headers["Referer"] = self.url
						self.token = bs4.re.search(r"var\stoken\s=\s'(.*?)'",self.pg.text)
						if self.token is not None:
							self.get_coin = requests.post("https://watchhours.com/system/gateways/video.php",data={"data": self.id, "token": self.token.group(1)}, headers=self.headers)
							if "SUCCESS" in self.get_coin.text:
								self.earn = bs4.BeautifulSoup(self.get_coin.text,"html.parser").findAll("b")[-1].text
								print(f"\n • {g} success, you earning {p}{self.earn}")
							else:
								print(f"\n • {r} failed to get coins!")
								continue
						else:
							print(f"\n • {r} failed to get tokens!")
					except EOFError:
						continue
				self.headers["Origin"]=""
				self.headers["Content-Type"]=""
				self.headers["Referer"]=self.home
				self.login()
			else:
				exit(f"\n • {r} Video habis, balik lagi besok!!")
		else:
			exit(f"\n • {r} failed to get data ,check your config!!")

if __name__=="__main__":
	try:
		bs4.os.system("xdg-open https://youtube.com/channel/UCfTsQXMv33z6geEbaeZMi5w")
		Watchhours()
	except:
		raise TypeError("Goblogggggg!!")
