import aiosqlite
from config import DB_NAME

class Database:
    conn = None

    @classmethod
    async def init(cls):
        cls.conn = await aiosqlite.connect(DB_NAME)
        cls.conn.row_factory = aiosqlite.Row
        await cls.conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id PRIMARY KEY, bal REAL DEFAULT 0, spent REAL DEFAULT 0,
                status TEXT DEFAULT 'USER', energy INT DEFAULT 100,
                ref_l1 INT DEFAULT 0, shadow_ban INT DEFAULT 0, joined TEXT
            );
            CREATE TABLE IF NOT EXISTS shop_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,
                name TEXT, price REAL, data TEXT, stock INT DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS p2p_market (
                id INTEGER PRIMARY KEY AUTOINCREMENT, seller_id INT,
                title TEXT, price REAL, status TEXT DEFAULT 'SALE'
            );
            CREATE TABLE IF NOT EXISTS inventory (
                uid INT, item_id INT, purchase_date TEXT
            );
            CREATE TABLE IF NOT EXISTS internal_mail (
                id INTEGER PRIMARY KEY, from_uid INT, to_uid INT, msg TEXT
            );
        """)
        await cls.conn.commit()
        async def init(self):
            await cls.conn.commit("""CREATE TABLE IF NOT EXISTS items 
        (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)""")
    
            await cls.conn.commit("""CREATE TABLE IF NOT EXISTS p2p_market 
        (id INTEGER PRIMARY KEY, seller_id INTEGER, item_name TEXT, price INTEGER, status TEXT)""")
    
            await cls.conn.commit("""CREATE TABLE IF NOT EXISTS mail 
        (id INTEGER PRIMARY KEY, user_id INTEGER, sender TEXT, text TEXT, is_read INTEGER DEFAULT 0)""")
        await cls.conn.commit()

    @classmethod
    async def get_user(cls, uid):
        async with cls.conn.execute("SELECT * FROM users WHERE id = ?", (uid,)) as cur:
            return await cur.fetchone()
