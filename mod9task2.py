from flask import Flask, url_for, request, render_template, redirect, jsonify, abort, make_response
from album_form import AlbumForm, SearchForm
from albums import Albums

albums = Albums("albums.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "veryimportantsecretKEY"

@app.route("/albums/", methods=["GET", "POST"])
def albums_main():
    form = AlbumForm()
    searchform = SearchForm()
    errors = ""
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.data)
            temp = {
                'id' : albums.get_next_id(),
                'title' : form.data.get('title'),
                'artist' : form.data.get('artist'),
                'genre' : form.data.get('genre'),
                'year' : form.data.get('year'),
                'csrf_token' : form.data.get('csrf_token'),
            }
            albums.add(temp)
            return render_template("albums.html", form=form, searchform=searchform, albums=albums.all(), search_result=None, errors=errors)
        if searchform.data:
            search_result = albums.find(searchform.data)
            return render_template("albums.html", form=form, searchform=searchform, albums=albums.all(), search_result=search_result, errors=errors)

    return render_template("albums.html", form=form, searchform=searchform, albums=albums.all(), search_result=None, errors=errors)

@app.route("/albums/<int:id>/", methods=["GET", "POST"])
def album_details(id):
    album = albums.get(id - 1)
    form = AlbumForm(data=album)
    if request.method == "POST":
        if form.validate_on_submit():
            albums.update(form.data, id - 1)
        return redirect(url_for("albums_main"))

    return render_template("album.html", form=form, id=id)

@app.route("/api/v1/albums/", methods=["GET"])
def albums_list_api_v1():
    return jsonify(albums.all())

@app.route("/api/v1/albums/<int:id>/", methods=["GET"])
def get_album(id):
    album = albums.get(id)
    if not album:
        abort(404)
    return jsonify({"album":album})

@app.route("/api/v1/albums/", methods=["POST"])
def add_album():
    print(request.json)
    if ( not request.json or
        not 'title' in request.json or
        not 'artist' in request.json
    ):
        abort(400)
    album = {
        'id' : albums.get_next_id(),
        'title' : request.json['title'],
        'artist' : request.json['artist'],
        'genre' : request.json['genre'],
        'year' : request.json['year'],
    }
    albums.add_via_api(album)
    return jsonify({"album": album}), 201

@app.route("/api/v1/albums/<int:id>", methods=["DELETE"])
def delete_album(id):
    result = albums.delete(id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/albums/<int:id>", methods=["PUT"])
def update_album(id):
    album = albums.get(id)
    print(album)
    if not album:
        abort(404)
    if not request.json:
        abort(404)
    data = request.json
    if any ([
        'title' in data and not isinstance(data.get('title'), str),
        'artist' in data and not isinstance(data.get('artist'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        # 'year' in data and not isinstance(data.get('year'), int),
    ]):
        abort(400)
    album = {
        'id' : album['id'],
        'title' : data.get('title', album['title']),
        'artist' : data.get('artist', album['artist']),
        'genre' : data.get('genre', album['genre']),
        'year' : data.get('year', album['year']),
    }
    print("\n")
    print(album)
    albums.update_via_api(album, id)
    return jsonify({'album': album})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)
