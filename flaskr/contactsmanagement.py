from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import logging

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('contactsmanagement', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    subscriptions = db.execute(
        '''SELECT s.subscription_name as name, a.f_name as f_name, a.l_name as l_name, a.email as email, s.owner_id as owner_id, s.id as id 
        FROM subscriptions s 
        JOIN admins a 
        ON s.owner_id = a.id'''
    ).fetchall()
    return render_template('subscriptions/index.html', subscriptions=subscriptions)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        subscription = request.form['name']
        error = None

        if not subscription:
            error = 'Subscription is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO Subscriptions (subscription_name, owner_id)'
                ' VALUES (?, ?)',
                (subscription, g.user['id'])
            )
            db.commit()
            return redirect(url_for('contactsmanagement.index'))

    return render_template('subscriptions/create.html')


def get_subscription_contacts(id):
    subscription = get_db().execute(
        '''SELECT s.owner_id as owner_id, c.email as email, c.f_name as f_name, c.l_name as l_name, c.id as id FROM contacts c
        JOIN subscriptions s ON c.subscription_id = s.id
        WHERE c.subscription_id = ?''',
        (id,)
    ).fetchall()

    return subscription


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    contacts = get_subscription_contacts(id)
    db = get_db()
    name = db.execute(
        '''
        SELECT subscription_name 
        FROM subscriptions
        where id = ?''', (id,)
    ).fetchone()[0]

    if request.method == 'POST':
        f_name = request.form['f_name'].strip()
        l_name = request.form['l_name'].strip()
        email = request.form['email'].strip()
        error = None

        if not f_name:
            error = 'First Name is required.'

        if not l_name:
            error = 'Last Name is required.'

        if not email:
            error = 'Email is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                '''
                Insert into contacts(email, f_name, l_name, subscription_id) values (?, ?, ?, ?)
                ''', (email, f_name, l_name, id)
            )
            db.commit()
            return redirect(url_for('contactsmanagement.update', contacts=contacts, name=name, id=id))

    return render_template('subscriptions/update.html', contacts=contacts, name=name, id=id)


@bp.route('/deleteContact', methods=('GET',))
@login_required
def delete_contact():
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    contact_id = request.args['contact_id']
    db = get_db()
    subscription_id = db.execute('SELECT subscription_id from contacts where id = ?', (contact_id,)).fetchone()[0]
    logging.error(subscription_id)
    logging.error(contact_id)

    db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    db.commit()
    return redirect(url_for('contactsmanagement.update', id = subscription_id))


@bp.route('/<int:id>/deletesubscription', methods=('GET',))
@login_required
def delete_subscription(id):
    get_subscription_contacts(id)
    db = get_db()
    db.execute('DELETE FROM contacts WHERE subscription_id = ?', (id,))
    db.execute('DELETE FROM subscriptions WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('contactsmanagement.index'))