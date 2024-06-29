from copy import deepcopy

from database import meteo_dao
from numpy import mean

class Model:

    def __init__(self):
        self.sequenza = {}
        self.costo = 0

    def get_medie(self, _mese):
        situazioni = meteo_dao.MeteoDao.get_all_situazioni()
        medie_citta = {}
        for s in situazioni:
            if s.data.month == _mese:
                if s.localita not in medie_citta:
                    medie_citta[s.localita] = [s.umidita]
                else:
                    medie_citta[s.localita].append(s.umidita)
        for c in medie_citta:
            medie_citta[c] = mean(medie_citta[c])
        return medie_citta

    def get_sequenza(self, _mese):
        all_situazioni = meteo_dao.MeteoDao.get_all_situazioni()
        giornate = {}
        for s in all_situazioni:
            if s.data.month == _mese and s.data.day <= 15:
                if s.data.day not in giornate:
                    giornate[s.data.day] = [s]
                else:
                    giornate[s.data.day].append(s)

        self.find_sequenza(giornate, {}, 0, {}, (None, None))

        return self.sequenza, self.costo

    def find_sequenza(self, giorni_mancanti: dict, giorni_decisi: dict, costo_attuale: int, citta_ripetizioni: dict, citta_attuale: tuple):
        if len(giorni_mancanti.keys()) == 0:
            if self.costo == 0 or costo_attuale < self.costo:
                self.sequenza = giorni_decisi
                self.costo = costo_attuale
            return
        else:
            print(giorni_decisi)
            for situazione in giorni_mancanti[len(giorni_decisi)+1]:
                if self.costo != 0 and costo_attuale >= self.costo or (citta_attuale in citta_attuale and citta_ripetizioni[citta_attuale] == 6):
                    return
                temp_giorni_mancanti = deepcopy(giorni_mancanti)
                temp_giorni_mancanti.pop(len(giorni_decisi)+1)
                temp_giorni_decisi = deepcopy(giorni_decisi)
                temp_giorni_decisi[len(giorni_decisi)+1] = situazione
                temp_citta_ripetizioni = deepcopy(citta_ripetizioni)
                if situazione.localita not in temp_citta_ripetizioni:
                    temp_citta_ripetizioni[situazione.localita] = 1
                else:
                    temp_citta_ripetizioni[situazione.localita] = temp_citta_ripetizioni[situazione.localita]+1
                    print(temp_citta_ripetizioni[situazione.localita])

                if citta_attuale[0] == situazione.localita and 1 <= citta_attuale[1] < 3:
                    self.find_sequenza(temp_giorni_mancanti, temp_giorni_decisi, costo_attuale+situazione.umidita, temp_citta_ripetizioni, (situazione.localita, citta_attuale[1]+1))
                else:
                    if citta_attuale[0] == situazione.localita and temp_citta_ripetizioni[situazione.localita] <= 6:
                        self.find_sequenza(temp_giorni_mancanti, temp_giorni_decisi, costo_attuale+situazione.umidita, temp_citta_ripetizioni, (situazione.localita, citta_attuale[1]+1))
                    if citta_attuale[0] != situazione.localita and temp_citta_ripetizioni[situazione.localita]+min(3, len(giorni_mancanti)) <= 6:
                        self.find_sequenza(temp_giorni_mancanti, temp_giorni_decisi, costo_attuale + situazione.umidita+100, temp_citta_ripetizioni, (situazione.localita, 1))