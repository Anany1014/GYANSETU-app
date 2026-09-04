import sqlite3
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "gyansetu.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        uid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        class_level INTEGER DEFAULT 6,
        coins INTEGER DEFAULT 100,
        level INTEGER DEFAULT 1,
        title TEXT DEFAULT 'Beginner Scholar',
        avatar TEXT DEFAULT 'avatar_default.png',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Game Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        game_id TEXT NOT NULL,
        subject TEXT NOT NULL,
        class_num INTEGER NOT NULL,
        chapter TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        max_score INTEGER DEFAULT 100,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(uid) REFERENCES users(uid)
    )
    """)
    
    # Achievements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        achievement_id TEXT NOT NULL,
        title TEXT NOT NULL,
        desc TEXT NOT NULL,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(uid) REFERENCES users(uid)
    )
    """)
    
    # Inventory table (store purchases)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        item_id TEXT NOT NULL,
        item_type TEXT NOT NULL,
        item_name TEXT NOT NULL,
        cost INTEGER NOT NULL,
        purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(uid) REFERENCES users(uid)
    )
    """)
    
    # Daily Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        task_id TEXT NOT NULL,
        task_desc TEXT NOT NULL,
        reward_coins INTEGER DEFAULT 20,
        is_completed INTEGER DEFAULT 0,
        task_date TEXT NOT NULL,
        FOREIGN KEY(uid) REFERENCES users(uid)
    )
    """)
    
    conn.commit()
    conn.close()

