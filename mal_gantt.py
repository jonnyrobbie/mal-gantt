#!/usr/bin/env python3
## Read this code at your own risk. Reckless assertion of your
## first freedom may result in permanent brain damage. I might have
## broken everything from PEP 8 as well as summon a devil.

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import xml.etree.ElementTree as ET
import time
import datetime
import pandas as pd
import logging
import argparse

vcount = {2: logging.DEBUG,
		  1: logging.INFO,
		  None: logging.WARNING}

#Argument parser
parser = argparse.ArgumentParser(description='Render Gantt charts from exported MyAnimeList data...')
parser.add_argument("-v", "--verbose", help="Verbose output.", action="count")
parser.add_argument("--bgcolour", help="Background colour.", default="#D7D6A5")
parser.add_argument("--barcolour", help="Finished bar colour.", default="#458985")
parser.add_argument("--dbarcolour", help="Dropped bar colour.", default="#DBA67B")
parser.add_argument("--wbarcolour", help="Watching bar colour.", default="#7AC97B")
parser.add_argument("--hbarcolour", help="On-Hold bar colour.", default="#8A8054")
parser.add_argument("--textcolour", help="Text colour.", default="#074358")
parser.add_argument("--glowcolour", help="Glow colour.", default="#80FFF8")
parser.add_argument("--glow", help="Enable text glow.", action="store_true")
parser.add_argument("--mincolour", help="Minor (month) grid  colour.", default="#C4C397")
parser.add_argument("--majcolour", help="Major (year) grid colour.", default="#ABAA83")
parser.add_argument("--lgridcolour", help="Grid label colour.", default="#5C5B46")
parser.add_argument("-o", "--open", help="XML file downloaded and unpacked from MyAnimeList - https://myanimelist.net/panel.php?go=export", required=True)
parser.add_argument("-s", "--save", help="The final PNG file save location", default="mal_gantt_export.png")
parser.add_argument("-p", "--point", help="Font pointsize.", default=11)
parser.add_argument("-f", "--fontfile", help="TTF or OTF font filename.")

args = parser.parse_args()

logging.basicConfig(level=vcount[args.verbose])

