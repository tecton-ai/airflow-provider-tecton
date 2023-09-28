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
import textwrap
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

from tecton_provider.operators.tecton_job_operator import TectonJobOperator
from tecton_provider.sensors.tecton_sensor import TectonSensor

WORKSPACE = "my_workspace"
FEATURE_VIEW = "my_stream_feature_view"

with DAG(
    dag_id="example_tecton_job",
    default_args={"retries": 3},
    description=textwrap.dedent(
        """
            This example shows a BatchFeatureView with triggered materialization
            where Airflow handles retries. Note that the retry parameters
            used are standard Airflow retries.

            Because this is a StreamFeatureView, the materialization job 
            is not needed to write to the online store.

            TectonSensor is used for online only. 
            Model training can wait for `tecton_job` becuase this
            operator waits for completion.
            The online reporting part can proceed independently.

            Model training starts when the offline feature store is ready, 
            And a report when the online feature store is up to date. 

            BashOperators are used in place of actual training/reporting operators.
    """
    ),
    start_date=datetime(2022, 7, 10),
    schedule_interval=timedelta(days=1),
) as dag:
    process_hive_data = BashOperator(
        task_id="process_hive_data", bash_command='echo "hive data processed!"'
    )
    tecton_job = TectonJobOperator(
        task_id="tecton_job",
        workspace=WORKSPACE,
        feature_view=FEATURE_VIEW,
        online=False,
        offline=True,
        # retries inherited from default_args
    )
    online_data_ready = TectonSensor(
        task_id="wait_for_online",
        workspace=WORKSPACE,
        feature_view=FEATURE_VIEW,
        online=True,
        offline=False,
    )
    train_model = BashOperator(
        task_id="train_model", bash_command='echo "model trained!"'
    )
    report_online_done = BashOperator(
        task_id="report_online_done", bash_command='echo "online data ready!"'
    )

    process_hive_data >> tecton_job >> train_model
    online_data_ready >> report_online_done
