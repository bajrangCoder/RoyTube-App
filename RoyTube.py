'''
Author : @Raunak Raj
'''

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from pytube import YouTube
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

KV = '''
ScreenManager:
    MainScreen:
    DownloadScreen:

<MainScreen>:
    name:'main_screen'
    MDToolbar:
        title: "RoyTube"
        elevation: 10
        pos_hint: {"top": 1}
    MDCard:
        size_hint: None, None
        size: 600, 300
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 25
        spacing: 25
        radius:[25]
        orientation: 'vertical'

        MDLabel:
            id: welcome_label
            text: "Search Video"
            font_size: 40
            halign: 'center'

        MDTextFieldRound:
            id: url
            hint_text: "Enter video url.."
            size_hint_x: None
            width: 400
            font_size: 20
            pos_hint: {"center_x": 0.5}

        MDFillRoundFlatButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            on_press: app.search_video()
    MDToolbar:
        title:"Developed By Raunak Raj"
        pos_hint:{"bottom":1}

<DownloadScreen>:
    name:'download_screen'
    MDBoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "RoyTube"
            pos_hint:{"top":1}
            elevation: 10
            left_action_items: [["arrow-left-bold-circle-outline", lambda x: app.goto_main()]]
        MDLabel:
            id: video_title
        MDLabel:
            id: video_views
        MDLabel:
            id: video_author
        MDLabel:
            id: publish_date
        MDLabel:
            id: video_length
        MDRaisedButton:
            text: "Download Video"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: app.show_confirmation_dialog()
        
<Content>
    id: download_dialog
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "400dp"

    MDGridLayout:
        cols:2
        rows:4
        MDLabel:
            text:"1080p ---"
            font_size:40
        MDFillRoundFlatButton:
            text:"Download"
            on_press: app.download("1080")
        MDLabel:
            text:"720p ---"
            font_size:40
        MDFillRoundFlatButton:
            text:"Download"
            on_press: app.download("720")
        MDLabel:
            text:"360p ---"
            font_size:40
        MDFillRoundFlatButton:
            text:"Download"
            on_press: app.download("360")
        MDLabel:
            text:"Audio ---"
            font_size:40
        MDFillRoundFlatButton:
            text:"Download"
            on_press: app.download("Audio")
    MDLabel:
        id: progress_txt
        halign:"center"
        text:"Download Compled at hahahha gahahah"
        pos_hint:{"y":.16}
    
    MDProgressBar:
        id: progress_bar
        value: 0
'''

class Content(BoxLayout):
    pass

class MainScreen(Screen):
    pass

class DownloadScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='main_screen'))
sm.add_widget(DownloadScreen(name='download_screen'))

class MainApp(MDApp):
    dialog = None
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.screen = Builder.load_string(KV)
        return self.screen
    
    def goto_main(self):
        self.screen.get_screen('download_screen').manager.current='main_screen'
    
    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Download:",
                type="custom",
                content_cls=Content(),
                
            )
        self.dialog.open()
        self.dialog.content_cls.ids.progress_txt.text = ""
        
    
    def download(self,type):
        self.dialog.content_cls.ids.progress_txt.text=""
        self.dialog.content_cls.ids.progress_bar.value = 0
        
        if type == "1080":
            self.video_obj.streams.get_by_itag(137).download('/storage/emulated/0/RoyTube/Downloads/')
        elif type == "720":
            self.video_obj.streams.get_by_itag(22).download('/storage/emulated/0/RoyTube/Downloads/')
        elif type == "360":
            self.video_obj.streams.get_by_itag(18).download('/storage/emulated/0/RoyTube/Downloads/')
        elif type == "Audio":
            self.video_obj.streams.get_by_itag(140).download('/storage/emulated/0/RoyTube/Downloads/')
        else:
            pass
    
    def on_complete(self,stream, filepath):
        self.dialog.content_cls.ids.progress_txt.text=f"Download Completed!\n {filepath}"
        self.dialog.content_cls.ids.progress_bar.value = 100
    
    def on_progress(self, stream, chunk, bytes_remaining):
        #self.download_dialog.ids.progress_bar.value = 70
        progress_string = 100 - round(bytes_remaining / stream.filesize * 100)
        self.dialog.content_cls.ids.progress_bar.value = progress_string
        self.dialog.content_cls.ids.progress_txt.text=f"Downloading.... {progress_string}%"
     
    def search_video(self):
        url = self.screen.get_screen('main_screen').ids.url.text
        self.video_obj = YouTube(url,on_complete_callback = self.on_complete, on_progress_callback = self.on_progress)
        self.screen.get_screen('download_screen').ids.video_title.text = self.video_obj.title
        self.screen.get_screen('download_screen').ids.video_views.text = f'{str(self.video_obj.views)} views'
        self.screen.get_screen('download_screen').ids.video_author.text = f'Author : {self.video_obj.author}'
        self.screen.get_screen('download_screen').ids.publish_date.text = str(self.video_obj.publish_date)
        self.screen.get_screen('download_screen').ids.video_length.text = str(f'{round(self.video_obj.length / 60,2)} minutes')
        #self.screen.get_screen('download_screen').ids.video_desc.text = self.video_obj.description
        self.screen.get_screen('main_screen').manager.current='download_screen'


if __name__ == '__main__':
    MainApp().run()

