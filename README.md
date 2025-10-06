# YouTube Channel Analytics Pipeline

A production-ready data pipeline that extracts, transforms, and loads YouTube channel metrics into a PostgreSQL database for performance analytics and insights. Built with Python, Apache Airflow, and the YouTube Data API v3.

## 📊 Project Overview

This ETL pipeline automates the collection of YouTube channel statistics to help content creators and social media managers:
- Monitor video performance metrics (views, likes, comments)
- Identify underperforming content for optimization
- Track channel growth over time
- Make data-driven decisions about content strategy
- Analyze trends and patterns across video uploads

## 🏗️ Architecture

```
YouTube Data API v3
        ↓
   Python Script / Airflow DAG
        ↓
   Data Extraction & Transformation
        ↓
PostgreSQL Database (Aiven)
        ↓
   PowerBI Dashboard (Analytics & Visualization)
```

### Key Components:
1. **Data Extraction**: YouTube Data API v3 integration
2. **Orchestration**: Apache Airflow for workflow management
3. **Storage**: PostgreSQL database (hosted on Aiven)
4. **Analysis**: PowerBI dashboards for visualization and reporting

## 🚀 Features

- ✅ Automated data extraction from YouTube channels
- ✅ Batch processing of video metadata
- ✅ Incremental data loading to PostgreSQL
- ✅ Airflow orchestration for scheduled runs
- ✅ Error handling and retry logic
- ✅ Scalable architecture (handles 50+ videos per API call)
- ✅ Ready for PowerBI integration

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **PostgreSQL** (or access to a cloud database)
- **Apache Airflow 2.0+** (for automated pipeline)
- **Git** (for cloning the repository)

### Required Python Packages:
```bash
pandas
google-api-python-client
sqlalchemy
psycopg2-binary
apache-airflow
python-dotenv
```

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kilemba/Lynn-Ngugi-Channel-Pipeline.git
cd Lynn-Ngugi-Channel-Pipeline
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Create a `requirements.txt` file with:
```
pandas==2.0.3
google-api-python-client==2.95.0
sqlalchemy==2.0.19
psycopg2-binary==2.9.7
apache-airflow==2.6.3
python-dotenv==1.0.0
```

### Step 3: Set Up YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Create credentials (API Key)
5. Copy your API key

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
CHANNEL_ID=your_target_channel_id

# PostgreSQL Database Configuration
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=10721
DB_NAME=defaultdb
```

**⚠️ IMPORTANT**: Add `.env` to your `.gitignore` file to prevent exposing credentials:
```bash
echo ".env" >> .gitignore
```

### Step 5: Set Up PostgreSQL Database

You can use a local PostgreSQL instance or a cloud provider like Aiven, AWS RDS, or Azure Database.

**For Aiven (recommended for beginners):**
1. Sign up at [Aiven.io](https://aiven.io)
2. Create a PostgreSQL service
3. Copy the connection details to your `.env` file

**Database Connection String Format:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

### Step 6: Update the Code to Use Environment Variables

Modify `Final.LNN.ipynb` to load credentials from `.env`:

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# YouTube API Setup
API_KEY = os.getenv('YOUTUBE_API_KEY')
channel_id = os.getenv('CHANNEL_ID')

# Database Connection
DB_CONNECTION = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_CONNECTION)
```

## 📖 Usage

### Option 1: Run the Jupyter Notebook (One-time Extraction)

```bash
jupyter notebook Final.LNN.ipynb
```

Execute all cells to:
1. Connect to YouTube API
2. Extract channel data
3. Transform data into a pandas DataFrame
4. Load data into PostgreSQL

### Option 2: Deploy Airflow DAG (Automated Pipeline)

1. **Set up Airflow** (if not already installed):
```bash
# Initialize Airflow database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

2. **Configure Airflow Variables**:
```bash
# Set YouTube API Key in Airflow
airflow variables set YOUTUBE_API_KEY your_api_key_here
```

Or via the Airflow UI:
- Navigate to **Admin → Variables**
- Click **"+"** to add a new variable
- Key: `YOUTUBE_API_KEY`
- Value: Your API key

3. **Copy the DAG file**:
```bash
cp LNN_DAG.py ~/airflow/dags/
```

4. **Update the DAG** with your channel ID:
```python
params={'channel_id': 'YOUR_CHANNEL_ID_HERE'}
```

5. **Start Airflow**:
```bash
# Start the scheduler
airflow scheduler

# Start the web server (in a new terminal)
airflow webserver --port 8080
```

6. **Access Airflow UI**:
- Open browser: `http://localhost:8080`
- Login with your admin credentials
- Enable the DAG: `youtube_video_metadata_pipeline`
- Trigger manually or set a schedule

### Setting a Schedule in Airflow

To run the pipeline automatically (e.g., daily at 2 AM):

```python
with DAG(
    dag_id='youtube_video_metadata_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
) as dag:
```

