import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import api_client
from kivy.uix.popup import Popup

class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.affichage = Label(text="", size_hint_y=None, halign="left", valign="top")
        self.affichage.bind(texture_size=self.affichage.setter("size"))
        scroll = ScrollView()
        scroll.add_widget(self.affichage)

        self.saisie = TextInput(multiline=False, size_hint_y=None, height=40)
        self.saisie.bind(on_text_validate=self.envoyer)

        barre = BoxLayout(size_hint_y=None, height=50, spacing=10)
        bouton_cle = Button(text="Clé API")
        bouton_cle.bind(on_press=self.ouvrir_cle)
        bouton_envoyer = Button(text="Envoyer")
        bouton_envoyer.bind(on_press=self.envoyer)
        barre.add_widget(bouton_cle)
        barre.add_widget(bouton_envoyer)

        root.add_widget(scroll)
        root.add_widget(self.saisie)
        root.add_widget(barre)
        return root

    def envoyer(self, *_):
        message = self.saisie.text.strip()
        if not message:
            return
        self.saisie.text = ""
        self.ajouter(f"Vous : {message}")
        threading.Thread(target=self.appeler, args=(message,), daemon=True).start() # renvoi la reponse dans un fil asyncro

    def appeler(self, message):
        try:
            reponse = api_client.envoyer(message)
        except Exception as e:
            reponse = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(f"IA : {reponse}")) # renvoir chaque reponse du fil

    def ajouter(self, texte):
        self.affichage.text += texte + "\n\n"   # affiche le texte

    def enregistrer_cle(self, *_):
        cle = self.champ_cle.text.strip()
        if not cle:
            return
        self.popup.dismiss()
        threading.Thread(target=self.appeler_cle, args=(cle,), daemon=True).start()

    def ouvrir_cle(self, *_):
        contenu = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.champ_cle = TextInput(
            hint_text="Colle ta clé API",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        bouton_ok = Button(text="Enregistrer", size_hint_y=None, height=50)
        bouton_ok.bind(on_press=self.enregistrer_cle)
        contenu.add_widget(self.champ_cle)
        contenu.add_widget(bouton_ok)

        self.popup = Popup(title="Clé API", content=contenu, size_hint=(0.9, 0.4))
        self.popup.open()

    def appeler_cle(self, cle):
        try:
            api_client.enregistreCle(cle)
            texte = "Clé API enregistrée."
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(texte))

if __name__ == "__main__":
    ChatApp().run()
