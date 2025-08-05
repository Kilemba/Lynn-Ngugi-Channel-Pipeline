## Importing modules for the DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from googleapiclient.discovery import build
from datetime import datetime, timedelta


##Initializing youtube API
def get_youtube_client():
    from airflow.models import Variable
    api_key = Variable.get("YOUTUBE_API_KEY")
    return build('youtube', 'v3', developerKey=api_key)

# Step 1: Get uploads playlist ID
def get_uploads_id(**kwargs):
    youtube = get_youtube_client()
    channel_id = kwargs['params']['channel_id']
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    kwargs['ti'].xcom_push(key='uploads_id', value=uploads_id)

# Step 2: Get video IDs from uploads playlist
def get_video_ids_task(**kwargs):
    youtube = get_youtube_client()
    uploads_id = kwargs['ti'].xcom_pull(key='uploads_id', task_ids='get_uploads_id')
    video_ids = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    kwargs['ti'].xcom_push(key='video_ids', value=video_ids)

# Step 3: Get video details
def get_video_details_task(**kwargs):
    youtube = get_youtube_client()
    video_ids = kwargs['ti'].xcom_pull(key='video_ids', task_ids='get_video_ids')
    video_data = []

    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50])
        ).execute()
        for item in response['items']:
            data = dict(
                title=item['snippet']['title'],
                video_id=item['id'],
                published_at=item['snippet']['publishedAt'],
                views=item['statistics'].get('viewCount', 0),
                likes=item['statistics'].get('likeCount', 0),
                comments=item['statistics'].get('commentCount', 0)
            )
            video_data.append(data)

    # For now, just print
    for vid in video_data:
        print(vid)

# DAG Definition
default_args = {
    'start_date': datetime(2023, 1, 1),
    'owner': 'airflow',
    'retries': 1
}

with DAG(
    dag_id='youtube_video_metadata_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Run on demand
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='get_uploads_id',
        python_callable=get_uploads_id,
        provide_context=True,
        params={'channel_id': 'UC_x5XG1OV2P6uZZ5FSM9Ttw'},  # example: Google Developers
    )

    t2 = PythonOperator(
        task_id='get_video_ids',
        python_callable=get_video_ids_task,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id='get_video_details',
        python_callable=get_video_details_task,
        provide_context=True
    )

    t1 >> t2 >> t3