import sqlite3
from question_model import Question, PossibleAnswer

DATABASE_PATH = 'dataBase.db'

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def insert_question(question: Question):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, position, title, text, image FROM Question WHERE position = ?", (question.position,))
    existing_question = cursor.fetchone()
    if existing_question is not None:

        # Incrémenter les positions des questions existantes si nécessaire
        cursor.execute("""
            UPDATE Question
            SET position = position + 1
            WHERE position >= ?
        """, (question.position,))

    try:
        cursor.execute(
            "INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)", 
            (question.position, question.title, question.text, question.image)
        )
        question_id = cursor.lastrowid
        answer_position=1
        for answer in question.possible_answers:
            cursor.execute(
                "INSERT INTO PossibleAnswer (question_id, text, is_correct,position) VALUES (?, ?, ?,?)",
                (question_id, answer.text, int(answer.is_correct),answer_position)
                
            )
            answer_position += 1

        conn.commit()
        return question_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()



def get_question_by_id(question_id : int ):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,))
    question_row = cursor.fetchone()

    cursor.execute("SELECT * FROM PossibleAnswer WHERE question_id = ?", (question_id,))
    answer_rows = cursor.fetchall()

    conn.close()

    if question_row:
        possible_answers = [
            PossibleAnswer(id=row[0], text=row[2], is_correct=bool(row[3]))
            for row in answer_rows
        ]
        return Question(
            id=question_row[0], 
            position=question_row[1], 
            title=question_row[2], 
            text=question_row[3], 
            image=question_row[4], 
            possible_answers=possible_answers
        )
    return None

def get_question_by_position(position : int  ):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Question WHERE position = ?", (position,))
    question_row = cursor.fetchone()

    if question_row:
        cursor.execute("SELECT * FROM PossibleAnswer WHERE question_id = ?", (question_row[0],))
        answer_rows = cursor.fetchall()
        conn.close()

        possible_answers = [
            PossibleAnswer(id=row[0], text=row[2], is_correct=bool(row[3]))
            for row in answer_rows
        ]
        return Question(
            id=question_row[0], 
            position=question_row[1], 
            title=question_row[2], 
            text=question_row[3], 
            image=question_row[4], 
            possible_answers=possible_answers
        )
    return None

def reassign_positions(current_position : int = 1, position_to_set : int =1):

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Question")
    question_count = cursor.fetchone()[0]
    while(position_to_set <= question_count):
        cursor.execute("SELECT id FROM Question WHERE position = ?", (current_position,))
        question_at_position = cursor.fetchone()
        if question_at_position is None:
            current_position += 1 # On cherche une question avec une position plus haute
        else:

            # On réasigne la position
            cursor.execute("UPDATE Question SET position = ? WHERE id = ?", (position_to_set, question_at_position[0]))
            conn.commit()
            #update_question_position(question_at_position,position_to_set)

            current_position += 1
            position_to_set += 1

    conn.close()






