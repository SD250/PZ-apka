import kivy
import kivymd

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivymd.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu

import requests

# Window.size = (1080/3,1920/3)       # na telefonie zakomnertowac albo usunac

class ContentForPanel(MDFloatLayout):
    panel_name = StringProperty('')

class CustomDialogContent(FloatLayout):
    pass

class SettingsScreen(Screen):
    pass

class AddNewSensorContent(MDFloatLayout):
    pass        


class MainScreen(Screen):
    def add_list_item(self):
        panel_name = f"Czujnik #{len(self.list_view.children) + 1}"
        content = ContentForPanel()
        content.panel_name = panel_name  

        panel = MDExpansionPanel(
            icon=f"numeric-{len(self.list_view.children) + 1}-box-outline",
            content=content,
            panel_cls=MDExpansionPanelTwoLine(
                text=panel_name,
                theme_text_color= 'Custom',
                text_color= (58/255,83/255,155/255,1),
                divider=None,
                secondary_text="Połączony",
                bg_color = (197/255,239/255,247/255,1),
                radius=(10,10,0,0),
                size_hint_x = 1,
            )
        )
        self.list_view.add_widget(panel)

class MainApp(MDApp):
    add_sensor_dialog = None
    settings_dialog = None

    water_cm = StringProperty('0')
    water_cm_progress = NumericProperty(round(0))
    water_cm_progress_info = StringProperty('0 %')
    

    def update(self, *args):
        water_container_full = 17.34
        url = "https://fra1.blynk.cloud/external/api/get?token=wtFC-kSgVfDkyrtjds1zyb8tlR5nAdOy&V2"
        response = requests.get(url)
        distance_cm = round(int(response.text) / 58,2)
        self.water_cm = f"{distance_cm} cm"
        self.water_cm_progress = round((water_container_full-distance_cm)*100/water_container_full) if distance_cm<water_container_full else 0 
        self.water_cm_progress_info = f"{self.water_cm_progress} %"

    # def menu_open(self):
    #     menu_items = [
    #         {
    #             "text": f"Item {i}",
    #             "on_release": lambda x=f"Item {i}": self.menu_callback(x),
    #         } for i in range(5)
    #     ]
    #     MDDropdownMenu(
    #         caller=self.root.ids.button, items=menu_items
    #     ).open()

    def on_start(self):
        Clock.schedule_interval(self.update, 2)
    
    def close_sensor_settings_dialog(self, *args):
        if self.settings_dialog:
            self.settings_dialog.dismiss()

    def save_sensor_settings(self, *args):
        if self.settings_dialog:
            self.settings_dialog.dismiss()

    def show_sensor_settings_dialog(self, panel_name):
        if not self.settings_dialog:
            self.settings_dialog = MDDialog(
                title=panel_name,
                md_bg_color = (197/255,239/255,247/255,1),
                type="custom",
                content_cls=CustomDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="ANULUJ",
                        on_release=self.close_sensor_settings_dialog,
                        theme_text_color= 'Custom',
                        text_color= (58/255,83/255,155/255,1),
                    ),
                    MDFlatButton(
                        text="ZAPISZ",
                        on_release=self.save_sensor_settings,
                        theme_text_color= 'Custom',
                        text_color= (58/255,83/255,155/255,1),
                    ),
                ],
            )
        self.settings_dialog.open()

    def close_add_new_sensor_dialog(self, *args):
        if self.add_sensor_dialog:
            self.add_sensor_dialog.dismiss()

    def add_new_sensor(self, *args):
        if self.add_sensor_dialog:
            self.add_sensor_dialog.dismiss()
            self.close_add_new_sensor_dialog()
            main_screen = self.root.get_screen('mainscreen')
            main_screen.add_list_item()

    def show_add_new_sensor_dialog(self):
        if not self.add_sensor_dialog:
            self.add_sensor_dialog = MDDialog(
                title='Dodaj nowy Czujnik',
                md_bg_color = (197/255,239/255,247/255,1),
                type="custom",
                content_cls=AddNewSensorContent(),
                buttons=[
                    MDFlatButton(
                        text="ANULUJ",
                        on_release=self.close_add_new_sensor_dialog,
                        theme_text_color= 'Custom',
                        text_color= (58/255,83/255,155/255,1),
                    ),
                    MDFlatButton(
                        text="DODAJ",
                        on_release=self.add_new_sensor,
                        theme_text_color= 'Custom',
                        text_color= (58/255,83/255,155/255,1),
                    ),
                ],
            )
        self.add_sensor_dialog.open()

    def build(self):
        self.theme_cls.theme_style = 'Light'
        Builder.load_file('ui.kv')
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(MainScreen(name='mainscreen'))
        self.screen_manager.add_widget(SettingsScreen(name='settingsscreen'))
        return self.screen_manager

MainApp().run()