class GanttChart():
	def __init__(self, width, height, bgColor, glowColor):
		self.imageWidth = width + 200
		self.imageHeight = height
		self.glowColor = glowColor
		self.bgColor = bgColor
		self.outline = True
		self.glow = True
		self.timeMin = "0000-00-00"
		self.textHeight = 11
		self.ganttChart = Image.new("RGBA", (self.imageWidth, self.imageHeight + 3*self.textHeight), self.bgColor + "ff")
		self.ganttBlur = Image.new("RGBA", (self.imageWidth, self.imageHeight + 3*self.textHeight), self.glowColor + "00")
		self.ganttText = Image.new("RGBA", (self.imageWidth, self.imageHeight + 3*self.textHeight), "#00000000")
	def addItem(self, top, left, width, text, barColor, textColor):
		self.itemBar = ImageDraw.Draw(self.ganttChart)
		self.barColor = barColor
		self.textColor = textColor
		if self.outline:
			self.outlineColor = self.textColor
		else:
			self.outlineColor = self.barColor
		self.itemBar.rectangle([left, top, left+width, top+self.textheight], fill=self.barColor, outline=self.outlineColor)
		
		self.itemBlur = ImageDraw.Draw(self.ganttBlur)
		self.itemBlur.text((left+1, top), text, font=self.font, fill=self.glowColor + "ff")
		
		self.itemText = ImageDraw.Draw(self.ganttText)
		self.itemText.text((left+1, top), text, font=self.font, fill=textColor)
		
		logging.debug("Drawing bar for %s", text)
	
	def drawGrid(self, majColor, minColor, textColor):
		self.currentTuple = list(datetime.datetime.strptime(self.timeMin, "%Y-%m-%d").timetuple())
		self.minTuple = list(self.currentTuple)
		self.currentTime = list(time.gmtime())
		if self.currentTuple[2] != 1:
			self.currentTuple[2] = 1
			#modTupByIndex(self.currentTuple, 2, 1)
			if self.currentTuple[1] != 12:
				self.currentTuple[1] = self.currentTuple[1] + 1
				#modTupByIndex(self.currentTuple, 1, self.currentTuple[1] + 1)
			else:
				self.currentTuple[1] = 1
				self.currentTuple[0] = self.currentTuple[0] + 1
				#modTupByIndex(self.currentTuple, 1, 1)
				#modTupByIndex(self.currentTuple, 0, self.currentTuple[0] + 1)
		logging.info("Current date: %s", self.currentTuple)
		logging.info("Date of beginning: %s", self.currentTime)
		while time.mktime(tuple(self.currentTuple)) < time.mktime(tuple(self.currentTime)):
			#print("Pixel:", timeConv()/(3600*24))
			#print(round((time.mktime(time.struct_time(self.currentTuple))/(3600*24))), round((time.mktime(time.struct_time(self.minTuple))/(3600*24))))
			self.pixel = round((time.mktime(time.struct_time(self.currentTuple))/(3600*24)))-round((time.mktime(time.struct_time(self.minTuple))/(3600*24)))
			self.gridLineDraw = ImageDraw.Draw(self.ganttChart)
			if self.currentTuple[1] == 1:
				#print("Major gridline")
				self.gridLineDraw.line([self.pixel, 0, self.pixel, self.imageHeight], fill=majColor, width = 1)
				self.gridLineDraw.text((self.pixel-10, self.imageHeight + self.textHeight), str(self.currentTuple[0]), font=self.font, fill=textColor)
			else:
				#print("Minor gridline")
				self.gridLineDraw.line([self.pixel, 0, self.pixel, self.imageHeight], fill=minColor, width = 1)
			if self.currentTuple[1] != 12:
				self.currentTuple[1] = self.currentTuple[1] + 1
				#modTupByIndex(self.currentTuple, 1, self.currentTuple[1] + 1)
				#print("modding")
			else:
				self.currentTuple[1] = 1
				self.currentTuple[0] = self.currentTuple[0] + 1
				#modTupByIndex(self.currentTuple, 1, 1)
				#modTupByIndex(self.currentTuple, 0, self.currentTuple[0] + 1)
		
	
	def setTextFont(self, font, height):
		self.textheight = height
		self.font = ImageFont.truetype(font, height)
	
	def blur(self):
		self.ganttBlur = self.ganttBlur.filter(ImageFilter.GaussianBlur(radius=2))
		
	def composite(self):
		if self.glow: self.ganttChart = Image.alpha_composite(self.ganttChart, self.ganttBlur)
		self.ganttChart = Image.alpha_composite(self.ganttChart, self.ganttText)
	
	def save(self, filename):
		self.ganttChart.save(filename)
		
	def show(self, filename):
		self.ganttChart.save("ABar_" + filename)
		self.ganttBlur.save("ABlur_" + filename)
		self.ganttText.save("AText_" + filename)
		
	def getChart(self):
		return(self.ganttChart)

class timeConv():
	def __init__(self, date):
		self.date = date
	def getUnixtime(self):
		try:
			return(time.mktime(datetime.datetime.strptime(self.date, "%Y-%m-%d").timetuple()))
		except ValueError:
			return(time.mktime(time.gmtime()))

