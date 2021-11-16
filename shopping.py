from os import getcwd
from os import listdir
from os import mkdir
from datetime import date
from pytz import timezone
from datetime import datetime
import json
from re import search


class date_time:

	def date():
		zone = timezone("Asia/Kolkata")
		time = str(datetime.now(zone))
		date_ = time.split(" ")[0]
		return date_


	def time():
		zone = timezone("Asia/Kolkata")
		time = str(datetime.now(zone))
		time  = time.split(" ")[1].split('.')[0]
		return time

	def month():
		months = [0,"january","february","march","april","may","jun","july","august","september","october","november","december"]
		zone = timezone("Asia/Kolkata")
		time = str(datetime.now(zone))
		yr = time.split(" ")[0].split('-')[0]
		indx = int(time.split(" ")[0].split('-')[1])
		mth = f"{yr}-{months[indx]}"
		return mth



class shopping_data_entry:

	def __init__(self):
		self.date = date_time.date()
		self.time = date_time.time()
		self.month = date_time.month()
		self.check_file()
		print("loading contents...")
		self.contents = self.load()
		print(self.contents)
		self.wrt_json()
		self.data_entry()

	
	def data_entry(self):
		prt = """'new' for data entry\n'show' to see today's data\n'quit' to exit """
		print(prt)
		while True:
			mode = input(">>> ")
			if mode == "quit":
				break
			if mode == "new":
				name = input('enter name : ')
				quantity = input("enter quantity : ")
				cost = int(input("enter the cost : "))
				quantity = self.unite_conv(quantity)
				today = self.contents[self.date]
				if name in today:
					lis  = today[name]
					qnty = lis[0]

					quantity_add = float(search(r"\d*",qnty).group(0)) + float(search(r'\d*',quantity).group(0))
					unit = search("[a-zA-Z]+",quantity).group(0)
			
					lis[0] = f"{quantity_add} {unit}"
					lis[1] += cost
					lis[2] = date_time.time()
					self.contents[self.date][name] = lis 
					self.wrt_json()

				if name not in today:
					self.contents[self.date][name] = [quantity,cost,date_time.time()]
					self.wrt_json()

			if mode=="show":
				print(json.dumps(self.contents[self.date]))


	def unite_conv(self,quantity):
		amount = float(search(r'\d*[.]*\d*',quantity).group(0))
		unite = search(r'[a-zA-Z]+',quantity).group(0)
		if unite == "gram" or unit == "g":
			amount /= 1000
			unite = 'kg'

		quantity = f"{amount} {unite}"
		return quantity




	def wrt_json(self):
		with open(f"{getcwd()}/shopping/{self.month}","w") as file:
			if self.date not in self.contents:
				self.contents[self.date] = {}
			json.dump(self.contents,file)


	def load(self):
		with open(f"{getcwd()}/shopping/{self.month}",'r') as file:
			contents = json.load(file)
			return contents


	def check_file(self):
		if "shopping" not in listdir(getcwd()):
			mkdir(f"{getcwd()}/shopping")
		files_path = f"{getcwd()}/shopping/"
		files = listdir(files_path)
		for i in files:
			if self.month == i:
				print("file already exsits..")
				return True
		else:
			with open(f"{getcwd()}/shopping/{self.month}",'w') as file:
				dummy_dick = {
					self.date:{}
				}
				json.dump(dummy_dick,file)


shop = shopping_data_entry()
