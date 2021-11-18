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



class shopping:

	def __init__(self):
		self.date = date_time.date()
		self.time = date_time.time()
		self.month = date_time.month()
		self.check_file()
		print("loading contents...")
		self.contents = self.load()
		self.wrt_json()
		self.data_entry()

	
	def data_entry(self):
		prt = """\n'--help' how to use\n"""
		print(prt)
		while True:
			mode = input("./shopping.py> ")
			mode = mode.strip()

			if mode == "quit":
				break

			if mode == "new":
				name = input('enter name : ').strip()
				quantity = input("enter quantity : ").strip()
				today = self.contents[self.date]
				try:
					cost = int(input("enter the cost : "))
				except:
					cost = 0
				
				if name == "":
					pass

				elif quantity == "":
					print("ERROR: please put somthing in quantity :)")
				
				elif name in today:
					quantity = self.unite_conv(quantity)
					lis  = today[name]
					qnty = lis[0]

					quantity_add = float(search(r"\d*[.]*\d*",qnty).group(0)) + float(search(r"\d*[.]*\d*",quantity).group(0))
					try:
						unite = search("[a-zA-Z]+",quantity).group(0)
					except:
						unite = ''

					lis[0] = f"{quantity_add} {unite}"
					lis[1] += cost
					lis[2] = date_time.time()
					self.contents[self.date][name] = lis 
					self.wrt_json()


				elif name not in today:
					quantity = self.unite_conv(quantity)
					self.contents[self.date][name] = [quantity,cost,date_time.time()]
					self.wrt_json()


			if mode=="show":
				print(json.dumps(self.contents[self.date]))

			if mode == "delete":
				self.deletion_mode()

			if mode == "modify":
				self.modification_mode()

			if mode=="--help":
				prt = """\n'new' to insert new data\n'show' to see today's data\n'quit' to exit\ndelete to enter in deletion mode\nmodify to enter modification mode\n"""
				print(prt)



	def deletion_mode(self):
		print("\ndeletion mode !!!!\n")
		name = input("enter product name : ").strip()
		try:
			del self.contents[self.date][name]
			self.wrt_json()
			print(f"product {name} deleted successfully !!!\n")
		except:
			print(f'sorry ! the product {name} is not exists\n')


	def modification_mode(self):
		print("\nmodification mode !!!\n'--help to see usage\n")
		while True:
			mode = input("@modification/$ ")
			if mode == "--help":
				prt = """\nquit to exit from modification mode\n"mod name" to modify product name\n """
				print(prt)
			if mode == "mod name":
				name_old = input("enter old product name : ").strip()
				name_new = input("enter new product name : ").strip()
			if mode == "quit":
				break



	def unite_conv(self,quantity):
		try:
			amount = float(search(r'\d*[.]*\d*',quantity).group(0))
		except:
			amount = 0.0
		try:
			unite = search(r'[a-zA-Z]+',quantity).group(0)
		except:
			unite = ""
		if unite == "gram" or unite == "g":
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


#function call
if __name__ == '__main__':
	shop = shopping()
