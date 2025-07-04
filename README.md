# Comment Watcher

A modular Python application for monitoring regulations.gov comments for specific keywords with Teams and email webhook notifications.

## 🏗️ Architecture

The application is structured with clear separation of concerns:

- **`config.py`** - Configuration management and environment variables
- **`fetcher.py`** - Regulations.gov API interactions
- **`filter.py`** - Keyword matching logic
- **`notifier.py`** - Alert formatting and webhook notifications
- **`storage.py`** - SQLite database management
- **`main.py`** - Orchestration logic
- **`db_utils.py`** - Database query and management utilities
- **`test_notifications.py`** - Test webhook notifications
- **`test_webhook_server.py`** - Local webhook server for testing

## 📋 Module Functions

### `fetcher.py`

- `fetch_metadata(since_date)` → returns list of comment metadata
- `fetch_comment_detail(comment_id)` → returns full comment content

### `filter.py`

- `flag_by_keyword(metadata_list, keyword_list)` → returns list of (id, keyword) hits
- `recheck_full_text(full_comment, keyword_list)` → returns True/False or keyword match

### `notifier.py`

- `format_alert(comment)` → returns formatted console string
- `format_teams_message(comment)` → returns Teams message card
- `format_email_message(comment)` → returns email message
- `send_teams_alert(comment)` → sends Teams webhook
- `send_email_alert(comment)` → sends email webhook
- `send_alerts(comments)` → sends all notification types
- `test_notifications()` → tests all notification systems

### `storage.py`

- `save_flagged_comments(comment_list)` → saves to SQLite database
- `load_seen_ids()` → loads previously seen comment IDs
- `mark_as_seen(id)` → marks a comment as seen to avoid duplicates
- `get_comments_by_keyword(keyword)` → query comments by keyword
- `get_comments_by_date_range(start, end)` → query comments by date range
- `get_statistics()` → get database statistics
- `export_to_json(filename)` → export data to JSON

### `main.py`

- Loads environment variables
- Sets up keywords
- Orchestrates the monitoring cycle: fetch → flag → pull detail → notify → save

## 🗄️ SQLite Database

The application uses SQLite for data storage with two main tables:

### `flagged_comments` table

- Stores all flagged comments with full details
- Includes metadata like title, date, submitter, organization
- Tracks when comments were added to the database

### `seen_ids` table

- Tracks previously processed comment IDs
- Prevents duplicate processing of the same comments
- Includes timestamps for when IDs were marked as seen

## 🔔 Notification System

The application supports multiple notification channels:

### Microsoft Teams

- Rich message cards with comment details
- Direct links to regulations.gov comments
- Configurable webhook URL
- Includes keyword, title, submitter, and organization

### Email Webhooks

- Plain text and HTML email formats
- Configurable webhook URL for email services
- Includes all comment metadata and direct links
- Compatible with Zapier, IFTTT, or custom email services

### Console Output

- Detailed console logging for all alerts
- Includes comment links and full metadata
- Progress tracking and summary statistics

## 🚀 Quick Start

1. **Install dependencies:**

   ```bash
   pip install requests python-dotenv flask
   ```

2. **Set up your API key:**
   Create a `.env` file:

   ```
   API_KEY=your_regulations_gov_api_key_here
   ```

3. **Configure notifications (optional):**

   ```
   # Teams notifications
   TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/...
   ENABLE_TEAMS_ALERTS=true

   # Email notifications
   EMAIL_WEBHOOK_URL=https://your-email-service.com/webhook
   ENABLE_EMAIL_ALERTS=true
   ```

4. **Run the watcher:**
   ```bash
   python main.py
   ```

## 📖 Usage Examples

### Basic Usage

```python
from main import run_monitoring_cycle

results = run_monitoring_cycle()
print(f"Found {results['flagged_count']} flagged comments")
```

### Database Queries

```python
from storage import get_comments_by_keyword, get_statistics

# Get all comments matching a keyword
pesticide_comments = get_comments_by_keyword("pesticide")

# Get database statistics
stats = get_statistics()
print(f"Total comments: {stats['total_flagged_comments']}")
```

### Using Database Utilities

```bash
# View database statistics
python db_utils.py stats

# View recent comments
python db_utils.py recent 5

# Search by keyword
python db_utils.py keyword pesticide

# Search by date range
python db_utils.py date 2024-01-01 2024-12-31

# Export to JSON
python db_utils.py export

# Clear database (use with caution!)
python db_utils.py clear
```

### Testing Notifications

```bash
# Test all notification systems
python test_notifications.py
```

### Local Webhook Testing

```bash
# Start local webhook server
python test_webhook_server.py

# In another terminal, set EMAIL_WEBHOOK_URL=http://localhost:5000/webhook
# Then run the test script
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Keywords**: Terms to search for in comments
- **Page size**: Number of comments to check per run
- **Request delay**: Time between API requests
- **Database file**: SQLite database filename
- **Notification settings**: Teams and email webhook URLs

## 🔧 Key Features

### SQLite Database

- **Reliable storage**: ACID compliance and data integrity
- **Fast queries**: Indexed lookups for efficient searching
- **No duplicates**: Primary key constraints prevent duplicate entries
- **Rich metadata**: Stores full comment details and timestamps

### Webhook Notifications

- **Teams integration**: Rich message cards with direct links
- **Email support**: Plain text and HTML email formats
- **Configurable**: Enable/disable individual notification types
- **Error handling**: Graceful failure handling for webhook errors

### Duplicate Prevention

The system tracks previously seen comment IDs to avoid processing the same comment multiple times.

### Two-Stage Filtering

1. **Metadata scan**: Quick scan of titles and snippets
2. **Full text verification**: Double-check with complete comment content

### Advanced Querying

- Search by keyword
- Filter by date range
- Get statistics and analytics
- Export data to JSON

### Detailed Logging

- Shows each comment being processed
- Displays titles and IDs
- Tracks progress through each step
- Provides summary statistics

## 📊 Database Utilities

The `db_utils.py` script provides command-line tools for:

- **Statistics**: View database metrics and keyword counts
- **Searching**: Find comments by keyword or date range
- **Exporting**: Convert database data to JSON format
- **Management**: Clear database or view recent entries

## 🧪 Testing

### Test Notifications

```bash
# Test all notification systems
python test_notifications.py
```

### Local Webhook Testing

```bash
# Start local webhook server
python test_webhook_server.py

# In another terminal, set EMAIL_WEBHOOK_URL=http://localhost:5000/webhook
# Then run the test script
```

### Run Main Application

```bash
python main.py
```

Check database status:

```bash
python db_utils.py stats
```

## 📝 License

This project is open source and available under the MIT License.
