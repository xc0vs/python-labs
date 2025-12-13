import sqlite3
from datetime import datetime, timedelta
import random

class SecurityLogSystem:
    def __init__(self, db_name="security_logs.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventSources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                location TEXT,
                type TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventTypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT UNIQUE NOT NULL,
                severity TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SecurityEvents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source_id INTEGER,
                event_type_id INTEGER,
                message TEXT,
                ip_address TEXT,
                username TEXT,
                FOREIGN KEY (source_id) REFERENCES EventSources(id),
                FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
            )
        """)
        self.conn.commit()

    # Функції реєстрації та запису (Завдання 4a, 4b, 4c)

    def register_source(self, name, location, src_type):
        try:
            self.cursor.execute("""
                INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)
            """, (name, location, src_type))
            self.conn.commit()
            print(f"[INFO] Джерело '{name}' успішно додано.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"[WARN] Джерело '{name}' вже існує.")


    def register_event_type(self, type_name, severity):
        """4.b Реєстрація нового типу подій."""
        try:
            self.cursor.execute("""
                INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)
            """, (type_name, severity))
            self.conn.commit()
            print(f"[INFO] Тип події '{type_name}' успішно додано.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"[WARN] Тип події '{type_name}' вже існує.")


    def log_event(self, source_id, event_type_id, message, ip_address=None, username=None, custom_time=None):
        if custom_time is None:
            timestamp = datetime.now()
        else:
            timestamp = custom_time

        self.cursor.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, source_id, event_type_id, message, ip_address, username))
        self.conn.commit()


    def get_login_failures_24h(self):
        print("\n--- Login Failed за останні 24 години ---")
        query = """
            SELECT SecurityEvents.timestamp, EventSources.name, SecurityEvents.ip_address, SecurityEvents.username 
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            JOIN EventSources ON SecurityEvents.source_id = EventSources.id
            WHERE EventTypes.type_name = 'Login Failed' 
            AND SecurityEvents.timestamp >= datetime('now', '-1 day')
        """
        rows = self.cursor.execute(query).fetchall()
        if not rows:
            print("Подій не знайдено.")
        for row in rows:
            print(f"Time: {row[0]} | Source: {row[1]} | IP: {row[2]} | User: {row[3]}")


    def detect_brute_force(self):
        print("\n--- Потенційні атаки (Brute Force) за останню годину ---")
        query = """
            SELECT SecurityEvents.ip_address, COUNT(*) as attempts
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            WHERE EventTypes.type_name = 'Login Failed'
            AND SecurityEvents.timestamp >= datetime('now', '-1 hour')
            GROUP BY SecurityEvents.ip_address
            HAVING attempts > 5
        """
        rows = self.cursor.execute(query).fetchall()
        if not rows:
            print("Підозрілих активностей не виявлено.")
        for row in rows:
            print(f"ALARM! IP: {row[0]} здійснив {row[1]} невдалих спроб входу.")


    def get_critical_events_grouped(self):
        print("\n--- Critical події за останній тиждень ---")
        query = """
            SELECT EventSources.name, COUNT(*) as count, GROUP_CONCAT(EventTypes.type_name, ', ')
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            JOIN EventSources ON SecurityEvents.source_id = EventSources.id
            WHERE EventTypes.severity = 'Critical'
            AND SecurityEvents.timestamp >= datetime('now', '-7 days')
            GROUP BY EventSources.name
        """
        rows = self.cursor.execute(query).fetchall()
        if not rows:
            print("Критичних подій не знайдено.")
        for row in rows:
            print(f"Source: {row[0]} | Total Critical: {row[1]} | Types: {row[2]}")

    def search_by_keyword(self, keyword):
        print(f"\n--- Пошук за словом '{keyword}' ---")
        query = """
            SELECT SecurityEvents.timestamp, SecurityEvents.message 
            FROM SecurityEvents
            WHERE SecurityEvents.message LIKE ?
        """

        rows = self.cursor.execute(query, (f'%{keyword}%',)).fetchall()
        for row in rows:
            print(f"Time: {row[0]} | Message: {row[1]}")

    def close(self):
        self.conn.close()



if __name__ == "__main__":

    system = SecurityLogSystem()

    initial_types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]
    
    type_ids = {}
    for t_name, severity in initial_types:
        type_ids[t_name] = system.register_event_type(t_name, severity)

    sources_data = [
        ("Firewall_Main", "192.168.1.1", "Firewall"),
        ("Web_Server_Apache", "192.168.1.10", "Web Server"),
        ("IDS_Sensor_N", "Gateway_North", "IDS"),
        ("DB_Server_Oracle", "192.168.1.50", "Database")
    ]
    
    source_ids = []
    for name, loc, s_type in sources_data:
        source_ids.append(system.register_source(name, loc, s_type))

    print("\n[INFO] Генерація тестових даних...")
    
    users = ["admin", "user1", "guest", "root", "manager"]
    ips = ["10.0.0.5", "192.168.1.100", "172.16.0.5", "45.33.22.11"]
    
    for _ in range(15):
        s_id = random.choice(source_ids)
        t_name = random.choice(list(type_ids.keys()))
        t_id = type_ids[t_name]
        
        msg = f"Detected {t_name} event initiated by user."
        user = random.choice(users)
        ip = random.choice(ips)
        
        rand_time = datetime.now() - timedelta(hours=random.randint(0, 72))
        
        system.log_event(s_id, t_id, msg, ip, user, rand_time)

    attacker_ip = "66.249.66.1"
    brute_force_type_id = type_ids["Login Failed"]
    target_source = source_ids[1] # Web Server
    
    print("[INFO] Симуляція Brute Force атаки...")
    for i in range(6):
        system.log_event(
            source_id=target_source,
            event_type_id=brute_force_type_id,
            message=f"Invalid password for user root. Attempt {i+1}",
            ip_address=attacker_ip,
            username="root",
            custom_time=datetime.now() - timedelta(minutes=i*5)
        )
        
    system.log_event(
        source_id=source_ids[0],
        event_type_id=type_ids["Malware Alert"],
        message="Trojan detected on perimeter",
        ip_address="192.168.1.1",
        username="N/A",
        custom_time=datetime.now() - timedelta(hours=2)
    )

    system.get_login_failures_24h()
    system.detect_brute_force()
    system.get_critical_events_grouped()
    system.search_by_keyword("password")

    system.close()