from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'f3b9a8d4c7e1f0b29a6d4e3c5b7f2a18'  # খুব গুরুত্বপূর্ণ! এটা strong রাখতে হবে

conversion_history = []

# ফিক্সড ইউজার
USERNAME = "admin"
PASSWORD = "mypassword"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "ইউজারনেম বা পাসওয়ার্ড ভুল!"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    result1 = None
    result2 = None

    if request.method == 'POST':
        try:
            total_shotok = float(request.form['totalShotok'])
            ana = int(request.form['ana'])
            gonda = int(request.form['gonda'])
            kora = int(request.form['kora'])
            kranti = int(request.form['kranti'])
            til = int(request.form['til'])

            # হিসাব
            til_per_ana = 4800
            til_per_gonda = 240
            til_per_kora = 60
            til_per_kranti = 20
            full_land_til = 76800

            user_til = (ana * til_per_ana) + (gonda * til_per_gonda) + (kora * til_per_kora) + (kranti * til_per_kranti) + til
            factor = total_shotok / full_land_til
            user_shotok = user_til * factor
            result1 = round(user_shotok, 2)

            sqft_per_shotok = 435.6
            gonda_sqft = 864
            kora_sqft = 216
            kranti_sqft = 72
            til_sqft = 3.6

            total_sqft = user_shotok * sqft_per_shotok
            remainder = total_sqft

            g = int(remainder // gonda_sqft)
            remainder %= gonda_sqft
            k = int(remainder // kora_sqft)
            remainder %= kora_sqft
            kr = int(remainder // kranti_sqft)
            remainder %= kranti_sqft
            t = int(remainder // til_sqft)
            remainder = round(remainder % til_sqft, 2)

            result2 = {
                'gonda': g,
                'kora': k,
                'kranti': kr,
                'til': t,
                'extra_sqft': remainder,
                'total_sqft': round(total_sqft, 2)
            }

            # ইতিহাসে যোগ
            conversion_history.append({
                'ana': ana if ana > 0 else 0,
                'gonda': gonda if gonda > 0 else 0,
                'kora': kora if kora > 0 else 0,
                'kranti': kranti if kranti > 0 else 0,
                'til': til if til > 0 else 0,
                'total_shotok': round(result1, 2),
                'total_sqft': round(result2['total_sqft'], 2)
            })

            if len(conversion_history) > 10:
                conversion_history.pop(0)

        except Exception as e:
            result1 = "ত্রুটি: " + str(e)

    return render_template("index.html", result1=result1, result2=result2, history=conversion_history)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
