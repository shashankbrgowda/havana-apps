#  See the NOTICE file distributed with this work for additional information
#  regarding copyright ownership.
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from flask import render_template, request, Blueprint
from src.havana.utils import query
from src.havana.extensions import mysql2

nsi = Blueprint('nsi', __name__)

conn2 = mysql2.connect()
cursor2 = conn2.cursor()


@nsi.route('/nsi/', methods=['GET', 'POST'])
def nsi_app():
    """
    This endpoint queries `gencode_sf5_human_no_support_introns.no_intropolis` and renders results in a table

    :return: NSI template
    """

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
