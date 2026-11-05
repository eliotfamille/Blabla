import threading
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
import api_client

class ListeModeles(Spinner):
    def __init__(self, afficher, get_provider_callback, **kwargs):
        super().__init__(text="Chargement...", values=["Chargement..."], size_hint_x=0.5, **kwargs)
        self.afficher = afficher            # ecrit dans le chat
        self.get_provider_callback = get_provider_callback  # callback pour avoir le provider actif
        self.modele_actuel = None           # evite renvoi inutile
        self.bind(text=self.on_modele_choisi)   # declenche au changement

    def charger(self):
        threading.Thread(target=self.charger_modeles, daemon=True).start()  # fil separe

    def charger_modeles(self):
        try:
            provider = self.get_provider_callback()
            data = api_client.lister_modeles(provider)
        except Exception as e:
            Clock.schedule_once(lambda dt, err=e: self.afficher(f"[erreur modeles] {err}"))
            return
        Clock.schedule_once(lambda dt, d=data: self.maj_modeles(d["modeles"], d["actuel"]))

    def maj_modeles(self, liste, actuel):
        self.values = liste                 # remplit la liste
        choix = actuel if actuel in liste else (liste[0] if liste else "Aucun modele")
        self.modele_actuel = choix
        self.text = choix                   # modele affiche

    def on_modele_choisi(self, spinner, nom):
        if nom == self.modele_actuel or nom not in spinner.values:
            return                          # ignore les changements du code
        self.modele_actuel = nom
        provider = self.get_provider_callback()
        threading.Thread(target=self.appliquer_modele, args=(nom, provider), daemon=True).start()

    def appliquer_modele(self, nom, provider):
        try:
            api_client.choisir_modele(nom, provider)
            texte = f"Modele choisi : {nom}"
        except Exception as e:
            texte = f"[erreur] {e}"
        Clock.schedule_once(lambda dt: self.afficher(texte))