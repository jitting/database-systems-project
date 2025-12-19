#!/usr/bin/env python3
"""
Test database connection for SkillLink application
"""

import psycopg2
from config import DB_CONFIG

def test_connection():
    """Test PostgreSQL connection"""
    print("=" * 60)
    print("SkillLink Database Connection Test")
    print("=" * 60)
    print(f"\nAttempting to connect with:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Password: {'*' * len(DB_CONFIG['password']) if DB_CONFIG['password'] else '(empty)'}")
    print("\nConnecting...")

    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("\n✓ Connection successful!")
        print(f"\nPostgreSQL version:")
        print(f"  {version[0]}")

        # Check if tables exist
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()

        if tables:
            print(f"\n✓ Found {len(tables)} tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("\n⚠ Warning: No tables found in database!")
            print("  You need to import the SQL schema.")

        # Check for sample data
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]

        if user_count > 0:
            print(f"\n✓ Found {user_count} users in database")
            print("\n✓ Database is ready to use!")
        else:
            print("\n⚠ Warning: No users found in database!")
            print("  You may need to import the sample data.")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("You can now run: python3 skilllink_app.py")
        print("=" * 60)

        return True

    except psycopg2.OperationalError as e:
        print("\n✗ Connection failed!")
        print(f"\nError: {e}")
        print("\nPossible solutions:")
        print("  1. Check that PostgreSQL is running")
        print("  2. Verify the database name in config.py")
        print("  3. Check username and password in config.py")
        print("  4. Make sure the database exists in pgAdmin4")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
