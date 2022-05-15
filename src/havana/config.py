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


class Config:
    """
    Contains all application related configuration which are set as environmental variables.
    """

    SECRET_KEY = 'b96db16ba0058f0e8b75619be74f0aec872a63c4bd6b67a7'
    MYSQL_DATABASE_USER = 'nomerge'
    MYSQL_DATABASE_PASSWORD = 'is_coming'
    MYSQL_DATABASE_HOST = 'mysql-ens-havana-prod-1'
    MYSQL_DATABASE_PORT = 4581

    print(f'MYSQL_DATABASE_HOST={MYSQL_DATABASE_HOST}')
    print(f'MYSQL_DATABASE_PORT={MYSQL_DATABASE_PORT}')
