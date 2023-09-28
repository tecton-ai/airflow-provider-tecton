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

__version__ = "0.2.0"

def get_provider_info():
    return {
        "package-name": "airflow-provider-tecton",
        "name": "Tecton Airflow provider",
        "description": "Apache Airflow provider for Tecton.",
        "hook-class-names": ["airflow_provider_tecton.hooks.tecton_hook.TectonHook"],
        "connection-types": [
            {
                "connection-type": "tecton",
                "hook-class-name": "airflow_provider_tecton.hooks.tecton_hook.TectonHook",
            }
        ],
        "versions": ["0.0.2"],  # Required
        "extra-links": ["tecton_provider.operators.extra_links.RegistryLink"] 
   }


from tecton_provider.operators.tecton_job_operator import TectonJobOperator
from tecton_provider.operators.tecton_trigger_operator import TectonTriggerOperator
from tecton_provider.sensors.tecton_sensor import TectonSensor
