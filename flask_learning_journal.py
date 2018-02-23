from flask import Flask, render_template, url_for, request, redirect, flash
from flask_learning_journal_models import Entry
from flask_learning_forms import EntryForm
from os import urandom
from peewee import OperationalError, IntegrityError


app = Flask(__name__)
app.secret_key = urandom(25)


@app.route('/')
@app.route('/entries')
def list_all():
    all_entries = Entry.select()
    return render_template('index.html', all_entries=all_entries)


@app.route('/new', methods=['GET', 'POST'])
def new():
    new_entry_form = EntryForm()
    if request.method == 'POST':
        # There could be much more data checking here
        if new_entry_form.title.data == '':
            flash('Please enter a valid title')
            return render_template('new.html', new_entry_form=new_entry_form)
        try:
            new_entry = Entry.create(
                title=new_entry_form.title.data,
                date=new_entry_form.date.data,
                time_spent=new_entry_form.time_spent.data,
                learned=new_entry_form.learned.data,
                resources=new_entry_form.resources.data
            )
            new_entry.save()
            return redirect(url_for('list_all'))
        except IntegrityError as e:
            flash('Data error: {}'.format(e.args[0]))
            flash('Please check your entry data and try again')
            return render_template('new.html', new_entry_form=new_entry_form)
    else:
        return render_template('new.html', new_entry_form=new_entry_form)


@app.route('/entries/edit/<entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    edit_entry = Entry.get(Entry.id == entry_id)
    edit_entry_form = EntryForm(obj=edit_entry)
    if request.method == 'POST':
        edited_entry = Entry.update(
            title=edit_entry_form.title.data,
            date=edit_entry_form.date.data,
            time_spent=edit_entry_form.time_spent.data,
            learned=edit_entry_form.learned.data,
            resources=edit_entry_form.resources.data
        ).where(Entry.id == entry_id)
        edited_entry.execute()
        return redirect(url_for('detail', entry_id=entry_id))
    else:
        return render_template('edit.html', edit_entry=edit_entry,
                               edit_entry_form=edit_entry_form)


@app.route('/entries/delete/<entry_id>')
def delete(entry_id):
    delete_entry = Entry.delete().where(Entry.id == entry_id)
    delete_entry.execute()
    return redirect(url_for('list_all'))


@app.route('/entries/<entry_id>')
def detail(entry_id):
    entry_detail = Entry.get(Entry.id == entry_id)
    return render_template('detail.html', entry_detail=entry_detail)


if __name__ == '__main__':
    try:
        Entry.create_table()
        print('Creating new database')
    except OperationalError:
        print('Using existing database')
    app.run(debug=True)

