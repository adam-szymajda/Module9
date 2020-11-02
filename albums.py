import json

class Albums:
    def __init__(self):
        try:
            with open("albums.json", "r") as f:
                self._albums = json.load(f)
        except:
            self._albums = []

    def all(self):
        return self._albums

    def get(self, id):
        return self._albums[id]

    def add(self, data):
        data.pop('csrf_token')
        self._albums.append(data)

    def save(self):
        with open("albums.json", "w") as f:
            json.dump(self._albums, f)

    def update(self, data, id):
        data.pop('csrf_token')
        self._albums[id] = data
        self.save()

    def find(self, pattern):
        result = []
        pattern.pop('csrf_token')
        # print(self._albums)
        for album in self.all():
            for key, value in album.items():
                if pattern['search'] in str(value):
                    print(album)
                    result.append(album)
        print(result)
        print(self._albums)
        return self._albums

albums = Albums()
