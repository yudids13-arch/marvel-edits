# 🤖 JARVIS - Your Personal Offline AI Assistant

A powerful, offline-first AI assistant inspired by JARVIS from Marvel. Create files, manage your project, search your knowledge base, and interact with advanced NLP capabilities—all without leaving your local machine.

## Features

✨ **Core Capabilities:**
- 📁 **File Management** - Read, write, create, edit, and delete files
- 🧠 **Knowledge Base** - Build and search your personal knowledge database
- 🔍 **NLP Analysis** - Entity recognition, tokenization, text analysis
- 📝 **Text Summarization** - Quick summaries of content
- 💾 **Offline-First** - Works completely offline with local SQLite database
- 🌐 **Web Interface** - Beautiful modern dashboard
- 🎮 **CLI Mode** - Command-line interface for quick operations

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run JARVIS**

   **Option A: CLI Mode (Interactive)**
   ```bash
   python jarvis.py
   ```

   **Option B: Web Interface**
   ```bash
   python web_interface.py
   ```
   Then open http://localhost:5000 in your browser

## Usage

### Command Structure

**File Operations:**
```bash
read <file_path>                    # Read file content
write <file_path> <content>        # Write to file
create <file_path>                 # Create new file
edit <file_path> <line> <content>  # Edit specific line
delete <file_path>                 # Delete file
list [directory]                   # List files in directory
```

**Knowledge Management:**
```bash
search <query>                     # Search knowledge base
learn <category> <topic> <content> # Add to knowledge base
analyze <text>                     # NLP analysis
summarize <text>                   # Summarize content
```

**System:**
```bash
help                               # Show all commands
exit                              # Quit JARVIS
```

### Examples

```bash
# File operations
JARVIS> read config.json
JARVIS> create my_project/index.py
JARVIS> write my_project/data.txt Important information here
JARVIS> list my_project
JARVIS> edit my_project/data.txt 1 Updated information

# Knowledge base
JARVIS> learn Marvel Ironman Tony Stark is a genius inventor
JARVIS> search Ironman
JARVIS> search Tony Stark

# Analysis
JARVIS> analyze The quick brown fox jumps over the lazy dog
JARVIS> summarize This is a long text that needs to be summarized into shorter form
```

## Project Structure

```
.
├── jarvis.py              # Main JARVIS engine
├── web_interface.py       # Flask web server
├── requirements.txt       # Python dependencies
├── jarvis_knowledge.db    # SQLite knowledge base (auto-created)
├── templates/
│   └── dashboard.html     # Web interface HTML
└── static/
    ├── style.css          # Web interface styles
    └── script.js          # Web interface scripts
```

## Database Schema

### Knowledge Table
```sql
CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY,
    category TEXT,
    topic TEXT,
    content TEXT,
    timestamp DATETIME
);
```

### Edit History Table
```sql
CREATE TABLE edits (
    id INTEGER PRIMARY KEY,
    file_path TEXT,
    action TEXT,
    content TEXT,
    timestamp DATETIME
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    description TEXT,
    status TEXT,
    created_at DATETIME,
    completed_at DATETIME
);
```

## API Endpoints (Web Interface)

- `POST /api/chat` - Send message to JARVIS
- `GET /api/commands` - Get available commands
- `GET /api/history` - Get conversation history
- `GET /api/knowledge` - Get knowledge base stats
- `GET /api/system/info` - Get system information

## Advanced Features

### Natural Language Processing
- Entity recognition (people, places, organizations)
- Part-of-speech tagging
- Token analysis
- Named entity linking

### Knowledge Base
- Categorized information storage
- Full-text search
- Timestamp tracking
- Easy retrieval and expansion

### File Management
- Read/write operations
- Line-by-line editing
- Directory listing
- Recursive file operations

## Configuration

Edit `jarvis.py` to customize:
- Database location
- Project root directory
- NLP model
- Command set

## Limitations

- NLP features require spacy and language model download
- Web interface requires Flask
- File operations limited to project directory
- No internet connectivity required (fully offline)

## Future Enhancements

- [ ] Voice input/output
- [ ] Task scheduling
- [ ] Git integration
- [ ] Machine learning model training
- [ ] Smart recommendations
- [ ] Multi-language support
- [ ] Cloud sync (optional)
- [ ] Plugin system

## Troubleshooting

**Q: spacy model not found**
A: Run `python -m spacy download en_core_web_sm`

**Q: Flask not found**
A: Run `pip install Flask Flask-CORS`

**Q: File operations not working**
A: Check that files are in the project directory and you have proper permissions

**Q: Web interface not loading**
A: Make sure port 5000 is not in use: `netstat -ano | findstr :5000` (Windows) or `lsof -i :5000` (Mac/Linux)

## License

MIT License - Free to use and modify

## Disclaimer

This is an educational project inspired by JARVIS from Marvel. It operates completely offline and locally. No data is sent to external servers.

---

**Ready to work with your AI assistant?** Start with `python jarvis.py` and type `help` for a list of commands!
