from flask import Flask, render_template, request
from DBcm import UseDataBase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'plansdb', }

def infoplan_request() -> None:
    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """insert into infoplan (day, plan)
                values (%s, %s)"""

        cursor.execute(_SQL, (request.form['day'],
                        request.form['plan'], ))

@app.route('/')
@app.route('/dayplane')
def view_the_first_page() -> 'html':
    return render_template('first_page.html',
                            the_title='Make your plans')

@app.route('/step_to_save', methods=['POST'])
def step_to_save() -> 'html':
    infoplan_request()
    day = request.form['day']
    plan = request.form['plan']
    return render_template('first_page.html',
                                the_day=day,
                                the_plan=plan,)

@app.route('/database')
def view_the_database() -> 'html':
    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """select day, plan from infoplan"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Day', 'Plan')
    return render_template('database.html',
                           the_title='Database',
                           the_row_titles=titles,
                           the_data=contents,)

if __name__ == '__main__':
    app.run(debug=True)