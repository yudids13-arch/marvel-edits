#!/usr/bin/env python3
"""
JARVIS - Advanced Offline AI Assistant
Your personal AI that can access information and make edits to your projects
Works completely offline with local knowledge base and file manipulation
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Dict, List, Any, Optional
import subprocess

# Local NLP capabilities
try:
    import spacy
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False
    print("⚠️ Install spacy: pip install spacy")
    print("⚠️ Download model: python -m spacy download en_core_web_sm")

class JarvisKnowledgeBase:
    """Local knowledge base for JARVIS"""
    
    def __init__(self, db_path: str = "jarvis_knowledge.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the knowledge database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge
                     (id INTEGER PRIMARY KEY, category TEXT, topic TEXT, content TEXT, timestamp DATETIME)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS edits
                     (id INTEGER PRIMARY KEY, file_path TEXT, action TEXT, content TEXT, timestamp DATETIME)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY, description TEXT, status TEXT, created_at DATETIME, completed_at DATETIME)''')
        
        conn.commit()
        conn.close()
    
    def add_knowledge(self, category: str, topic: str, content: str):
        """Add information to knowledge base"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO knowledge (category, topic, content, timestamp) VALUES (?, ?, ?, ?)",
                 (category, topic, content, datetime.now()))
        conn.commit()
        conn.close()
    
    def query_knowledge(self, query: str) -> List[Dict]:
        """Search knowledge base"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM knowledge WHERE topic LIKE ? OR content LIKE ?",
                 (f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()
        
        return [{"id": r[0], "category": r[1], "topic": r[2], "content": r[3]} for r in results]


class JarvisFileEditor:
    """Handle file editing operations"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Read file content"""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                return full_path.read_text()
            return None
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to file"""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            return True
        except Exception as e:
            print(f"Error writing file: {str(e)}")
            return False
    
    def append_file(self, file_path: str, content: str) -> bool:
        """Append content to file"""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'a') as f:
                f.write(content + "\n")
            return True
        except Exception as e:
            print(f"Error appending to file: {str(e)}")
            return False
    
    def create_file(self, file_path: str, content: str = "") -> bool:
        """Create new file"""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                return True
            return False
        except Exception as e:
            print(f"Error creating file: {str(e)}")
            return False
    
    def list_files(self, directory: str = ".") -> List[str]:
        """List files in directory"""
        try:
            target = self.base_path / directory
            if target.exists():
                return [str(p.relative_to(self.base_path)) for p in target.rglob("*") if p.is_file()]
            return []
        except Exception as e:
            print(f"Error listing files: {str(e)}")
            return []
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False


class JARVIS:
    """Main JARVIS AI Assistant"""
    
    def __init__(self, project_root: str = "."):
        self.knowledge_base = JarvisKnowledgeBase()
        self.file_editor = JarvisFileEditor(project_root)
        self.nlp = spacy.load("en_core_web_sm") if NLP_AVAILABLE else None
        self.conversation_history = []
        self.commands = {
            "read": self.cmd_read_file,
            "write": self.cmd_write_file,
            "create": self.cmd_create_file,
            "list": self.cmd_list_files,
            "delete": self.cmd_delete_file,
            "search": self.cmd_search_knowledge,
            "learn": self.cmd_learn,
            "help": self.cmd_help,
            "analyze": self.cmd_analyze_text,
            "summarize": self.cmd_summarize,
            "edit": self.cmd_edit_file,
        }
    
    def process_command(self, user_input: str) -> str:
        """Process user command and execute appropriate action"""
        user_input = user_input.strip()
        
        # Extract command
        parts = user_input.split(maxsplit=1)
        if not parts:
            return "Please provide a command. Type 'help' for available commands."
        
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            return self.commands[command](args)
        else:
            return self.process_natural_language(user_input)
    
    def cmd_read_file(self, args: str) -> str:
        """Read file command"""
        if not args:
            return "Usage: read <file_path>"
        content = self.file_editor.read_file(args)
        if content is None:
            return f"File not found: {args}"
        return f"📄 Content of {args}:\n\n{content}"
    
    def cmd_write_file(self, args: str) -> str:
        """Write to file - format: write <file_path> <content>"""
        if not args:
            return "Usage: write <file_path> <content>"
        
        parts = args.split(maxsplit=1)
        file_path = parts[0]
        content = parts[1] if len(parts) > 1 else ""
        
        if self.file_editor.write_file(file_path, content):
            return f"✅ Successfully wrote to {file_path}"
        return f"❌ Failed to write to {file_path}"
    
    def cmd_create_file(self, args: str) -> str:
        """Create file command"""
        if not args:
            return "Usage: create <file_path>"
        
        if self.file_editor.create_file(args):
            return f"✅ Created {args}"
        return f"❌ File already exists or error: {args}"
    
    def cmd_list_files(self, args: str) -> str:
        """List files in directory"""
        directory = args if args else "."
        files = self.file_editor.list_files(directory)
        if files:
            return f"📁 Files in {directory}:\n" + "\n".join(f"  • {f}" for f in files)
        return f"No files found in {directory}"
    
    def cmd_delete_file(self, args: str) -> str:
        """Delete file command"""
        if not args:
            return "Usage: delete <file_path>"
        
        if self.file_editor.delete_file(args):
            return f"✅ Deleted {args}"
        return f"❌ Failed to delete {args}"
    
    def cmd_edit_file(self, args: str) -> str:
        """Edit file - format: edit <file_path> <line_number> <new_content>"""
        if not args:
            return "Usage: edit <file_path> <line_number> <new_content>"
        
        parts = args.split(maxsplit=2)
        if len(parts) < 3:
            return "Usage: edit <file_path> <line_number> <new_content>"
        
        file_path, line_num, new_content = parts[0], int(parts[1]) - 1, parts[2]
        
        content = self.file_editor.read_file(file_path)
        if content is None:
            return f"File not found: {file_path}"
        
        lines = content.split('\n')
        if line_num < 0 or line_num >= len(lines):
            return f"Line number {line_num + 1} out of range"
        
        lines[line_num] = new_content
        updated_content = '\n'.join(lines)
        
        if self.file_editor.write_file(file_path, updated_content):
            return f"✅ Edited line {line_num + 1} in {file_path}"
        return f"❌ Failed to edit {file_path}"
    
    def cmd_search_knowledge(self, args: str) -> str:
        """Search knowledge base"""
        if not args:
            return "Usage: search <query>"
        
        results = self.knowledge_base.query_knowledge(args)
        if results:
            output = f"🔍 Found {len(results)} results for '{args}':\n"
            for r in results:
                output += f"\n📌 {r['topic']} ({r['category']})\n{r['content']}\n"
            return output
        return f"No results found for '{args}'"
    
    def cmd_learn(self, args: str) -> str:
        """Learn new information - format: learn <category> <topic> <content>"""
        if not args:
            return "Usage: learn <category> <topic> <content>"
        
        parts = args.split(maxsplit=2)
        if len(parts) < 3:
            return "Usage: learn <category> <topic> <content>"
        
        category, topic, content = parts[0], parts[1], parts[2]
        self.knowledge_base.add_knowledge(category, topic, content)
        return f"✅ Learned: {topic} in {category}"
    
    def cmd_analyze_text(self, args: str) -> str:
        """Analyze text using NLP"""
        if not args:
            return "Usage: analyze <text>"
        
        if not NLP_AVAILABLE:
            return "⚠️ NLP not available. Install spacy and download model."
        
        doc = self.nlp(args)
        analysis = {
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "tokens": [token.text for token in doc],
            "pos_tags": [(token.text, token.pos_) for token in doc],
        }
        
        return f"📊 Analysis:\n{json.dumps(analysis, indent=2)}"
    
    def cmd_summarize(self, args: str) -> str:
        """Summarize content"""
        if not args:
            return "Usage: summarize <text>"
        
        sentences = args.split('.')
        num_sentences = len([s for s in sentences if s.strip()])
        summary_length = max(1, num_sentences // 3)
        
        summary = '. '.join(sentences[:summary_length]).strip()
        return f"📝 Summary:\n{summary}..."
    
    def cmd_help(self, args: str) -> str:
        """Show available commands"""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║           JARVIS - AI Assistant Commands                  ║
╚════════════════════════════════════════════════════════════╝

📁 FILE OPERATIONS:
  read <file>              - Read file content
  write <file> <content>   - Write to file
  create <file>            - Create new file
  edit <file> <line> <content> - Edit specific line
  delete <file>            - Delete file
  list [directory]         - List files

🧠 KNOWLEDGE & ANALYSIS:
  search <query>           - Search knowledge base
  learn <cat> <topic> <content> - Add to knowledge base
  analyze <text>           - NLP analysis
  summarize <text>         - Summarize text

💡 OTHER:
  help                     - Show this help message

EXAMPLES:
  read README.md
  write config.json {"api": "enabled"}
  search Marvel movies
  analyze The quick brown fox
"""
        return help_text
    
    def process_natural_language(self, text: str) -> str:
        """Process natural language queries"""
        text_lower = text.lower()
        
        # Intent detection
        if any(word in text_lower for word in ["what", "how", "when", "where", "why"]):
            results = self.knowledge_base.query_knowledge(text)
            if results:
                return f"From my knowledge: {results[0]['content']}"
            return "I don't have information about that yet. Try using 'learn' to teach me."
        
        if any(word in text_lower for word in ["create", "make", "generate"]):
            return "I can help create files. Use: create <file_path>"
        
        if any(word in text_lower for word in ["read", "show", "display"]):
            return "Use the 'read' command to view files: read <file_path>"
        
        return f"🤔 I'm processing: '{text}'\nTry using a specific command or type 'help' for options."
    
    def start_interactive(self):
        """Start interactive mode"""
        print("\n" + "="*60)
        print("JARVIS - Your Personal Offline AI Assistant")
        print("="*60)
        print("Type 'help' for available commands or start typing...")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("JARVIS> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("JARVIS: Shutting down. Goodbye, Sir/Madam.")
                    break
                
                response = self.process_command(user_input)
                print(f"\nJARVIS: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nJARVIS: Interrupted. Type 'exit' to quit properly.")
            except Exception as e:
                print(f"\nJARVIS: Error - {str(e)}\n")


def main():
    """Main entry point"""
    jarvis = JARVIS(project_root=".")
    jarvis.start_interactive()


if __name__ == "__main__":
    main()
