
try:
	from kivy.app import App

	from kivy.uix.label import Label
	from kivy.uix.gridlayout import GridLayout
	from kivy.uix.textinput import TextInput
	from kivy.uix.button import Button
	from kivy.uix.scrollview import ScrollView
	from kivy.core.window import Window
	from kivy.uix.popup import Popup
	from kivy.logger import Logger
	from kivy.clock import Clock

except Exception as e:
	Logger.info('HoloWatch: Failed to import a kivy libary Error ' + str(e))



try:
	import json
	import requests
	import traceback
except Exception as e:
	Logger.info('HoloWatch: Failed to import a main libary Error ' + str(e))

MOB_BUTTON_SIZE = 300
SERVER_URL = "http://10.0.0.51:8000/"
SERVER_PATH = "update.json"
UPDATE_TIME = 600

class StatusData():

	def __init__(self,url=None,path=None,name=None):
		self.url = url
		self.path = path
		self.name = name

	def getData(self):
		r = requests.get(self.url + self.path)
		self.data = r.json()

class Streamer():

	def __init__(self,name="",isLive=False,link=None,thumbnail=None):
		self.name = name
		self.isLive = isLive
		self.link = link
		self.thumbnail = thumbnail

	def addSelf(self,container):

		container.add_widget(Label(text=self.name))
		
		self.liveButton = Button(text=str(self.isLive),font_size=24,size_hint_y=None,height=MOB_BUTTON_SIZE)

		self.liveButton.bind(on_press=self.openStream)

		container.add_widget(self.liveButton)

	def updateStatus(self,status=None):
		if status == None:
			self.liveButton.text = str(self.isLive)
		else:
			self.liveButton.text = str(status)

		Logger.info("HoloWatch: Updated status to " + str(status))

	def openStream(self,instance):
		if self.isLive:
			print("Opening stream" + self.link)
			#webbrowser.open(self.link)
		else:
			print("Not live")

class HoloWatch(App):

	def build(self):
		
		Logger.info('HoloWatch: Starting main app')

		Clock.schedule_interval(self.updateStatus, UPDATE_TIME)

		self.streamers = []

		layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
		# Make sure the height is such that there is something to scroll.
		layout.bind(minimum_height=layout.setter('height'))

		Status = StatusData(SERVER_URL,SERVER_PATH)

		Status.getData()

		data = Status.data

		for streamer in data:
			self.streamers.append(Streamer(name=str(streamer['name']),isLive=streamer['status'],link=streamer['link'],thumbnail=streamer['thumbnail']))
			
		for streamer in self.streamers:
			streamer.addSelf(layout)

		root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		root.add_widget(layout)

		return root

	def updateStatus(self,dt):

		Logger.info("HoloWatch: Updating Status")

		Status = StatusData(SERVER_URL,SERVER_PATH)

		Status.getData()

		data = Status.data

		for i in range(len(data)):
			self.streamers[i].isLive = data[i]['status']
			self.streamers[i].updateStatus()

if __name__ == "__main__":
	try:
		HoloWatch().run()
	except Exception as e:

		Logger.error('HoloWatch: Big Error ' + traceback.format_exc() + " " + str(e))