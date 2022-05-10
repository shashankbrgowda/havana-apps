from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from re import findall
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='./template')
app.config['SECRET_KEY'] = 'b96db16ba0058f0e8b75619be74f0aec872a63c4bd6b67a7'
app.config['MYSQL_DATABASE_USER'] = 'nomerge'
app.config['MYSQL_DATABASE_PASSWORD'] = 'is_coming'
app.config['MYSQL_DATABASE_HOST'] = 'mysql-ens-havana-prod-1'
app.config['MYSQL_DATABASE_PORT'] = 4581

mysql1 = MySQL(db='gencode_sf5_intropolis_res1')
mysql1.init_app(app)
conn1 = mysql1.connect()
cursor1 = conn1.cursor()

mysql2 = MySQL(db='gencode_sf5_human_no_support_introns')
mysql2.init_app(app)
conn2 = mysql2.connect()
cursor2 = conn2.cursor()
title = 'NI'


# TODO: Apply design patterns - Code clean up
@app.route('/', methods=['GET', 'POST'])
@app.route('/ni/', methods=['GET', 'POST'])
def ni():
    if request.method == 'POST':
        tissue = request.form['tissue']
        coords = request.form['coords']
        limit = request.form['limit'] if request.form['limit'] else 50
        matches = findall(r"(\w+):*(\d*)-*(\d*)", coords)
        chr = None
        from_coord = None
        to_coord = None

        if matches:
            chr, from_coord, to_coord = matches[0]

        if from_coord:
            from_coord.replace(",", "")
        if to_coord:
            to_coord.replace(",", "")

        data = None
        if chr and from_coord and to_coord:
            print(f'chr={chr}, from_coord={from_coord}, to_coord={to_coord}, tissue={tissue} and limit={limit}')
            data = query("""select * from counts where tissue like '{}' and chr = '{}' and cstart <= {} and cend >= {} 
            order by cstart limit {}""".format(tissue, chr, from_coord, to_coord, limit), cursor1, conn1)
        elif chr:
            print(f'chr={chr}, tissue={tissue} and limit={limit}')
            data = query("select * from counts where tissue like '{}' and chr = '{}' order by diff desc limit {}"
                         .format(tissue, chr, limit), cursor1, conn1)
        else:
            print(f'tissue={tissue} and limit={limit}')
            sql = "select * from counts where tissue like '{}' order by diff desc limit {}".format(tissue, limit)
            cursor1.execute(sql)
            conn1.commit()
            data = query("select * from counts where tissue like '{}' order by diff desc limit {}".format(tissue, limit)
                         , cursor1, conn1)
        return render_template('ni.html', title=title, result=data)
    return render_template('ni.html', title=title)


@app.route('/nsi/', methods=['GET', 'POST'])
def nsi():
    if request.method == 'POST':
        otter_id = request.form['otter_id']
        limit = request.form['limit'] if request.form['limit'] else 50

        data = None
        if 'OTTHUMG' in otter_id:
            print(f"Contains 'OTTHUMG', otter_id={otter_id}, limit={limit}")
            data = query("""SELECT * FROM no_intropolis WHERE otter_gene_id  LIKE '%{}%' ORDER BY otter_trans_id, chr, 
            istart LIMIT {}""".format(otter_id, limit), cursor2, conn2)
        elif 'OTTHUMT' in otter_id:
            print(f"Contains 'OTTHUMT', otter_id={otter_id}, limit={limit}")
            data = query("""SELECT * FROM no_intropolis WHERE otter_trans_id  LIKE '%{}%' ORDER BY otter_trans_id, chr, 
            istart LIMIT {}""".format(otter_id, limit), cursor2, conn2)
        else:
            print(f'otter_id={otter_id}, limit={limit}')
            data = query("""SELECT * FROM no_intropolis WHERE gene_name  LIKE '%{}%' ORDER BY otter_trans_id, chr, 
                        istart LIMIT {}""".format(otter_id, limit), cursor2, conn2)
        return render_template('nsi.html', title='NSI', result=data)
    return render_template('nsi.html', title='NSI')


@app.route('/intron/')
def intron():
    return render_template('intron.html', title='Intron')


@app.route('/health/')
def health_check():
    return {
        'status': 'UP',
        'timestamp': datetime.now()
    }


def query(sql, cursor, conn):
    print(f'SQL={sql}')
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()


if __name__ == '__main__':
    app.run(debug=False)
