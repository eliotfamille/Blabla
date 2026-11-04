import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import api_client

class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.affichage = Label(text="", size_hint_y=None, halign="left", valign="top")
        self.affichage.bind(texture_size=self.affichage.setter("size"))
        scroll = ScrollView()
        scroll.add_widget(self.affichage)

        self.saisie = TextInput(multiline=False, size_hint_y=None, height=40)
        self.saisie.bind(on_text_validate=self.envoyer)

        bouton = Button(text="Envoyer", size_hint_y=None, height=50)
        bouton.bind(on_press=self.envoyer)

        root.add_widget(scroll)
        root.add_widget(self.saisie)
        root.add_widget(bouton)
        return root

    def envoyer(self, *_):
        message = self.saisie.text.strip()
        if not message:
            return
        self.saisie.text = ""
        self.ajouter(f"Vous : {message}")
        threading.Thread(target=self.appeler, args=(message,), daemon=True).start()

    def appeler(self, message):
        try:
            reponse = api_client.envoyer(message)
        except Exception as e:
            reponse = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(f"IA : {reponse}"))

    def ajouter(self, texte):
        self.affichage.text += texte + "\n\n"

if __name__ == "__main__":
    ChatApp().run()
