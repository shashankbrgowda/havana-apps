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
from re import findall
from src.havana.utils import query
from src.havana.extensions import mysql1

ni = Blueprint('ni', __name__)

conn1 = mysql1.connect()
cursor1 = conn1.cursor()


@ni.route('/', methods=['GET', 'POST'])
@ni.route('/ni/', methods=['GET', 'POST'])
def ni_app():
    """
    This endpoint queries `gencode_sf5_intropolis_res1.counts` and renders results in a table

    :return: NI template
    """

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
            data = query("select * from counts where tissue like '{}' order by diff desc limit {}".format(tissue, limit)
                         , cursor1, conn1)
        return render_template('ni.html', title='NI', result=data)

    return render_template('ni.html', title='NI')
