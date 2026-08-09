from datetime import datetime
import os
 
import validators
import requests
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
 
from .db import (
    get_db_connection,
    find_url_by_name,
    create_url,
    get_urls_with_last_check,
    get_url_by_id,
    get_checks_for_url,
    create_url_check,
)
from .parser import parse_page
from .utils import normalize_url
 
 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-only-insecure-key-change-me-please') # NOSONAR
csrf = CSRFProtect(app)
 
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
 
 
@app.route('/urls', methods=['GET', 'POST'])
def urls_list():
    if request.method == 'POST':
        url_input = request.form.get('url')
        normalized = normalize_url(url_input)
        if not validators.url(normalized) or len(normalized) > 255:
            flash('Некорректный URL', 'danger')
            return render_template('index.html'), 422
 
        conn = get_db_connection()
        try:
            existing_url = find_url_by_name(conn, normalized)
            if existing_url:
                url_id = existing_url['id']
                flash('Страница уже существует', 'info')
            else:
                url_id = create_url(conn, normalized, datetime.now())
                flash('Страница успешно добавлена', 'success')
        finally:
            conn.close()
        return redirect(url_for('url_show', url_id=url_id))
 
    conn = get_db_connection()
    try:
        urls = get_urls_with_last_check(conn)
    finally:
        conn.close()
    return render_template('urls.html', urls=urls)
 
 
@app.route('/urls/<int:url_id>', methods=['GET'])
def url_show(url_id):
    conn = get_db_connection()
    try:
        url = get_url_by_id(conn, url_id)
        if url is None:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('urls_list'))
        checks = get_checks_for_url(conn, url_id)
    finally:
        conn.close()
    return render_template('url.html', url=url, checks=checks)
 
 
@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_check(url_id):
    conn = get_db_connection()
    try:
        url = get_url_by_id(conn, url_id)
        if url is None:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('urls_list'))
 
        try:
            response = requests.get(url['name'], timeout=7)
            response.raise_for_status()
        except requests.RequestException:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('url_show', url_id=url_id))
 
        page_data = parse_page(response.text)
        create_url_check(
            conn,
            url_id,
            response.status_code,
            page_data['h1'],
            page_data['title'],
            page_data['description'],
            datetime.now(),
        )
        flash('Страница успешно проверена', 'success')
    except psycopg2.Error:
        conn.rollback()
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        conn.close()
    return redirect(url_for('url_show', url_id=url_id))
 
 
if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'False') == 'True')
 
