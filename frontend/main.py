import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import api_client
from popup_cle import ClePopup
from liste_modeles import ListeModeles

class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.affichage = Label(text="", size_hint_y=None, halign="left", valign="top")
        self.affichage.bind(texture_size=self.affichage.setter("size"))     # taille = texte
        scroll = ScrollView()
        scroll.add_widget(self.affichage)

        self.saisie = TextInput(multiline=False, size_hint_y=None, height=40)
        self.saisie.bind(on_text_validate=self.envoyer)     # touche entree

        self.liste_modeles = ListeModeles(afficher=self.ajouter)    # callback chat

        bouton_cle = Button(text="Cle API")
        bouton_cle.bind(on_press=self.ouvrir_cle)
        bouton_envoyer = Button(text="Envoyer")
        bouton_envoyer.bind(on_press=self.envoyer)

        barre = BoxLayout(size_hint_y=None, height=50, spacing=10)
        barre.add_widget(self.liste_modeles)
        barre.add_widget(bouton_cle)
        barre.add_widget(bouton_envoyer)

        root.add_widget(scroll)
        root.add_widget(self.saisie)
        root.add_widget(barre)

        Clock.schedule_once(lambda dt: self.liste_modeles.charger())    # charge au demarrage
        return root

    def ouvrir_cle(self, *_):
        popup = ClePopup(afficher=self.ajouter, apres_succes=self.liste_modeles.charger)
        popup.open()                        # affiche le popup

    def envoyer(self, *_):
        message = self.saisie.text.strip()
        if not message:
            return
        self.saisie.text = ""
        self.ajouter(f"Vous : {message}")
        threading.Thread(target=self.appeler, args=(message,), daemon=True).start()     # fil separe

    def appeler(self, message):
        try:
            reponse = api_client.envoyer(message)
        except Exception as e:
            reponse = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(f"IA : {reponse}"))     # retour thread principal

    def ajouter(self, texte):
        self.affichage.text += texte + "\n\n"       # ajoute au chat

if __name__ == "__main__":
    ChatApp().run()
