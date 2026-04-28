"""
Database Manager - SQLite Database Operations
"""

import sqlite3
import datetime
import hashlib
import random
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

# Import models
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.visitor import Visitor
from models.ticket import Ticket
from models.ticket_type import TicketType
from models.visit import Visit


class DatabaseError(Exception):
    """Database operation error"""
    pass


class DatabaseManager:
    """Professional database manager for museum system"""
    
    def __init__(self, db_path: str = "museum.db"):
        self.db_path = db_path
        self._initialize_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        finally:
            if conn:
                conn.close()
    
    def _initialize_database(self):
        """Initialize database with schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_number TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS ticket_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT UNIQUE NOT NULL,
                    visitor_id INTEGER NOT NULL,
                    ticket_type_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    sale_time TEXT NOT NULL,
                    status TEXT DEFAULT 'purchased',
                    remaining_uses INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (visitor_id) REFERENCES visitors (id),
                    FOREIGN KEY (ticket_type_id) REFERENCES ticket_types (id)
                );
                
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id INTEGER NOT NULL,
                    entry_time TEXT NOT NULL,
                    exit_time TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticket_id) REFERENCES tickets (id)
                );
                
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    description TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_tickets_ticket_id ON tickets(ticket_id);
                CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
                CREATE INDEX IF NOT EXISTS idx_visits_entry_time ON visits(entry_time);
                CREATE INDEX IF NOT EXISTS idx_visitors_id_number ON visitors(id_number);
            """)
            
            # Insert default data
            default_ticket_types = [
                ("Senior", 10.0, "Senior citizen ticket (age 60+)"),
                ("Child", 5.0, "Child ticket (age 3-12)"),
                ("Adult", 30.0, "Adult ticket (age 13-59)"),
                ("Student", 15.0, "Student ticket with valid ID"),
                ("Free", 0.0, "Free admission (age under 3 or over 80)")
            ]
            
            for name, price, desc in default_ticket_types:
                cursor.execute("""
                    INSERT OR IGNORE INTO ticket_types (name, price, description) 
                    VALUES (?, ?, ?)
                """, (name, price, desc))
            
            default_config = [
                ("max_capacity", "10", "Maximum number of visitors allowed"),
                ("ticketing_start_time", "09:00", "Ticket sales start time"),
                ("ticketing_end_time", "17:00", "Ticket sales end time"),
                ("ticket_usage_count", "1", "Number of times a ticket can be used")
            ]
            
            for key, value, desc in default_config:
                cursor.execute("""
                    INSERT OR IGNORE INTO config (key, value, description) 
                    VALUES (?, ?, ?)
                """, (key, value, desc))
            
            conn.commit()
    
    # Visitor operations
    def create_visitor(self, visitor: Visitor) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visitors (id_number, name, gender, date_of_birth, phone, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (visitor.id_number, visitor.name, visitor.gender, 
                  visitor.date_of_birth, visitor.phone, visitor.email))
            conn.commit()
            return cursor.lastrowid
    
    def get_visitor_by_id_number(self, id_number: str) -> Optional[Visitor]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM visitors WHERE id_number = ?", (id_number,))
            row = cursor.fetchone()
            if row:
                return Visitor(**dict(row))
            return None
    
    # Ticket type operations
    def get_all_ticket_types(self, include_inactive: bool = False) -> List[TicketType]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if include_inactive:
                cursor.execute("SELECT * FROM ticket_types ORDER BY price")
            else:
                cursor.execute("SELECT * FROM ticket_types WHERE is_active = 1 ORDER BY price")
            rows = cursor.fetchall()
            return [TicketType(**dict(row)) for row in rows]
    
    def get_ticket_type_by_name(self, name: str) -> Optional[TicketType]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ticket_types WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return TicketType(**dict(row))
            return None
    
    # Ticket operations
    def generate_ticket_id(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        random_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:6]
        return f"TKT{timestamp}{random_suffix}".upper()
    
    def create_ticket(self, ticket: Ticket) -> int:
        if not ticket.ticket_id:
            ticket.ticket_id = self.generate_ticket_id()
        if not ticket.sale_time:
            ticket.sale_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tickets (ticket_id, visitor_id, ticket_type_id, price, sale_time, status, remaining_uses)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ticket.ticket_id, ticket.visitor_id, ticket.ticket_type_id,
                  ticket.price, ticket.sale_time, ticket.status, ticket.remaining_uses))
            conn.commit()
            return cursor.lastrowid
    
    def get_ticket_by_id(self, ticket_id: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.*, tt.name as ticket_type_name, tt.price as original_price,
                       v.name as visitor_name, v.id_number as visitor_id_number
                FROM tickets t
                LEFT JOIN ticket_types tt ON t.ticket_type_id = tt.id
                LEFT JOIN visitors v ON t.visitor_id = v.id
                WHERE t.ticket_id = ?
            """, (ticket_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_ticket_status(self, ticket_id: str, status: str, remaining_uses: int = None) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if remaining_uses is not None:
                cursor.execute("""
                    UPDATE tickets SET status = ?, remaining_uses = ? WHERE ticket_id = ?
                """, (status, remaining_uses, ticket_id))
            else:
                cursor.execute("""
                    UPDATE tickets SET status = ? WHERE ticket_id = ?
                """, (status, ticket_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def validate_ticket(self, ticket_id: str) -> Dict:
        ticket = self.get_ticket_by_id(ticket_id)
        
        if not ticket:
            return {"valid": False, "reason": "Ticket not found"}
        
        if ticket['status'] == 'cancelled':
            return {"valid": False, "reason": "Ticket has been cancelled"}
        
        if ticket['status'] == 'expired':
            return {"valid": False, "reason": "Ticket has expired"}
        
        if ticket['remaining_uses'] <= 0:
            return {"valid": False, "reason": "No remaining uses for this ticket"}
        
        return {"valid": True, "ticket": ticket}
    
    # Visit operations
    def get_active_visits_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM visits WHERE exit_time IS NULL")
            return cursor.fetchone()[0]
    
    def get_active_visitors(self) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.name, v.id_number, t.ticket_id, vi.entry_time
                FROM visits vi
                JOIN tickets t ON vi.ticket_id = t.id
                JOIN visitors v ON t.visitor_id = v.id
                WHERE vi.exit_time IS NULL
                ORDER BY vi.entry_time
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def record_entry(self, ticket_id: int) -> bool:
        entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visits (ticket_id, entry_time)
                VALUES (?, ?)
            """, (ticket_id, entry_time))
            
            # Update ticket remaining uses
            cursor.execute("""
                UPDATE tickets 
                SET remaining_uses = remaining_uses - 1,
                    status = CASE WHEN remaining_uses - 1 <= 0 THEN 'used' ELSE 'visiting' END
                WHERE id = ?
            """, (ticket_id,))
            
            conn.commit()
            return True
    
    def record_exit(self, ticket_id: int) -> bool:
        exit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE visits SET exit_time = ?
                WHERE ticket_id = ? AND exit_time IS NULL
            """, (exit_time, ticket_id))
            
            # Update ticket status to 'left' if all uses are done
            cursor.execute("""
                UPDATE tickets 
                SET status = 'left'
                WHERE id = ? AND status = 'visiting' AND remaining_uses >= 0
            """, (ticket_id,))
            
            conn.commit()
            return True
    
    # Configuration
    def get_config_value(self, key: str) -> Optional[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None
    
    def set_config_value(self, key: str, value: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO config (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
            conn.commit()
            return True
    
    # Statistics
    def get_total_statistics(self) -> Dict:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM visitors")
            total_visitors = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tickets")
            total_tickets = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(price) FROM tickets WHERE status != 'cancelled'")
            total_revenue = cursor.fetchone()[0] or 0
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM tickets WHERE DATE(sale_time) = ?", (today,))
            today_tickets = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(price) FROM tickets WHERE DATE(sale_time) = ?", (today,))
            today_revenue = cursor.fetchone()[0] or 0
            
            cursor.execute("""
                SELECT COUNT(DISTINCT v.id) 
                FROM visits vi
                JOIN tickets t ON vi.ticket_id = t.id
                JOIN visitors v ON t.visitor_id = v.id
                WHERE DATE(vi.entry_time) = ?
            """, (today,))
            today_visitors = cursor.fetchone()[0]
            
            active_visitors = self.get_active_visits_count()
            
            return {
                "total_visitors": total_visitors,
                "total_tickets_sold": total_tickets,
                "total_revenue": total_revenue,
                "today_tickets_sold": today_tickets,
                "today_revenue": today_revenue,
                "today_visitors": today_visitors,
                "active_visitors": active_visitors
            }
    
    # Report methods
    def get_daily_sales_report(self, date: str = None) -> List[Dict]:
        """Get daily sales report"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    tt.name as ticket_type, 
                    COUNT(*) as count, 
                    SUM(t.price) as revenue
                FROM tickets t
                JOIN ticket_types tt ON t.ticket_type_id = tt.id
                WHERE DATE(t.sale_time) = ?
                GROUP BY tt.name
                ORDER BY revenue DESC
            """, (date,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_daily_visitor_report(self, date: str = None) -> Dict:
        """Get daily visitor statistics"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Total entries on the day
            cursor.execute("""
                SELECT COUNT(*) FROM visits 
                WHERE DATE(entry_time) = ?
            """, (date,))
            total_entries = cursor.fetchone()[0]
            
            # Total exits on the day
            cursor.execute("""
                SELECT COUNT(*) FROM visits 
                WHERE DATE(exit_time) = ?
            """, (date,))
            total_exits = cursor.fetchone()[0]
            
            # Average visit duration
            cursor.execute("""
                SELECT AVG((JULIANDAY(exit_time) - JULIANDAY(entry_time)) * 24 * 60)
                FROM visits 
                WHERE DATE(entry_time) = ? AND exit_time IS NOT NULL
            """, (date,))
            avg_duration = cursor.fetchone()[0]
            
            return {
                "date": date,
                "total_entries": total_entries,
                "total_exits": total_exits,
                "average_duration_minutes": round(avg_duration, 2) if avg_duration else 0
            }
    
    def get_top_ticket_types(self, limit: int = 5) -> List[Dict]:
        """Get top selling ticket types"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    tt.name,
                    COUNT(t.id) as tickets_sold,
                    SUM(t.price) as revenue
                FROM tickets t
                JOIN ticket_types tt ON t.ticket_type_id = tt.id
                GROUP BY tt.id
                ORDER BY tickets_sold DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_hourly_sales_breakdown(self, date: str = None) -> List[Dict]:
        """Get hourly sales breakdown for a specific date"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    STRFTIME('%H', sale_time) as hour,
                    COUNT(*) as tickets_sold,
                    SUM(price) as revenue
                FROM tickets
                WHERE DATE(sale_time) = ?
                GROUP BY hour
                ORDER BY hour
            """, (date,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]