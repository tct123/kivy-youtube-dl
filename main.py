import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty

from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

from kivymd.bottomsheet import MDListBottomSheet
from kivymd.button import MDRaisedButton
from kivymd.button import MDFloatingActionButton
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.list import ILeftBodyTouch
from kivymd.selectioncontrols import MDCheckbox
from kivymd.theming import ThemeManager

import thread
import time
from pytube import YouTube

# https://www.youtube.com/watch?v=TnCY6Apxibk
class IconLeftSampleWidget(ILeftBodyTouch, MDCheckbox):
    pass

class MyBoxLayout(BoxLayout):
	
	def __init__(self, **kwargs):
        	super(MyBoxLayout, self).__init__(**kwargs)

	def goButtonClicked(self, url):
		self.ids.spinner.active = True
		thread.start_new_thread( self.fetchVideo, (url,))
		

	def fetchVideo(self, url):
		box_vertical = self.ids.b1
		self.yt = YouTube(url)
		self.yt.register_on_complete_callback(self.downloadComplete)
		
		v_strms = self.yt.streams.filter(progressive=True).all()
		a_strms = self.yt.streams.filter(only_audio=True).all()
		self.selected = self.yt.streams.first()
				
		self.streams = v_strms + a_strms
		
		for index,eachStream in enumerate(self.streams):
		    box_horizontal = BoxLayout(orientation='horizontal', size_hint=(1,.4))
		    checkbox = MDCheckbox(id=str(index), group='test', size_hint=(.2,1))
		    checkbox.bind(active=self.cb_clicked)
		    video_details = 'Format: ' + str(eachStream.mime_type) + ', Resolution: ' + str(eachStream.resolution)
		    label = MDLabel(text=video_details, size_hint=(.8,1))
		    box_horizontal.add_widget(checkbox)
		    box_horizontal.add_widget(label)
		    box_vertical.add_widget(box_horizontal)
			
		
		self.ids.spinner.active = False

	def print_test(self, inst):
		print 'hello ', inst.text
	
	def cb_clicked(self, checkbox, value):
		print checkbox.id
		self.selected = self.streams[int(checkbox.id)]
	
	def downloadVideo(self, selectedVideo):
		print 'downloading..'		
		selectedVideo.download()

	def downloadButtonClicked(self):
		self.ids.spinner.active = True
        	thread.start_new_thread(self.downloadVideo, (self.selected,))
		#self.showDialog()

	def downloadComplete(self, stream, file_handle):
		self.ids.spinner.active = False
        	print('Download Complete')
		self.showDialog()


	def showDialog(self):
		content = MDLabel(font_style='Body1',
		                  theme_text_color='Secondary',
		                  text="Find your downloaded video inside /sdcard/kivy/nimmitube",
		                  size_hint_y=None,
		                  valign='top')
		content.bind(texture_size=content.setter('size'))
		self.dialog = MDDialog(title="Download Complete!",
		                       content=content,
		                       size_hint=(.8, None),
		                       height=180,
		                       auto_dismiss=False)

		self.dialog.add_action_button("DONE",
		                              action=lambda *x: self.dialog.dismiss())
		self.dialog.open()

	def pasteURL(self):
		print 'pasting..'
		self.ids.inputUrl.text = Clipboard.paste()

class MyApp(App):
	theme_cls = ThemeManager()
	def build(self):
		return MyBoxLayout()

MyApp().run()
