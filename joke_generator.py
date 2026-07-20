#!/usr/bin/env python3
"""
Random Joke Generator - CLI Version
Fetches jokes from external APIs
"""

import requests
import json
from typing import Dict, List, Optional
import random

class JokeGenerator:
    """Generate random jokes from multiple sources"""
    
    def __init__(self):
        self.apis = {
            'official': 'https://official-joke-api.appspot.com/random_joke',
            'dad_jokes': 'https://icanhazdadjoke.com/?format=json',
            'advice': 'https://api.adviceslip.com/advice',
        }
        self.timeout = 5
    
    def fetch_joke(self, source: str = 'official') -> Optional[Dict]:
        """Fetch a random joke from specified API"""
        if source not in self.apis:
            return self._fetch_from_all()
        
        try:
            url = self.apis[source]
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Parse based on source
            if source == 'official':
                return {
                    'type': 'joke',
                    'category': data.get('type', 'General'),
                    'setup': data.get('setup', ''),
                    'punchline': data.get('punchline', ''),
                    'full': f"{data.get('setup', '')}\\n{data.get('punchline', '')}",
                    'source': 'Official Joke API'
                }
            elif source == 'dad_jokes':
                return {
                    'type': 'joke',
                    'category': 'Dad Joke',
                    'setup': '',
                    'punchline': data.get('joke', ''),
                    'full': data.get('joke', ''),
                    'source': 'iCanHazDadJoke'
                }
            elif source == 'advice':
                return {
                    'type': 'advice',
                    'full': data.get('slip', {}).get('advice', ''),
                    'source': 'Advice Slip API'
                }
        except requests.exceptions.RequestException as e:
            return {'error': f'Failed to fetch from {source}: {str(e)}'}
    
    def _fetch_from_all(self) -> Optional[Dict]:
        """Fetch from random available source"""
        available = list(self.apis.keys())
        random.shuffle(available)
        
        for source in available:
            result = self.fetch_joke(source)
            if result and 'error' not in result:
                return result
        
        return {'error': 'All APIs failed'}
    
    def get_multiple_jokes(self, count: int = 5) -> List[Dict]:
        """Get multiple jokes from different sources"""
        jokes = []
        sources = list(self.apis.keys())
        
        for i in range(count):
            source = sources[i % len(sources)]
            joke = self.fetch_joke(source)
            if joke and 'error' not in joke:
                jokes.append(joke)
        
        return jokes
    
    def format_joke(self, joke: Dict) -> str:
        """Format joke for display"""
        if 'error' in joke:
            return f"❌ {joke['error']}"
        
        output = ""
        
        if 'category' in joke:
            output += f"📂 Category: {joke['category']}\\n"
        
        if joke.get('setup'):
            output += f"❓ {joke['setup']}\\n"
            output += f"💡 {joke['punchline']}\\n"
        else:
            output += f"{joke['full']}\\n"
        
        output += f"\\n📌 Source: {joke.get('source', 'Unknown')}\\n"
        
        return output


class JokeApp:
    """CLI application for joke generator"""
    
    def __init__(self):
        self.generator = JokeGenerator()
    
    def clear_screen(self):
        import os
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def display_banner(self):
        """Display welcome banner"""
        print("\\n" + "="*60)
        print("😂 RANDOM JOKE GENERATOR".center(60))
        print("="*60 + "\\n")
    
    def display_joke(self, joke: Dict):
        """Display formatted joke"""
        self.clear_screen()
        self.display_banner()
        print(self.generator.format_joke(joke))
    
    def display_multiple(self, count: int = 5):
        """Display multiple jokes"""
        self.clear_screen()
        self.display_banner()
        
        jokes = self.generator.get_multiple_jokes(count)
        
        for i, joke in enumerate(jokes, 1):
            print(f"\\n{'='*60}")
            print(f"Joke #{i}")
            print(f"{'='*60}")
            print(self.generator.format_joke(joke))
    
    def display_help(self):
        """Display help menu"""
        self.clear_screen()
        self.display_banner()
        
        help_text = """
╔════════════════════════════════════════════════════════════╗
║              AVAILABLE COMMANDS                           ║
╚════════════════════════════════════════════════════════════╝

😂 JOKE OPERATIONS:
  random               - Get a random joke
  official             - Get joke from Official API
  dad                  - Get a dad joke
  advice               - Get life advice
  multiple [count]     - Get multiple jokes (default: 5)
  <number>             - Get that many jokes

📋 INFORMATION:
  help                 - Show this help
  about                - About this application
  exit                 - Quit program

EXAMPLES:
  random               # Get a random joke
  dad                  # Get a dad joke
  multiple 10          # Get 10 jokes
  3                    # Get 3 jokes

"""
        print(help_text)
    
    def display_about(self):
        """Display about information"""
        self.clear_screen()
        self.display_banner()
        
        about_text = """
😂 RANDOM JOKE GENERATOR

A fun application that fetches random jokes
from multiple external APIs.

AVAILABLE SOURCES:
✨ Official Joke API - Professional jokes
✨ iCanHazDadJoke - Classic dad jokes
✨ Advice Slip - Random life advice

FEATURES:
✨ Multiple API sources
✨ Automatic failover
✨ Multiple joke formats
✨ Batch retrieval
✨ Intuitive CLI interface

VERSION: 1.0.0
AUTHOR: JARVIS

"""
        print(about_text)
    
    def run(self):
        """Start interactive mode"""
        self.clear_screen()
        self.display_banner()
        print("Type 'help' for commands or 'random' for a joke\\n")
        
        while True:
            try:
                user_input = input("😂 Joke> ").strip().lower()
                
                if not user_input:
                    continue
                
                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'exit':
                    print("\\n👋 Thanks for the laughs! Goodbye!\\n")
                    break
                
                elif command == 'help':
                    self.display_help()
                
                elif command == 'about':
                    self.display_about()
                
                elif command == 'random':
                    joke = self.generator._fetch_from_all()
                    self.display_joke(joke)
                
                elif command == 'official':
                    joke = self.generator.fetch_joke('official')
                    self.display_joke(joke)
                
                elif command == 'dad':
                    joke = self.generator.fetch_joke('dad_jokes')
                    self.display_joke(joke)
                
                elif command == 'advice':
                    joke = self.generator.fetch_joke('advice')
                    self.display_joke(joke)
                
                elif command == 'multiple':
                    count = int(args) if args and args.isdigit() else 5
                    self.display_multiple(count)
                
                elif command.isdigit():
                    count = int(command)
                    self.display_multiple(count)
                
                else:
                    print(f"❓ Unknown command: {command}. Type 'help' for options.")
            
            except KeyboardInterrupt:
                print("\\n\\n👋 Thanks for the laughs! Goodbye!\\n")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def main():
    """Main entry point"""
    app = JokeApp()
    app.run()


if __name__ == "__main__":
    main()
