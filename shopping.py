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
				print("\ndeletion mode !!!!\n")
				name = input("enter product name : ").strip()
				self.delete(name,p=True)

			if mode == "modify":
				self.modification_mode()

			if mode=="--help":
				prt = """\n'new' to insert new data\n'show' to see today's data\n'quit' to exit\n'delete' to enter in deletion mode\n'modify' to enter modification mode\n"""
				print(prt)



	def delete(self,name,p=False):
		try:
			del self.contents[self.date][name]
			self.wrt_json()
			if p== True:
				print(f"product {name} deleted successfully !!!\n")
			return True
		except:
			print(f'sorry ! the product {name} is not exists\n')
			return False


	def modification_mode(self):
		print("\nmodification mode !!!\n'--help to see usage\n")
		while True:
			mode = input("@modification/$ ")
			if mode == "--help":
				prt = """\n'quit' to exit from modification mode\n"name" to modify product name\n"quantity" to modify quantity of a product\n"cost" to modify cost\n"mod" to modify the all at a time\n"""
				print(prt)
			if mode == "name":
				name_old = input("enter old product name : ").strip()
				name_new = input("enter new product name : ").strip()
				try:
					info = self.contents[self.date][name_old]
					info[2] = date_time.time()
					del self.contents[self.date][name_old]
					self.contents[self.date][name_new] = info
					self.wrt_json()
				except:
					print(f"ERROR:name {name_old} is not found !!!")
			if mode == "quantity":
				name = input("enter name of the product : ").strip()
				quantity = input("enter new quantity : ").strip()
				if quantity == "":
					print("ERROR: please put somthing in quantity :)")
				try:
					quantity = self.unite_conv(quantity)
					info = self.contents[self.date][name]
					try:
						unite = search(r'[a-zA-Z]+',info[0]).group(0)
					except:
						unite = ""
					info[0] = f"{quantity} {unite}"
					info[2] = date_time.time()
					self.contents[self.date][name] = info
					self.wrt_json()
				except:
					print(f"ERROR:name {name} is not found !!!")
			if mode == "cost":
				name = input("enter name of the product : ").strip()
				try:
					cost = int(input("enter modified cost : ").strip())
				except:
					cost = 0
				try:
					info = self.contents[self.date][name]
					info[1] = cost
					info[2] = date_time.time()
					self.contents[self.date][name] = info
					self.wrt_json()
				except:
					print(f"ERROR:name {name} is not found !!!")
			if mode == "mod":
				name_old = input("enter old name of product : ").strip()
				exist = self.delete(name_old)
				if exist == False:
					pass
				elif exist == True:
					name_new = input("enter new name : ").strip()
					quantity = input("enter new quantity : ").strip()
					quantity = self.unite_conv(quantity)
					try:
						cost = int(input("enter cost : "))
					except:
						cost = 0 
					self.contents[self.date][name_new] = [quantity,cost,date_time.time()]
					self.wrt_json()
			if mode == "quit":
				break



	def unite_conv(self,quantity):
		try:
			quant = float(search(r'\d*[.]*\d*',quantity).group(0))
		except:
			quant = 0.0
		try:
			unite = search(r'[a-zA-Z]+',quantity).group(0)
		except:
			unite = ""


		if unite == "gram" or unite == "g":
			quant /= 1000
			unite = 'kg'

		if unite == "packet" or unite == "packets":
			try:
				pie = input('how many pieces are there in one packet : ').strip()
				pie = int(float(pie))
				pie = int(quant*pie)
			except:
				pie = 1.0
			quant = pie
			unite = 'pieces'
		quantity = f"{quant} {unite}"
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