def get_or_create_user(name="Scholar", class_level=6):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()
    if not user:
        uid = f"GS{int(time.time()) % 1000000:06d}"
        cursor.execute(
            "INSERT INTO users (uid, name, class_level, coins, level, title, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (uid, name, class_level, 100, 1, "Beginner Scholar", "profile.png")
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        user = cursor.fetchone()
        
        # Seed initial daily tasks for new user
        today = time.strftime("%Y-%m-%d")
        default_tasks = [
            ("t1", "Play 1 Arithmetic Game", 25),
            ("t2", "Score 50+ points in General Knowledge", 30),
            ("t3", "Complete an English Lesson", 20)
        ]
        for tid, tdesc, treward in default_tasks:
            cursor.execute(
                "INSERT INTO daily_tasks (uid, task_id, task_desc, reward_coins, is_completed, task_date) VALUES (?, ?, ?, ?, 0, ?)",
                (uid, tid, tdesc, treward, today)
            )
        conn.commit()
    
    user_dict = dict(user)
    conn.close()
    return user_dict

def update_user_coins(uid, delta_coins):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET coins = MAX(0, coins + ?) WHERE uid = ?", (delta_coins, uid))
    
    # Recalculate user level based on total activities/coins
    cursor.execute("SELECT coins FROM users WHERE uid = ?", (uid,))
    res = cursor.fetchone()
    if res:
        coins = res["coins"]
        new_level = max(1, coins // 100 + 1)
        cursor.execute("UPDATE users SET level = ? WHERE uid = ?", (new_level, uid))
        
    conn.commit()
    conn.close()

def update_user_profile(uid, name, class_level, avatar=None, title=None):
    conn = get_connection()
    cursor = conn.cursor()
    if avatar and title:
        cursor.execute("UPDATE users SET name = ?, class_level = ?, avatar = ?, title = ? WHERE uid = ?", (name, class_level, avatar, title, uid))
    elif avatar:
        cursor.execute("UPDATE users SET name = ?, class_level = ?, avatar = ? WHERE uid = ?", (name, class_level, avatar, uid))
    else:
        cursor.execute("UPDATE users SET name = ?, class_level = ? WHERE uid = ?", (name, class_level, uid))
    conn.commit()
    conn.close()

def save_game_progress(uid, game_id, subject, class_num, chapter, score, max_score=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO progress (uid, game_id, subject, class_num, chapter, score, max_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (uid, game_id, subject, class_num, chapter, score, max_score)
    )
    conn.commit()
    conn.close()
    
    # Award coins based on score (e.g. 1 coin per 10 points score)
    earned_coins = max(5, score // 10)
    update_user_coins(uid, earned_coins)
    
    # Auto-unlock achievement if first game played
    unlock_achievement(uid, "ach_first_game", "First Steps", "Completed your very first learning game!")
    if score >= 80:
        unlock_achievement(uid, "ach_high_score", "Master Mind", "Scored 80+ points in a game!")
    return earned_coins

def get_user_progress(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress WHERE uid = ? ORDER BY completed_at DESC", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_subject_stats(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, COUNT(*) as games_played, SUM(score) as total_score, MAX(score) as max_score
        FROM progress WHERE uid = ? GROUP BY subject
    """, (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def unlock_achievement(uid, achievement_id, title, desc):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM achievements WHERE uid = ? AND achievement_id = ?", (uid, achievement_id))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO achievements (uid, achievement_id, title, desc) VALUES (?, ?, ?, ?)",
            (uid, achievement_id, title, desc)
        )
        conn.commit()
    conn.close()

def get_user_achievements(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM achievements WHERE uid = ? ORDER BY unlocked_at DESC", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def buy_inventory_item(uid, item_id, item_type, item_name, cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE uid = ?", (uid,))
    res = cursor.fetchone()
    if not res or res["coins"] < cost:
        conn.close()
        return False, "Not enough coins!"
    
    cursor.execute("SELECT id FROM inventory WHERE uid = ? AND item_id = ?", (uid, item_id))
    if cursor.fetchone():
        conn.close()
        return False, "Already owned!"
    
    # Deduct coins and add item
    cursor.execute("UPDATE users SET coins = coins - ? WHERE uid = ?", (cost, uid))
    cursor.execute(
        "INSERT INTO inventory (uid, item_id, item_type, item_name, cost) VALUES (?, ?, ?, ?, ?)",
        (uid, item_id, item_type, item_name, cost)
    )
    conn.commit()
    conn.close()
    return True, "Purchased successfully!"

def get_user_inventory(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE uid = ?", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_daily_tasks(uid):
    conn = get_connection()
    cursor = conn.cursor()
    today = time.strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM daily_tasks WHERE uid = ? AND task_date = ?", (uid, today))
    rows = cursor.fetchall()
    if not rows:
        default_tasks = [
            ("t1", "Play 1 Arithmetic Game", 25),
            ("t2", "Score 50+ points in General Knowledge", 30),
            ("t3", "Complete an English Lesson", 20)
        ]
        for tid, tdesc, treward in default_tasks:
            cursor.execute(
                "INSERT INTO daily_tasks (uid, task_id, task_desc, reward_coins, is_completed, task_date) VALUES (?, ?, ?, ?, 0, ?)",
                (uid, tid, tdesc, treward, today)
            )
        conn.commit()
        cursor.execute("SELECT * FROM daily_tasks WHERE uid = ? AND task_date = ?", (uid, today))
        rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def complete_daily_task(uid, task_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = time.strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM daily_tasks WHERE uid = ? AND task_id = ? AND task_date = ?", (uid, task_id, today))
    task = cursor.fetchone()
    if task and task["is_completed"] == 0:
        cursor.execute("UPDATE daily_tasks SET is_completed = 1 WHERE id = ?", (task["id"],))
        reward = task["reward_coins"]
        cursor.execute("UPDATE users SET coins = coins + ? WHERE uid = ?", (reward, uid))
        conn.commit()
        conn.close()
        return True, reward
    conn.close()
    return False, 0

def get_leaderboard():
    # Includes local user + mock offline rural competitors for competitive learning
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, level, coins FROM users ORDER BY coins DESC LIMIT 5")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    mock_users = [
        {"name": "Simran (Class 8)", "level": 5, "coins": 450},
        {"name": "Gurpreet (Class 7)", "level": 4, "coins": 380},
        {"name": "Aman (Class 6)", "level": 3, "coins": 290},
        {"name": "Priya (Class 9)", "level": 6, "coins": 520},
        {"name": "Harman (Class 5)", "level": 2, "coins": 180}
    ]
    all_ranks = sorted(rows + mock_users, key=lambda x: x["coins"], reverse=True)
    return all_ranks
