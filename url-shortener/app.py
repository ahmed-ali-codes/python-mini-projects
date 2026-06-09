import string
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, init_db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

def generate_short_id(num_chars=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(num_chars))

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        original_url = request.form['url']

        if not original_url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        conn = get_db_connection()
        
        # Check if URL already exists
        url_data = conn.execute('SELECT * FROM urls WHERE original_url = ?', (original_url,)).fetchone()
        
        if url_data:
            short_id = url_data['short_id']
        else:
            short_id = generate_short_id()
            conn.execute('INSERT INTO urls (original_url, short_id) VALUES (?, ?)',
                         (original_url, short_id))
            conn.commit()
            
        conn.close()
        
        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url, short_id=short_id)

    return render_template('index.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    conn = get_db_connection()
    url_data = conn.execute('SELECT * FROM urls WHERE short_id = ?', (short_id,)).fetchone()
    
    if url_data:
        conn.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_id = ?', (short_id,))
        conn.commit()
        conn.close()
        return redirect(url_data['original_url'])
    else:
        conn.close()
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route('/stats/<short_id>')
def stats(short_id):
    conn = get_db_connection()
    url_data = conn.execute('SELECT * FROM urls WHERE short_id = ?', (short_id,)).fetchone()
    conn.close()

    if url_data:
        return render_template('stats.html', url=url_data)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        init_db()
    app.run(debug=True)
