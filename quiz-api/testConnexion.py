import sqlite3

def connect_db():
    conn = sqlite3.connect('dataBase.db')
    return conn

def create_question(conn, position, title, text, image):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)", (position, title, text, image))
    conn.commit()

def retrieve_questions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Question")
    questions = cursor.fetchall()
    return questions

def main():
    with connect_db() as conn:
        # Créer un nouvel élément dans la table 'Question'
        create_question(conn, 1, 'Exemple de question', 'Ceci est un exemple de question.', 'example_image.jpg')




if __name__ == "__main__":
    main()
