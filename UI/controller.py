import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        citta_medie = self._model.get_medie(self._mese)
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selzionato è: "))
        for c in citta_medie.keys():
            self._view.lst_result.controls.append(ft.Text(f"{c}: {citta_medie[c]}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        sequenza = self._model.get_sequenza(self._mese)
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {sequenza[1]} ed è: "))
        for s in sequenza[0].values():
            self._view.lst_result.controls.append(ft.Text(f"[{s.localita} - {s.data}] Umidità = {s.umidita}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

