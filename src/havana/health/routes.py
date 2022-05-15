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

from flask import Blueprint
from datetime import datetime

health = Blueprint('health', __name__)


@health.route('/health/')
def health_check():
    """
    Health check endpoint - helpful for liveness/readiness probe in k8s

    :return: sample response
    """
    return {
        'status': 'UP',
        'timestamp': datetime.now()
    }
