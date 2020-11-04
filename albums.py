import json

class Albums:
    def __init__(self, filename):
        try:
            with open(filename, "r") as f:
                self._albums = json.load(f)
        except:
            self._albums = []

    def all(self):
        return self._albums

    def get(self, id):
        # return self._albums[id]
        album = [album for album in self.all() if album['id']==id+1]
        if album:
            return album[0]
        return []

    def add(self, data):
        data.pop('csrf_token')
        self._albums.append(data)
        self.save()

    def add_via_api(self, data):
        self._albums.append(data)
        self.save()

    def save(self):
        with open("albums.json", "w") as f:
            json.dump(self._albums, f)

    def update(self, data, id):
        data.pop('csrf_token')
        self._albums[id] = data
        self.save()

    def update_via_api(self, data, id):
        album = self.get(id)
        if album:
            index = self._albums.index(album)
            self._albums[index] = data
            self.save
            return True
        return False

    def delete(self, id):
        album = self.get(id)
        if album:
            self._albums.remove(album)
            self.save()
            return True
        return False

    def find(self, pattern):
        result = []
        pattern.pop('csrf_token')
        for album in self.all():
            for key, value in album.items():
                if pattern['search'].lower() in str(value).lower():
                    if not album in result:
                        result.append(album)
        return result

    def get_next_id(self):
        return self.all()[-1]['id'] + 1

# albums = Albums()
