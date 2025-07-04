# Comment Watcher

A modular Python application for monitoring regulations.gov comments for specific keywords.

## 🏗️ Architecture

The application is built with separated concerns:

- **`config.py`** - Configuration management and environment variables
- **`api_client.py`** - HTTP client for regulations.gov API
- **`comment_analyzer.py`** - Keyword matching and comment processing
- **`data_storage.py`** - JSON file storage for flagged comments
- **`notifier.py`** - Alert formatting and output
- **`comment_watcher.py`** - Main orchestrator class
- **`main.py`** - Simple entry point

## 🚀 Quick Start

1. **Install dependencies:**

   ```bash
   pip install requests python-dotenv
   ```

2. **Set up your API key:**
   Create a `.env` file:

   ```
   API_KEY=your_regulations_gov_api_key_here
   ```

3. **Run the watcher:**
   ```bash
   python main.py
   ```

## 📖 Usage Examples

### Basic Usage

```python
from comment_watcher import CommentWatcher

watcher = CommentWatcher()
results = watcher.run_monitoring_cycle()
```

### Custom Keywords

```python
from comment_watcher import CommentWatcher
from comment_analyzer import CommentAnalyzer

# Create custom analyzer with different keywords
analyzer = CommentAnalyzer(keywords=["climate", "emissions", "carbon"])
watcher = CommentWatcher()
watcher.analyzer = analyzer

results = watcher.run_monitoring_cycle(page_size=50)
```

### View Historical Data

```python
watcher = CommentWatcher()
historical = watcher.get_historical_data()
print(f"Found {len(historical)} historical flagged comments")
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Keywords**: Terms to search for in comments
- **Page size**: Number of comments to check per run
- **Request delay**: Time between API requests
- **Output file**: Where to save flagged comments

## 🔧 Customization

### Adding New Keywords

```python
# In config.py
KEYWORDS = ["pesticide", "glyphosate", "worker safety", "your_new_keyword"]
```

### Custom Alert Format

```python
# Extend the Notifier class in notifier.py
class CustomNotifier(Notifier):
    def send_alert(self, comments):
        # Your custom alert logic
        pass
```

### Different Storage Backend

```python
# Extend the DataStorage class in data_storage.py
class DatabaseStorage(DataStorage):
    def save_flagged_comments(self, comments):
        # Save to database instead of JSON
        pass
```

## 📊 Output

The application provides:

- Real-time alerts for keyword matches
- Detailed comment information (title, date, submitter, etc.)
- Summary statistics
- Persistent storage of flagged comments

## 🧪 Testing

Run the example script to see different configurations:

```bash
python example_usage.py
```

## 📝 License

This project is open source and available under the MIT License.
