import psycopg2


def create_tables():
    conn = psycopg2.connect(
        host="localhost",
        database="headhunter_db",
        user="postgres",
        password="0102aamiss"
    )
    cur = conn.cursor()

    # Создание таблицы работодателей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT
        );
    """)

    # Создание таблицы вакансий
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            salary INTEGER,
            url TEXT,
            employer_id INTEGER REFERENCES employers(id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")


if __name__ == "__main__":
    create_tables()