Common schedule intervals:
- `@daily` - Run once a day at midnight
- `@weekly` - Run once a week at midnight on Sunday
- `0 2 * * *` - Run daily at 2:00 AM
- `0 */6 * * *` - Run every 6 hours

## 📊 Data Schema

The pipeline creates a table named `LNN_Show` with the following structure:

| Column Name    | Data Type | Description                          |
|----------------|-----------|--------------------------------------|
| title          | TEXT      | Video title                          |
| video_id       | TEXT      | Unique YouTube video identifier      |
| published_at   | TIMESTAMP | Date and time video was published    |
| views          | INTEGER   | Total view count                     |
| likes          | INTEGER   | Total like count                     |
| comments       | INTEGER   | Total comment count                  |

### Sample Query:

```sql
-- Get top 10 most viewed videos
SELECT title, views, likes, comments
FROM LNN_Show
ORDER BY views DESC
LIMIT 10;

-- Calculate average engagement rate
SELECT 
    AVG((likes + comments) * 100.0 / NULLIF(views, 0)) as avg_engagement_rate
FROM LNN_Show;
```

## 📈 Analytics & Insights

### Key Metrics to Track:

1. **Engagement Rate**: `(Likes + Comments) / Views * 100`
2. **Like-to-View Ratio**: `Likes / Views * 100`
3. **Comment Density**: `Comments / Views * 1000`
4. **Publishing Frequency**: Videos per week/month
5. **Growth Trends**: View count over time

### PowerBI Dashboard (Coming Soon)

The data can be connected to PowerBI for advanced visualizations:
- 📊 Performance trends over time
- 🎯 Top performing content analysis
- 📉 Underperforming video identification
- 🔄 Publishing schedule optimization
- 💡 Content strategy recommendations

## 🔒 Security Best Practices

1. **Never commit credentials**: Always use environment variables or secret management tools
2. **Use `.gitignore`**: Ensure `.env` files are never tracked
3. **Rotate API keys**: Regularly update your YouTube API keys
4. **Limit API permissions**: Use read-only keys when possible
5. **Database security**: Use strong passwords and enable SSL connections
6. **Airflow Variables**: Store sensitive data in Airflow's encrypted Variables or Connections

### For Airflow Production:

Store database credentials in Airflow Connections:
```bash
airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'your-host' \
    --conn-schema 'defaultdb' \
    --conn-login 'your-user' \
    --conn-password 'your-password' \
    --conn-port '10721'
```

## 🎯 Use Cases

### For Content Creators:
- Identify which video topics perform best
- Optimize upload schedules based on engagement patterns
- A/B test titles and thumbnails using historical data
- Track subscriber growth correlation with video performance

### For Social Media Managers:
- Monitor multiple channels from a single dashboard
- Generate automated performance reports
- Benchmark against competitors
- Identify content gaps and opportunities

### For Data Analysts:
- Build predictive models for video performance
- Perform sentiment analysis on top videos
- Create recommendation systems
- Analyze audience retention patterns

## 🚧 Roadmap & Future Enhancements

- [ ] Add data validation and quality checks
- [ ] Implement incremental loading (only new videos)
- [ ] Add sentiment analysis on video titles
- [ ] Create automated email reports
- [ ] Build REST API for data access
- [ ] Add support for multiple channels
- [ ] Implement data versioning and historical tracking
- [ ] Create Tableau/Looker dashboards
- [ ] Add video transcription analysis
- [ ] Integrate with other social media APIs (Instagram, TikTok)

## 🐛 Troubleshooting

### Common Issues:

**Issue**: `googleapiclient.errors.HttpError: 403 quotaExceeded`
- **Solution**: YouTube API has daily quota limits (10,000 units). Wait 24 hours or request quota increase.

**Issue**: `sqlalchemy.exc.OperationalError: could not connect to server`
- **Solution**: Check database credentials, ensure database is running, and verify firewall settings.

**Issue**: Airflow DAG not appearing in UI
- **Solution**: Check DAG file syntax, review Airflow logs (`airflow dags list`), ensure file is in correct directory.

**Issue**: `ModuleNotFoundError: No module named 'google'`
- **Solution**: Install the package: `pip install google-api-python-client`

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Caleb Kilemba**
- GitHub: https://github.com/Kilemba
- LinkedIn: https://www.linkedin.com/in/caleb-kilemba-65515b2a6/
- Email: calebkilemba843@gmail.com

## 🙏 Acknowledgments

- YouTube Data API v3 Documentation
- Apache Airflow Community
- Aiven for cloud database hosting
- Stack Overflow community

## 📧 Contact & Support

For questions, suggestions, or collaboration opportunities:
- Open an issue on GitHub
- Reach out via [your email]
- Connect on LinkedIn

---

⭐ **If you find this project helpful, please give it a star!** ⭐

*Last Updated: January 2025*
