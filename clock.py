#!/usr/bin/env python3
"""
Digital Clock with Multiple Time Zones
Displays current time in different time zones with real-time updates
"""

import datetime
import pytz
from typing import List, Dict
import os
import sys

class DigitalClock:
    """Advanced digital clock with timezone support"""
    
    def __init__(self):
        self.timezones = {
            'New York': 'America/New_York',
            'London': 'Europe/London',
            'Tokyo': 'Asia/Tokyo',
            'Sydney': 'Australia/Sydney',
            'Dubai': 'Asia/Dubai',
            'Singapore': 'Asia/Singapore',
            'Hong Kong': 'Asia/Hong_Kong',
            'São Paulo': 'America/Sao_Paulo',
            'Moscow': 'Europe/Moscow',
            'Istanbul': 'Europe/Istanbul',
            'Bangkok': 'Asia/Bangkok',
            'Mexico City': 'America/Mexico_City',
            'Los Angeles': 'America/Los_Angeles',
            'Berlin': 'Europe/Berlin',
            'Paris': 'Europe/Paris',
            'Delhi': 'Asia/Kolkata',
            'Auckland': 'Pacific/Auckland',
            'Honolulu': 'Pacific/Honolulu',
            'Toronto': 'America/Toronto',
        }
        self.custom_timezones = {}
    
    def add_timezone(self, city: str, timezone: str) -> bool:
        """Add custom timezone"""
        try:
            pytz.timezone(timezone)
            self.custom_timezones[city] = timezone
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    def get_time(self, timezone: str) -> datetime.datetime:
        """Get current time in specific timezone"""
        tz = pytz.timezone(timezone)
        return datetime.datetime.now(tz)
    
    def format_time_12h(self, dt: datetime.datetime) -> str:
        """Format time in 12-hour format"""
        return dt.strftime('%I:%M:%S %p')
    
    def format_time_24h(self, dt: datetime.datetime) -> str:
        """Format time in 24-hour format"""
        return dt.strftime('%H:%M:%S')
    
    def get_all_times(self, format_24h: bool = False) -> Dict[str, Dict]:
        """Get current time in all configured timezones"""
        times = {}
        all_zones = {**self.timezones, **self.custom_timezones}
        
        for city, timezone in all_zones.items():
            try:
                dt = self.get_time(timezone)
                format_func = self.format_time_24h if format_24h else self.format_time_12h
                times[city] = {
                    'time': format_func(dt),
                    'timezone': timezone,
                    'date': dt.strftime('%A, %B %d, %Y'),
                    'utc_offset': dt.strftime('%z'),
                    'dst': 'Yes' if bool(dt.dst()) else 'No'
                }
            except Exception as e:
                times[city] = {'error': str(e)}
        
        return times
    
    def get_time_for_city(self, city: str, format_24h: bool = False) -> Dict:
        """Get time for specific city"""
        all_zones = {**self.timezones, **self.custom_timezones}
        
        if city not in all_zones:
            return {'error': f'City {city} not found'}
        
        try:
            timezone = all_zones[city]
            dt = self.get_time(timezone)
            format_func = self.format_time_24h if format_24h else self.format_time_12h
            
            return {
                'city': city,
                'time': format_func(dt),
                'timezone': timezone,
                'date': dt.strftime('%A, %B %d, %Y'),
                'utc_offset': dt.strftime('%z'),
                'dst': 'Yes' if bool(dt.dst()) else 'No',
                'hour': dt.hour,
                'minute': dt.minute,
                'second': dt.second,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_available_timezones(self) -> List[str]:
        """List all available timezones"""
        return sorted(list(self.timezones.keys()) + list(self.custom_timezones.keys()))
    
    def get_utc_time(self) -> datetime.datetime:
        """Get current UTC time"""
        return datetime.datetime.now(pytz.UTC)
    
    def time_difference(self, city1: str, city2: str) -> Dict:
        """Calculate time difference between two cities"""
        all_zones = {**self.timezones, **self.custom_timezones}
        
        if city1 not in all_zones or city2 not in all_zones:
            return {'error': 'One or both cities not found'}
        
        try:
            dt1 = self.get_time(all_zones[city1])
            dt2 = self.get_time(all_zones[city2])
            
            diff = dt2 - dt1
            hours = diff.total_seconds() // 3600
            minutes = (diff.total_seconds() % 3600) // 60
            
            return {
                'city1': city1,
                'city2': city2,
                'difference': f'{int(hours)} hours {int(minutes)} minutes',
                'city2_ahead': hours > 0,
                'raw_hours': hours,
                'raw_minutes': minutes
            }
        except Exception as e:
            return {'error': str(e)}


class CLIClock:
    """Command-line interface for the digital clock"""
    
    def __init__(self):
        self.clock = DigitalClock()
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def display_banner(self):
        """Display welcome banner"""
        print("\n" + "="*70)
        print("🕐 DIGITAL CLOCK - MULTIPLE TIME ZONES".center(70))
        print("="*70 + "\n")
    
    def display_all_times(self, format_24h: bool = False):
        """Display times for all cities"""
        self.clear_screen()
        self.display_banner()
        
        times = self.clock.get_all_times(format_24h)
        
        print(f"{'City':<20} {'Time':<15} {'Date':<25} {'UTC Offset':<12} {'DST':<5}")
        print("-" * 80)
        
        for city in sorted(times.keys()):
            data = times[city]
            if 'error' not in data:
                print(f"{city:<20} {data['time']:<15} {data['date']:<25} {data['utc_offset']:<12} {data['dst']:<5}")
        
        print()
    
    def display_single_city(self, city: str, format_24h: bool = False):
        """Display large clock for single city"""
        self.clear_screen()
        self.display_banner()
        
        data = self.clock.get_time_for_city(city, format_24h)
        
        if 'error' in data:
            print(f"❌ Error: {data['error']}")
            return
        
        # Large ASCII display
        print(f"\n📍 {data['city']}")
        print(f"🌍 Timezone: {data['timezone']}")
        print(f"📅 Date: {data['date']}")
        print(f"🕐 UTC Offset: {data['utc_offset']}")
        print(f"🔄 DST Active: {data['dst']}")
        print()
        
        # Large time display
        time_str = data['time']
        print("┌" + "─" * 40 + "┐")
        print(f"│{time_str.center(40)}│")
        print("└" + "─" * 40 + "┘")
        print()
    
    def display_comparison(self, city1: str, city2: str):
        """Display time comparison between two cities"""
        self.clear_screen()
        self.display_banner()
        
        data1 = self.clock.get_time_for_city(city1)
        data2 = self.clock.get_time_for_city(city2)
        diff = self.clock.time_difference(city1, city2)
        
        if 'error' in data1 or 'error' in data2:
            print("❌ Error: One or both cities not found")
            return
        
        print(f"\n📍 {city1:<20} vs  {city2:<20}")
        print("-" * 50)
        print(f"🕐 {data1['time']:<20}    {data2['time']:<20}")
        print(f"📅 {data1['date']:<20}    {data2['date']:<20}")
        print()
        
        if 'error' not in diff:
            ahead = "is ahead" if diff['city2_ahead'] else "is behind"
            print(f"⏱️  {diff['city2']} {ahead} by {diff['difference']}")
        print()
    
    def display_help(self):
        """Display help menu"""
        self.clear_screen()
        self.display_banner()
        
        help_text = """
╔════════════════════════════════════════════════════════════╗
║              AVAILABLE COMMANDS                           ║
╚════════════════════════════════════════════════════════════╝

⏱️  TIME DISPLAY:
  all                - Show all timezones
  <city>             - Show clock for specific city
  compare <c1> <c2>  - Compare time between two cities
  24h                - Toggle 24-hour format
  12h                - Toggle 12-hour format

🌍 TIMEZONE MANAGEMENT:
  list               - List all available cities
  add <city> <tz>    - Add custom timezone
                      (e.g., add Istanbul Europe/Istanbul)
  utc                - Show UTC time
  diff <c1> <c2>     - Show time difference between cities

📋 INFORMATION:
  help               - Show this help
  about              - About this application
  exit               - Quit program

"""
        print(help_text)
    
    def display_about(self):
        """Display about information"""
        self.clear_screen()
        self.display_banner()
        
        about_text = """
🕐 DIGITAL CLOCK - MULTIPLE TIME ZONES

A sophisticated clock application that displays current time
across different time zones around the world.

FEATURES:
✨ Real-time updates
✨ 20+ preset timezones
✨ 12 and 24-hour formats
✨ Custom timezone support
✨ Time zone comparisons
✨ DST detection
✨ Intuitive CLI interface

VERSION: 1.0.0
AUTHOR: JARVIS

"""
        print(about_text)
    
    def run(self):
        """Start interactive mode"""
        format_24h = False
        
        while True:
            try:
                user_input = input("\n🕐 Clock> ").strip().lower()
                
                if not user_input:
                    continue
                
                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'exit':
                    print("\n👋 Goodbye!\n")
                    break
                
                elif command == 'all':
                    self.display_all_times(format_24h)
                
                elif command == '24h':
                    format_24h = True
                    print("✅ Switched to 24-hour format")
                
                elif command == '12h':
                    format_24h = False
                    print("✅ Switched to 12-hour format")
                
                elif command == 'list':
                    self.clear_screen()
                    self.display_banner()
                    cities = self.clock.list_available_timezones()
                    print(f"📍 Available Cities ({len(cities)}):")
                    print("\n".join(f"  • {city}" for city in cities))
                    print()
                
                elif command == 'utc':
                    utc_time = self.clock.get_utc_time()
                    print(f"\n🌍 UTC Time: {utc_time.strftime('%H:%M:%S - %B %d, %Y')}")
                
                elif command == 'help':
                    self.display_help()
                
                elif command == 'about':
                    self.display_about()
                
                elif command == 'compare':
                    if not args:
                        print("Usage: compare <city1> <city2>")
                        continue
                    cities = args.split()
                    if len(cities) >= 2:
                        self.display_comparison(cities[0], cities[1])
                    else:
                        print("Usage: compare <city1> <city2>")
                
                elif command == 'diff':
                    if not args:
                        print("Usage: diff <city1> <city2>")
                        continue
                    cities = args.split()
                    if len(cities) >= 2:
                        diff = self.clock.time_difference(cities[0], cities[1])
                        if 'error' not in diff:
                            print(f"\n⏱️  {diff['city2']} is {'ahead' if diff['city2_ahead'] else 'behind'} by {diff['difference']}")
                        else:
                            print(f"❌ Error: {diff['error']}")
                    else:
                        print("Usage: diff <city1> <city2>")
                
                elif command == 'add':
                    if not args:
                        print("Usage: add <city> <timezone>")
                        continue
                    parts_add = args.split(maxsplit=1)
                    if len(parts_add) >= 2:
                        city, tz = parts_add[0], parts_add[1]
                        if self.clock.add_timezone(city, tz):
                            print(f"✅ Added {city} ({tz})")
                        else:
                            print(f"❌ Invalid timezone: {tz}")
                    else:
                        print("Usage: add <city> <timezone>")
                
                else:
                    # Assume it's a city name
                    self.display_single_city(command, format_24h)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def main():
    """Main entry point"""
    cli = CLIClock()
    cli.clear_screen()
    cli.display_banner()
    print("Type 'help' for commands or 'all' to see all time zones\n")
    cli.run()


if __name__ == "__main__":
    main()
