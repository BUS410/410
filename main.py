from os import listdir
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.rst import RstDocument
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
import game


DESCRIPTION = '''
ОПИСАНИЕ
########

Привет, Спасибо за скачивание!)

410 - это игра-платформер без сюжета. Для прохождения каждого из уровней игры, 
нужно дойти от точки А в точку Б, если она конечно имеется. Для этой игры вы можете написать свой собственный уровень, инструкция находиться в папке с 
игрой **"инструкция по созданию уровня.txt"**. Также можно поместить в папку **music** 
свою музыку, которую можно будет вклюичть на любом из уровней.

В меню игры, установите нужные вам разрешение и выберите музыку и уровень.

Управление:

.. table::
	
	+--------------+--------+
	| D            | влево  |
	+--------------+--------+
	| A            | вправо |
	+--------------+--------+
	| SPACE(пробел)| прыжок |
	+--------------+--------+
	| ESC          | выйти  |
	+--------------+--------+

Приятной игры!)'''


Builder.load_string('''

<MenuLabel>:
	font_size: '36dp'
	background_color: 0, .5, 1, 1
	canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos

<Selector>:
	font_size: '36dp'
	font_color: 1, 1, 1, 1
	background_normal: ''
	background_color: 0, .6, 1, 1

<StartButton>:
	font_size: '36dp'
	background_normal: ''
	background_color: 0, .6, 1, 1
	text: 'Запустить'

<FullscreenButton>:
	font_size: '36dp'
	background_normal: ''
	background_color: 0, .6, 1, 1
	text: 'Выключено'

''')

class MenuLabel(Label):
	pass

class StartButton(Button):
	pass

class FullscreenButton(ToggleButton):
	pass

class Selector(Spinner):
	def get_levels(self):
		levels = listdir('levels/')
		self.values = levels
		if levels:
			self.text = levels[0]

	def get_music(self):
		music = listdir('music/')
		self.values = music
		if music:
			self.text = music[0]

class MenuApp(App):
	def start_game(self, instance):
		game.main({
			'level': 'levels/' + self.level.text,
			'music': 'music/' + self.music.text,
			'resolution': [int(x) for x in self.resolution.text.split('x')],
			'fullscreen': True if self.fullscreen.state == 'down' else False,
			})

	def _change(self, instance):
		instance.text = 'Включено' if instance.state == 'down' else 'Выключено'

	def build(self):
		menu = GridLayout(cols = 2)

		menu.add_widget(MenuLabel(text='Разрешение'))
		self.resolution = Selector(text='1280x720', values=['1920x1080', '1366x768', '1280x720', '800x480'])
		menu.add_widget(self.resolution)

		menu.add_widget(MenuLabel(text='Полный экран'))
		self.fullscreen = FullscreenButton(on_release = self._change)
		menu.add_widget(self.fullscreen)
		
		menu.add_widget(MenuLabel(text='Уровень'))
		self.level = Selector()
		self.level.text = 'Уровни не найдены'
		self.level.get_levels()
		menu.add_widget(self.level)
		
		menu.add_widget(MenuLabel(text='Музыка'))
		self.music = Selector()
		self.music.text = 'Музыка не найдена'
		self.music.get_music()
		menu.add_widget(self.music)

		menu.add_widget(MenuLabel(text='Начать игру'))
		menu.add_widget(StartButton(on_release=self.start_game,
				))


		description = RstDocument(text=DESCRIPTION)

		root = PageLayout()
		root.add_widget(menu)
		root.add_widget(description)
		
		return root

if __name__ == '__main__':
	MenuApp().run()