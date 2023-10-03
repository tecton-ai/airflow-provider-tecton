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

WORKSPACE = "airflow"
FEATURE_VIEW = "user_transaction_metrics_airflow"

with DAG(
    dag_id="example_tecton",
    default_args={"retries": 0},
    description=textwrap.dedent(
        """
            This example shows a use case where you have a BatchFeatureView with triggered materialization
            where Airflow handles retries. Note that the retry parameters
            used are standard Airflow retries.

            The materialization will process new data that is found within the defined data source
            that is new as of yesterday, this can be set to a different time window via the 
            start_time and end_time parameters

            In this scenario, we want to kick off a model training when the offline feature store is ready
        """
    ),
    start_date=datetime(2023, 9, 27),
    schedule_interval=timedelta(days=1),
    catchup=False,
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
        start_time=datetime.combine(datetime.now() - timedelta(days = 1), datetime.min.time()),
        end_time=datetime.combine(datetime.now(), datetime.min.time()),
        # retries inherited from default_args
    )
    train_model = BashOperator(
        task_id="train_model", bash_command='echo "model trained!"'
    )

    process_hive_data >> tecton_job >> train_model
