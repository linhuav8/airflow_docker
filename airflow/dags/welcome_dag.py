from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests

def print_welcome():
    print('Welcome to Airflow!')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    try:
        response = requests.get('https://zenquotes.io/api/random')  # 使用 ZenQuotes API
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        if data:
            quote_data = data[0]  # ZenQuotes API 返回一个包含一个 quote 对象的列表
            quote = quote_data['q']  # 引用文本在 'q' 字段
            author = quote_data['a'] # 作者在 'a' 字段
            print('Quote of the day: "{}" - {}'.format(quote, author))
        else:
            print("Failed to retrieve quote from ZenQuotes API: Empty response")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve quote from ZenQuotes API: {e}")

dag = DAG(
    'welcome_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_quote_task = PythonOperator(  # 修改了变量名以避免与函数名冲突
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote_task