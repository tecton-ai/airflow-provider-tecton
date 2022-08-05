# Copyright 2022 Tecton, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-tecton",
        "name": "Apache Airflow Providers Tecton",
        "description": "Apache Airflow Providers for Tecton.",
        "hook-class-names": [
            "apache_airflow_providers_tecton.hooks.tecton_hook.TectonHook"
        ],
        "connection-types": [
            {
                "connection-type": "tecton",
                "hook-class-name": "apache_airflow_providers_tecton.hooks.tecton_hook.TectonHook",
            }
        ],
        "versions": ["0.0.1"],  # Required
    }
