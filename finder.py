@app.route('/search', methods=['POST'])
def search():

    name = request.form['name']
    animals = Animal.query.filter_by(name=name).all()
    return render_template('search_results.html', animals=animals)