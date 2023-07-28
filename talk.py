import fakeyou
from pygame import mixer
import requests

fake_you = fakeyou.FakeYou()
import io
class Talk:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __login_to_fakeyou(self):
        fake_you.login(self.username, self.password)
        print("loggin")

    def __generate_audio(self, text):
        print("busd")
        i=fake_you.say(text=text, ttsModelToken="TM:5ggf3m5w2mhq")
        return i

    def talk(self, text):
        self.__login_to_fakeyou()
        filename = self.__generate_audio(text)
        play_audio_from_url(filename.link)


def play_audio_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        mixer.init()
        mixer.music.load(io.BytesIO(response.content))
        mixer.music.play()
        while mixer.music.get_busy():
            continue
'''
username = "DaniBe91"
password = "VivaGerryfake"
tts = Talk(username, password)
text_to_speak = "Ciao, sono "
tts.talk(text_to_speak)'''