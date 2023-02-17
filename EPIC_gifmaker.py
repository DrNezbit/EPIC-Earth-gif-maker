import asyncio,json,os
from urllib import request
from datetime import datetime,timedelta


import imageio
import imageio.v3 as iio


#TO RESIZE IMAGE UNCOMMENT BELOW AND LINE 75
##################################################
#from PIL import Image
#size=800 #RESOLUTION IN PIXELS : CHANGE SIZE HERE
##################################################
async def run():
##################################################
	rez=input("Choose quality: \n 1)  low (fast) \n 2)  medium \n 3)  high (slow)\nEnter choice: ")
	try: rez=int(rez)
	except(ValueError): rez=None
	if rez==1: rez="low"
	elif rez==2: rez="medium"
	elif rez==3: rez="high"
	else: print("Invalid choice"); return
	epic=Epic(rez)
	await epic.make_gif()
##################################################
##################################################
class Epic:
##################################################
	def __init__(self,rez="low"):
		print("\nWorking...\n")
		self.date_offset=1
		self.data=self.set_data()
		self.rez=rez
		self.images=self.get_list()
		self.current=self.images[0]
		self.newest=self.current
##################################################
	def set_data(self):
		showing=datetime.utcnow()+timedelta(hours=-5,days=-self.date_offset)
		date_str=showing.strftime("%Y-%m-%d")
		url_date=f"/date/{date_str}"
		data=[]
		with request.urlopen(f"https://epic.gsfc.nasa.gov/api/natural{url_date}") as url:
			data = json.loads(url.read().decode())
			if len(data) <1:
				self.date_offset+=1 ; self.start_offset=self.date_offset
				data=self.set_data() ; self.data=data	
		return data
##################################################	
	def get_list(self):
		if self.rez=="high": ext="png"; folder=ext
		elif self.rez=="medium": ext="jpg" ; folder=ext
		else: self.rez="low" ; ext="jpg" ; folder="thumbs"
		images=[]
		for data in self.data:
			full_date=data["date"]
			date=full_date.split(" ")[0].replace("-","/")
			image=data["image"]
			url=f"https://epic.gsfc.nasa.gov/archive/natural/{date}/{folder}/{image}.{ext}"
			images.append((full_date,url))
		return images
##################################################
	async def make_gif(self):
		frames=[]
		date=self.images[0][0].split(" ")[0]
		end=self.images[-1][0].split(" ")[1] #END TIME
		start=self.images[0][0].split(" ")[1] #START TIME
		filename=f"earth {date} {start} - {end} - {self.rez} quality.gif"
		if not os.path.exists(f"./{filename}"):
			date=self.current[0].split(" ")[0]
			print(f"Building gif from {len(self.images)} {self.rez} quality images on {date}\n")	
			for url in self.images:
				frame = iio.imread(url[1]) #UNCOMMENT BELOW TO RESIZE
				#frame= Image.fromarray(frame).resize((size,size))
				frames.append(frame)
				frames.append(frame) #SLOWS GIF SOME
				frames.append(frame) #SLOWS GIF MORE
	#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
			imageio.mimsave(f"./{filename}", frames) # SAVES GIF
			print(f"Saved: \n{filename}")
		else: print(f"File already exists: \n{filename}")
##################################################
asyncio.run(run())
##################################################
