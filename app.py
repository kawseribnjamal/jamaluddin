from flask import Flask, render_template, request, session
from collections import deque

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # যেকোনো র‍্যান্ডম সিক্রেট কী দিন

MAX_HISTORY = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

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

            # হিসাবের অংশ
            til_per_ana = 4800
            til_per_gonda = 240
            til_per_kora = 60
            til_per_kranti = 20
            full_land_til = 76800

            user_til = (ana * til_per_ana) + (gonda * til_per_gonda) + (kora * til_per_kora) + (kranti * til_per_kranti) + til
            factor = total_shotok / full_land_til
            user_shotok = user_til * factor
            result1 = round(user_shotok, 3)

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
            remainder %= til_sqft

            result2 = {
                'gonda': g,
                'kora': k,
                'kranti': kr,
                'til': t,
                'extra_sqft': round(remainder, 2),
                'total_sqft': round(total_sqft, 2)
            }

            # হিস্টরিতে যোগ করা
            new_record = {
                'input': {
                    'totalShotok': total_shotok,
                    'ana': ana,
                    'gonda': gonda,
                    'kora': kora,
                    'kranti': kranti,
                    'til': til,
                },
                'output': {
                    'result1': result1,
                    'result2': result2
                }
            }

            history = session['history']
            history.insert(0, new_record)
            if len(history) > MAX_HISTORY:
                history = history[:MAX_HISTORY]
            session['history'] = history

        except Exception as e:
            result1 = f"ত্রুটি হয়েছে: {e}"

    return render_template("index.html", result1=result1, result2=result2, history=session.get('history', []))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
