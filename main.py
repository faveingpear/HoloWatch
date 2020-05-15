import json
import requests
import webbrowser

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

MOB_BUTTON_SIZE = 300
STATUS_DATA_PATH = "test.json"

TEST_JSON = """[
    {
        "name": "Matsuri",
        "status":true,
        "link":"https://www.youtube.com/watch?v=A9iBkUW_w_A",
        "thumbnail":"https://www.youtube.com/watch?v=A9iBkUW_w_A"
    },
    {
        "name": "Matsuri",
        "status":false,
        "link":null,
        "thumbnail":null
    }
]"""

class StatusData():

	def __init__(self,url=None,path=None,name=None):
		self.url = url
		self.path = path
		self.name = name

	def getData(self):
		if self.url == None:
			
			file = open(self.path,"r")

			self.data = json.load(file)

			file.close

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

	def openStream(self,instance):
		if self.isLive:
			print("Opening stream" + self.link)
			webbrowser.open(self.link)
		else:
			print("Not live")

class HoloWatch(App):

	def build(self):

		self.streamers = []

		layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
		# Make sure the height is such that there is something to scroll.
		layout.bind(minimum_height=layout.setter('height'))

		data = json.loads(TEST_JSON)

		for streamer in data:
			self.streamers.append(Streamer(name=str(streamer['name']),isLive=streamer['status'],link=streamer['link'],thumbnail=streamer['thumbnail']))
			
		for streamer in self.streamers:
			streamer.addSelf(layout)

		root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		root.add_widget(layout)

		return root

if __name__ == "__main__":
	HoloWatch().run()