class ParseXML():
	def __init__(self, path):
		self.xmlPath = path
		self.timeMin = "9999-99-99"
		self.currentTime = datetime.datetime.now().strftime("%Y-%m-%d")
	
	def parse(self):
		self.animeXML = ET.parse(self.xmlPath)
		self.animeRoot = self.animeXML.getroot()
		self.animeList = []
		for anime in self.animeRoot.iter(tag="anime"):
			self.animeItem = {"name": anime.find("series_title").text,
					"date_start": anime.find("my_start_date").text,
					"date_finish": anime.find("my_finish_date").text,
					"eps": anime.find("my_watched_episodes").text,
					"status": anime.find("my_status").text,
					"un_start": False,
					"un_finish": False}
			self.animeList.append(self.animeItem)
		self.animeList[:] = [anime for anime in self.animeList if (anime["status"]=="Completed" or anime["status"]=="Watching" or anime["status"]=="Dropped" or anime["status"]=="On-Hold")]

		for anime in self.animeList:
			if anime["date_finish"][0:4] == "0000":
				anime["date_finish"] = self.currentTime
				anime["un_finish"] = True
			if anime["date_start"][0:4] == "0000":
				anime["un_start"] = True
				anime["date_start"] = self.currentTime
			if anime["date_start"][8:10] == "00":
				anime["date_start"] = anime["date_start"][0:8] + "01"
			if anime["date_start"][5:7] == "00":
				anime["date_start"] = anime["date_start"][0:5] + "01" + anime["date_start"][7:10]
			if anime["date_finish"][8:10] == "00":
				anime["date_finish"] = anime["date_finish"][0:8] + "01"
			if anime["date_finish"][5:7] == "00":
				anime["date_finish"] = anime["date_finish"][0:5] + "01" + anime["date_finish"][7:10]
			if anime["date_start"] < self.timeMin:
				self.timeMin = anime["date_start"]
			anime["length"] = timeConv(anime["date_finish"]).getUnixtime()-timeConv(anime["date_start"]).getUnixtime()
		logging.debug("Anime list: %s", self.animeList)
		for anime in self.animeList:
			if anime["un_start"] == True:
				anime["date_start"] = self.timeMin
			if anime["un_finish"] == True and anime["status"] != "Watching" and anime["status"] != "On-Hold":
				anime["date_finish"] = self.timeMin
		self.animeDF = pd.DataFrame(self.animeList)
		self.animeDF = self.animeDF.sort_values(by=["date_start", "date_finish", "name"])
		self.animeDF["indx"] = pd.Series(range(0,(self.animeDF.shape[0])), index=self.animeDF.index)

class DrawChart():
	def __init__(self, height, path, fontpath):
		self.height = height
		self.path = path
		self.fontpath = fontpath
	def draw(self):
		self.animeParse = ParseXML(self.path)
		self.animeParse.parse()
		logging.info("XML file parsed.")
		self.null_date = "0000-00-00"

		self.chartHeight = self.height*self.animeParse.animeDF.shape[0]
		self.chartWidth = round((time.mktime(time.gmtime()) - timeConv(self.animeParse.timeMin).getUnixtime())/(3600*24))
		#https://color.adobe.com/Vintage-1-color-theme-10367531/edit/?copy=true&base=2&rule=Custom&selected=3&name=Copy%20of%20Vintage%201&mode=rgb&rgbvalues=0.027450980392156862,0.2627450980392157,0.34509803921568627,0.27058823529411763,0.5372549019607843,0.5215686274509804,0.8431372549019608,0.8392156862745098,0.6470588235294118,0.8588235294117647,0.6509803921568628,0.4823529411764706,0.6470588235294118,0.3607843137254902,0.3333333333333333&swatchOrder=0,1,2,3,4
		logging.info("Image Width: %s, image height: %s", self.chartWidth, self.chartHeight)
		self.chart = GanttChart(self.chartWidth, self.chartHeight, bgColor=args.bgcolour, glowColor = args.glowcolour)
		self.chart.setTextFont(self.fontpath, self.height)
		self.chart.outline = False
		self.chart.glow = args.glow
		self.chart.textHeight = self.height
		self.chart.timeMin = self.animeParse.timeMin
		logging.info("Chart initialized.")
		self.chart.drawGrid(majColor=args.majcolour, minColor=args.mincolour, textColor=args.lgridcolour)
		logging.info("Grid drawn.")
		for index, anime in self.animeParse.animeDF.iterrows():
			if anime["status"] == "Dropped":
				self.colorBar = args.dbarcolour
			elif anime["status"] == "Watching":
				self.colorBar = args.wbarcolour
			elif anime["status"] == "On-Hold":
				self.colorBar = args.hbarcolour
			else:
				self.colorBar = args.barcolour
			self.chart.addItem(anime["indx"]*self.height, round((timeConv(anime["date_start"]).getUnixtime() - timeConv(self.animeParse.timeMin).getUnixtime())/(3600*24)), round((timeConv(anime["date_finish"]).getUnixtime() - timeConv(anime["date_start"]).getUnixtime())/(3600*24)), text=anime["name"], barColor=self.colorBar, textColor=args.textcolour)
		logging.info("Anime bars drawn.")
		#self.chart.getChart().save("anime_gantt.png")
		self.chart.blur()
		self.chart.composite()
		logging.info("Layers composited.")
		self.chart.save(args.save)
		logging.info("PNG exported.")
		
chart = DrawChart(height=int(args.point), path=args.open, fontpath=args.fontfile)
chart.draw()
