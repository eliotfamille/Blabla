import threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import api_client

class ClePopup(Popup):
    def __init__(self, afficher, apres_succes, **kwargs):
        super().__init__(title="Clé API", size_hint=(0.9, 0.4), **kwargs)
        self.afficher = afficher            # ecrit dans le chat
        self.apres_succes = apres_succes    # appele si cle ok

        contenu = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.champ = TextInput(
            hint_text="Colle cle API",
            password=True,                  # masque la saisie
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        bouton_ok = Button(text="Enregistrer", size_hint_y=None, height=50)
        bouton_ok.bind(on_press=self.enregistrer)
        contenu.add_widget(self.champ)
        contenu.add_widget(bouton_ok)
        self.content = contenu              # contenu du popup

    def enregistrer(self, *_):
        cle = self.champ.text.strip()
        if not cle:
            return
        self.dismiss()                      # ferme le popup
        threading.Thread(target=self.appeler, args=(cle,), daemon=True).start()

    def appeler(self, cle):
        try:
            api_client.enregistreCle(cle)
            texte = "Cle API enregistree."
            self.apres_succes()             # recharge les modeles
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.afficher(texte))    # retour thread principal
