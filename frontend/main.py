import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import api_client
from kivy.uix.popup import Popup    # fenetre flottant
from kivy.uix.spinner import Spinner #  list deroulant

class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.affichage = Label(text="", size_hint_y=None, halign="left", valign="top")
        self.affichage.bind(texture_size=self.affichage.setter("size"))
        scroll = ScrollView()
        scroll.add_widget(self.affichage)

        self.saisie = TextInput(multiline=False, size_hint_y=None, height=40)
        self.saisie.bind(on_text_validate=self.envoyer)

        self.modele_actuel = None
        self.liste_modeles = Spinner(text="Chargement...", values=["Chargement..."], size_hint_x=0.5)
        self.liste_modeles.bind(text=self.on_modele_choisi)

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
        # Charger les modèles au démarrage
        Clock.schedule_once(lambda dt: self.debut())
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
            texte = "Cle API enregistree."
            # Recharger les modèles maintenant que la clé est configurée
            threading.Thread(target=self.charger_modeles, daemon=True).start()
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(texte))

    def debut(self):
        threading.Thread(target=self.charger_modeles, daemon=True).start()

    def charger_modeles(self):
        try:
            data = api_client.lister_modeles()
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: self.ajouter(f"[erreur modeles] {err}"))
            return
        Clock.schedule_once(lambda dt, d=data: self.maj_modeles(d["modeles"], d["actuel"]))

    def maj_modeles(self, liste, actuel):
        self.liste_modeles.values = liste
        choix = actuel if actuel in liste else (liste[0] if liste else "Aucun modele")
        self.modele_actuel = choix
        self.liste_modeles.text = choix

    def on_modele_choisi(self, spinner, nom):
        if nom == self.modele_actuel or nom not in spinner.values:
            return
        self.modele_actuel = nom
        threading.Thread(target=self.appliquer_modele, args=(nom,), daemon=True).start()

    def appliquer_modele(self, nom):
        try:
            api_client.choisir_modele(nom)
            texte = f"Modele choisi : {nom}"
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.ajouter(texte))

if __name__ == "__main__":
    ChatApp().run()
