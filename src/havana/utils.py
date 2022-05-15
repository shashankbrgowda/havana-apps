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

from typing import Any

from pymysql.connections import Connection
from pymysql.cursors import Cursor


def query(sql: str, cursor: Cursor, conn: Connection) -> tuple[tuple[Any, ...], ...]:
    """
    Fetch all rows for a given SQL query.

    :param sql: SQL query string
    :param cursor: Mysql Cursor
    :param conn: Mysql Connection
    :return: Rows fetched
    """
    print(f'SQL={sql}')
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()
