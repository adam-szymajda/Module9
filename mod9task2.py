from flask import Flask, url_for, request, render_template, redirect
from album_form import AlbumForm, SearchForm
from albums import albums

app = Flask(__name__)
app.config["SECRET_KEY"] = "veryimportantsecretKEY"

@app.route("/albums/", methods=["GET", "POST"])
def albums_main():
    form = AlbumForm()
    searchform = SearchForm()
    errors = ""
    if request.method == "POST":
        if form.validate_on_submit():
            albums.add(form.data)
            albums.save()
        if searchform.data:
            return render_template("albums.html", form=form, searchform=albums.find(searchform.data), albums=albums.all(), errors=errors)
        return redirect(url_for("albums_main"))

    return render_template("albums.html", form=form, searchform=searchform, albums=albums.all(), errors=errors)

@app.route("/albums/<int:id>/", methods=["GET", "POST"])
def album_details(id):
    album = albums.get(id - 1)
    form = AlbumForm(data=album)
    if request.method == "POST":
        if form.validate_on_submit():
            albums.update(form.data, id - 1)
        return redirect(url_for("albums_main"))

    return render_template("album.html", form=form, id=id)

if __name__ == "__main__":
    app.run(debug=True)
