import pendulum
from airflow.sdk import dag, task

from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.validate import validate_weather_data
from src.load import load_weather_data

@dag(
    dag_id="weather_etl_madrid",
    start_date=pendulum.datetime(2026, 11, 16, 23, 0, tz="Europe/Madrid"), 
    end_date=pendulum.datetime(2027, 3, 10, 23, 59, tz="Europe/Madrid"),
    schedule="@hourly",
    catchup=False,
    is_paused_upon_creation=False,
    tags=["weather", "etl"],
)
def weather_etl_dag():

    @task(retries=2)
    def extract_task():
        extract_weather_data()

    @task(retries=2)
    def transform_validate_load_task():
        df = transform_weather_data()
        validate_weather_data(df)
        load_weather_data(df)

    t1 = extract_task()
    t2 = transform_validate_load_task()


    t1 >> t2  # type: ignore[operator]


weather_etl_dag()