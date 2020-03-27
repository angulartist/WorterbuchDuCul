from datetime import timedelta

from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'angulartist',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email_on_failure': False,
    'email_on_retry': False,
}


dag = DAG(
    'bot_du_cul_scheduler',
    default_args=default_args,
    description='Description du cul.',
    schedule_interval='*/10 * * * *',
    max_active_runs=1,
    catchup=False,
)


run_tweet = BashOperator(
    task_id='do_tweet',
    bash_command='python /storage/botducul/main.py',
    dag=dag,
)


run_tweet
