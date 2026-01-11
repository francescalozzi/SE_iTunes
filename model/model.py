import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.albums = []
        self.album_playlist_map = {}
        self.soluzione_best = []
        self.id_map = {}

    def carica_albums(self,min_duration):
        self.albums = DAO.get_all_album_by_min_durata(min_duration)
        self.id_map = {a.id: a for a in self.albums}  #ASSOCIA AD OGNI ID L'OGGETTO ALBUM

    def carica_album_playlists(self):
        self.album_playlist_map = DAO.get_albums_playlist_map(self.albums)

    def build_graph(self):
        self.G.clear()
        self.G.add_nodes_from(self.albums)

        for i, a1 in enumerate(self.albums):
            for a2 in self.albums[i+1:]:
                if self.album_playlist_map[a1] & self.album_playlist_map[a2]:
                    self.G.add_edge(a1, a2)


    def get_component(self,album):
        if album not in self.G:
            return []
        return list(nx.node_connected_component(self.G, album))


    def compute_best_set(self,start_album, max_duration):
        component = self.get_component(start_album)
        self.soluzione_best = []
        self._ricorsione(component, [start_album], start_album.duration ,max_duration)
        return self.soluzione_best

    def _ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

        for album in albums:
            if album in current_set:
                continue
            new_duration = current_duration + album.duration

            if new_duration <= max_duration:
                current_set.append(album)
                self._ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()
