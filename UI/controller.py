import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_strumenti(self, e):
        """
        Gestisce il popolamento della ListView con tutti gli strumenti presenti nel database.
        """
        # Pulizia dei risultati precedenti
        self._view.lista_strumenti.controls.clear()

        # Chiamata al modello
        strumenti = self._model.get_strumenti()

        # Gestione dell'errore di connessione o database vuoto
        if strumenti is None:
            self._view.show_alert("Errore durante la connessione al database o il recupero dei dati.")
            self._view.update()
            return

        if len(strumenti) == 0:
            self._view.show_alert("Nessuno strumento trovato nel database.")
            self._view.update()
            return

        # Popolamento del controllo ListView
        for s in strumenti:
            self._view.lista_strumenti.controls.append(ft.Text(str(s)))

        self._view.update()

    def cerca_strumenti_per_tipo(self, e):
        """
        Gestisce la ricerca degli strumenti dato un tipo inserito nell'input di testo.
        """
        # Pulizia dei risultati precedenti
        self._view.lista_strumenti_ricerca.controls.clear()

        tipo_ricercato = self._view.input_tipo_strumento.value

        # Controllo validità dell'input
        if not tipo_ricercato or tipo_ricercato.strip() == "":
            self._view.show_alert("Inserisci un tipo di strumento per effettuare la ricerca.")
            self._view.update()
            return

        # Chiamata al modello
        strumenti = self._model.cerca_strumenti_per_tipo(tipo_ricercato)

        # Gestione dell'errore di connessione o nessun risultato trovato
        if strumenti is None:
            self._view.show_alert("Errore durante la connessione al database.")
            self._view.update()
            return

        if len(strumenti) == 0:
            self._view.show_alert(f"Nessuno strumento trovato di tipo '{tipo_ricercato}'.")
            self._view.update()
            return

        # Popolamento del controllo ListView con i risultati
        for s in strumenti:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(s)))

        self._view.update()