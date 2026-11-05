import threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import api_client

PROVIDERS = ["openai", "google", "nvidia"]

class ClePopup(Popup):
    def __init__(self, afficher, apres_succes, **kwargs):
        super().__init__(title="Clé API", size_hint=(0.9, 0.5), **kwargs)
        self.afficher = afficher            # ecrit dans le chat
        self.apres_succes = apres_succes    # appele si cle ok

        contenu = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Selecteur de provider
        provider_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        provider_box.add_widget(Label(text="Fournisseur:", size_hint_x=0.3))
        self.provider_spinner = Spinner(
            text="nvidia",
            values=PROVIDERS,
            size_hint_x=0.7,
        )
        provider_box.add_widget(self.provider_spinner)
        contenu.add_widget(provider_box)

        # Champ cle API
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
        provider = self.provider_spinner.text
        if not cle or not provider:
            return
        self.dismiss()                      # ferme le popup
        threading.Thread(target=self.appeler, args=(cle, provider), daemon=True).start()

    def appeler(self, cle, provider):
        try:
            api_client.enregistreCle(cle, provider)
            texte = f"Cle API enregistree pour {provider}."
            self.apres_succes()             # recharge les modeles
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.afficher(texte))    # retour thread principal

# Pour eviter import circulaire
from kivy.uix.label import Label