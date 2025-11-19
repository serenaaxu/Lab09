from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO


class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi
        self._tour_disponibili = []
        self._max_budget = 0
        self._max_giorni = 0

        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """

        # TODO
        self.tour_attrazioni = TourDAO.get_tour_attrazioni()

        if self.tour_attrazioni is None:
            self.tour_attrazioni = []

        for id_tour, id_attrazione in self.tour_attrazioni:
            if id_tour in self.tour_map and id_attrazione in self.attrazioni_map:
                tour_obj = self.tour_map[id_tour]
                attr_obj = self.attrazioni_map[id_attrazione]

                tour_obj.attrazioni.add(attr_obj)
                tour_obj.valore_culturale_totale += attr_obj.valore_culturale


    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO

        self._tour_disponibili = []
        for t in self.tour_map.values():
            if t.id_regione == id_regione:
                self._tour_disponibili.append(t)

        self._ricorsione(0, [],0,0,0, set())

        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno
        if valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente
            self._pacchetto_ottimo = list(pacchetto_parziale)
            self._costo = costo_corrente

        for i in range(start_index, len(self._tour_disponibili)):
            tour = self._tour_disponibili[i]

            if self._max_budget is not None and (costo_corrente + tour.costo > self._max_budget):
                continue

            if self._max_giorni is not None and (durata_corrente + tour.data_tour > self._max_giorni):
                continue

            attrazioni_tour_ids = {a.id for a in tour.attrazioni}

            if not attrazioni_usate.isdisjoint(attrazioni_tour_ids):
                continue

            pacchetto_parziale.append(tour)
            nuove_attrazioni_usate = attrazioni_usate | attrazioni_tour_ids

            self._ricorsione(
                i + 1,  # start_index + 1 per non riutilizzare lo stesso tour
                pacchetto_parziale,
                costo_corrente + tour.costo,
                durata_corrente + tour.durata_giorni,
                valore_corrente + tour.valore_culturale_totale,
                nuove_attrazioni_usate
            )

            # F. BACKTRACKING (Rimuovi)
            pacchetto_parziale.pop()
















