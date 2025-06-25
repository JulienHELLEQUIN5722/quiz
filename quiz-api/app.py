import hashlib
import token
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from jwt_utils import build_token
from question import connect_db, insert_question, get_question_by_id, get_question_by_position, reassign_positions 
from question_model import Question
from possibleAnswer_model import PossibleAnswer

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"


    
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM Question")
	question_size = cursor.fetchone()[0]

	cursor.execute("SELECT * FROM Participation ORDER BY score DESC")
	all_participations = cursor.fetchall()

	all_participations_return = [
				{"playerName": participation[1], "score": participation[2]} for participation in all_participations
			]

	conn.close()


	return {"size": question_size, "scores": all_participations_return}, 200	

@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	tried_password = payload['password'].encode('UTF-8')
	
	hashed = hashlib.md5(tried_password).digest()

	if hashed == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@': #mot de passe == "flask2023"
		token = build_token()
		JsonToReturn = {
			"token" : token
		}
		return json.dumps(JsonToReturn), 200
	
	else : 
		return 'Unauthorized', 401
	
@app.route('/questions', methods=['POST'])
def post_question():
	token = request.headers.get('Authorization')
	if not token:
		return 'Token is missing', 401
	payload = request.get_json()
	new_question = Question.from_dict(payload)
	question_id = insert_question(new_question)
	return jsonify({'id':question_id}),200


@app.route('/all-questions/', methods=['GET'])
def get_all_questions():
	conn = connect_db()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Question")
	questions = cursor.fetchall()

	cursor.execute("SELECT * FROM PossibleAnswer")
	possibles_answers = cursor.fetchall()

	if questions and possibles_answers : 

		all_questions = []
		possible_answers_list = []
		for question in questions : 
			question_id = question[0]
			possible_answers_list = [
				{"text": answer[2], "isCorrect": bool(answer[3])} for answer in possibles_answers if answer[1] == question_id
			 	]
		

			question_formated = {
					"id": question_id,
					"title": question[2],
					"text": question[3],
					"position": question[1],
					"image": question[4],
					"possibleAnswers": possible_answers_list
			}

			all_questions.append(question_formated)
		
		conn.close()
		return jsonify(all_questions), 200
	else :
		conn.close()
		return jsonify({"error": "Questions not found"}), 404
	
@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
	
	conn = connect_db()
	cursor = conn.cursor()

	cursor.execute("SELECT id, position, title, text, image FROM Question WHERE id = ?", (question_id,))
	question = cursor.fetchone()

	if question : 

		question_id, position, title, text, image = question
		cursor.execute("SELECT text, is_correct FROM PossibleAnswer WHERE question_id = ?", (question_id,))
		possible_answers = cursor.fetchall()
		possible_answers_list = [
				{"text": answer[0], "isCorrect": bool(answer[1])} for answer in possible_answers
			]

		response = {
				"id": question_id,
				"title": title,
				"text": text,
				"position": position,
				"image": image,
				"possibleAnswers": possible_answers_list
			}
		
		conn.close()
		return jsonify(response), 200
	else :
		conn.close()
		return jsonify({"error": "Question not found"}), 404


@app.route('/questions/all', methods=['DELETE'])
def del_questions_all():
	token = request.headers.get('Authorization')
	if not token:
		return 'Token is missing', 401

	conn = connect_db()
	cursor = conn.cursor()

	try:
		cursor.execute("DELETE FROM Question")
		cursor.execute("DELETE FROM PossibleAnswer")
		conn.commit()  
	except Exception as e:
		conn.rollback()  
		return str(e), 500  
	finally:
		conn.close()  
    
	return "Request respond ok", 204

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def del_question_by_id(question_id):
	token = request.headers.get('Authorization')
	if not token:
		return 'Token is missing', 401

	conn = connect_db()
	cursor = conn.cursor()

	try:
		cursor.execute("SELECT COUNT(*) FROM Question WHERE id = ?", (question_id,))
		if cursor.fetchone()[0] == 0:
			conn.close()
			return "Question not found", 404

		cursor.execute("DELETE FROM PossibleAnswer WHERE question_id = ?", (question_id,))
		cursor.execute("DELETE FROM Question WHERE id = ?", (question_id,))
        
		conn.commit()

		reassign_positions()

		return "Question and its possible answers deleted successfully", 204

	except Exception as e:
		conn.rollback()
		return str(e), 500

	finally:
		conn.close()


@app.route('/participations/all', methods=['DELETE'])
def del_participations_all():

	token = request.headers.get('Authorization')
	if not token:
		return 'Token is missing', 401

	conn = connect_db()
	cursor = conn.cursor()

	try:
		cursor.execute("DELETE FROM Participation")
		conn.commit()  
	except Exception as e:
		conn.rollback()  
		return str(e), 500  
	finally:
		conn.close()  
    
	return "Request respond ok", 204

@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get('position', type=int)
    if position is None:
        return jsonify({'error': 'Position parameter is missing or invalid'}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Question WHERE position = ?", (position,))
    question = cursor.fetchone()

    if question:
        question_data = {
            'id': question[0],
            'position': question[1],
			'title': question[2],
            'text': question[3],
            'image': question[4]
        }

        cursor.execute("SELECT * FROM PossibleAnswer WHERE question_id = ?", (question[0],))
        possible_answers = cursor.fetchall()

        question_data['possibleAnswers'] = [{
            'text': answer[2],
            'isCorrect': bool(answer[3])
        } for answer in possible_answers]

        conn.close()
        return jsonify(question_data), 200
    else:
        conn.close()
        return jsonify({'error': 'Question not found'}), 404


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
	data = request.get_json()

	title = data.get('title')
	text = data.get('text')
	position = data.get('position')
	image = data.get('image')

	possible_answers = data.get('possibleAnswers')

	if title is None or text is None or position is None or image is None or possible_answers is None:
		return jsonify({'error': 'Missing required fields in request body'}), 400

	conn = connect_db()
	cursor = conn.cursor()


	cursor.execute("SELECT id, title, text, position, image FROM Question WHERE id = ?", (question_id,))	
	existing_question = cursor.fetchone()

	if existing_question is None:
		conn.close()
		return "Question not found", 404
	
	else:
		if(existing_question[3] != position) : 
			#si il faut changer la position de la question
			#il faudra aussi vérifier si il n'y a pas déjà de question à cette position
			#si c'est le cas, on fait un glissement des positions des questions

			cursor.execute("SELECT id, title, text, position, image FROM Question WHERE position = ?", (position,))	
			question_already_here = cursor.fetchone()

			if question_already_here is not None:#Si il y a déjà une question à cette position
				if(position < existing_question[3]) : 
					#On assigne à la question sa position demandé,...
					cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
						(title, text, position, image, question_id))

					if( existing_question[3] - position >1) : #... puis on fait les glissement si il y a des questions entre les 2 positions						
						current_position = existing_question[3] 
						while(current_position != position +1 ) : 
							cursor.execute("SELECT id, title, text, position, image FROM Question WHERE position = ?", (current_position -1,))	
							current_question = cursor.fetchone()

							cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(current_question[1], current_question[2], current_position, current_question[4], current_question[0]))
							current_position -=1 
						
						cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(question_already_here[1], question_already_here[2], current_position, question_already_here[4], question_already_here[0]))
			
					else : 
						cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(question_already_here[1], question_already_here[2], existing_question[3], question_already_here[4], question_already_here[0]))
				
				if(position > existing_question[3]) :
					cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
						(title, text, position, image, question_id))
					if(position - existing_question[3] > 1) :

						current_position = existing_question[3]

						while(current_position != position -1 ) : 
							cursor.execute("SELECT id, title, text, position, image FROM Question WHERE position = ?", (current_position +1,))	
							current_question = cursor.fetchone()

							cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(current_question[1], current_question[2], current_position, current_question[4], current_question[0]))
							current_position +=1 

						cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(question_already_here[1], question_already_here[2], current_position, question_already_here[4], question_already_here[0]))

					else : 
						cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
							(question_already_here[1], question_already_here[2], existing_question[3], question_already_here[4], question_already_here[0]))

						

		else : #si il n'y a pas déjà de question à cette position
			cursor.execute("UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?",
				(title, text, position, image, question_id))

		#Supression et insertion des nouvelles réponses possibles	
		cursor.execute("DELETE FROM PossibleAnswer WHERE question_id = ?", (question_id,))
		answer_position =1
		for answer in possible_answers:
			text = answer.get('text')
			is_correct = answer.get('isCorrect')
			cursor.execute("INSERT INTO PossibleAnswer (question_id, text, is_correct, position) VALUES (?, ?, ?, ?)", (question_id, text, is_correct,answer_position))
			answer_position+=1
			
		conn.commit()
		conn.close()

		return jsonify({'message': 'Question updated successfully'}), 204

@app.route('/participations/all', methods=['GET'])
def GetAllParticipations():
	conn = connect_db()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Participation ORDER BY score DESC")
	all_participations = cursor.fetchall()

	all_participations_return = [
				{"playerName": participation[1], "score": participation[2]} for participation in all_participations
			]

	conn.close()


	return {"allParticipations" : all_participations_return}, 200


@app.route('/participations', methods=['POST'])
def post_participation():
	data = request.get_json()
	answers = data['answers']
	if(len(answers) != 10):
		return "Bad request",400
	
	#récupération des positions des bonnes réponses
	conn = connect_db()
	cursor = conn.cursor()
	cursor.execute("""
            SELECT pa.position AS answer_position
            FROM Question q
            JOIN PossibleAnswer pa ON q.id = pa.question_id
            WHERE q.position BETWEEN 1 AND 10
            AND pa.is_correct = 1
            ORDER BY q.position ASC;
        """)
	correct_answers = cursor.fetchall()	

	#Comparaison des positions des réponses
	score:int=0
	for i in range(0,10):
		if(answers[i]==correct_answers[i][0]):
			score+=1
	cursor.execute("INSERT INTO Participation (name, score) VALUES(?, ?)",(data['playerName'],score))
	conn.commit()
	conn.close()
	return {"playerName":data['playerName'], "score":score},200

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
	conn = connect_db()
	cursor = conn.cursor()
	sql_script = """
    -- Drop existing tables
    DROP TABLE IF EXISTS Participation;
    DROP TABLE IF EXISTS PossibleAnswer;
    DROP TABLE IF EXISTS Question;

    -- Recreate tables

    -- Table: Participation
    CREATE TABLE "Participation" (
        "id" INTEGER NOT NULL,
        "name" TEXT NOT NULL,
        "score" INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    );

    -- Table: PossibleAnswer
    CREATE TABLE "PossibleAnswer" (
        "id" INTEGER NOT NULL,
        "question_id" INTEGER NOT NULL,
        "text" TEXT NOT NULL,
        "is_correct" INTEGER NOT NULL,
        "position" INTEGER NOT NULL,
        PRIMARY KEY("id")
    );

    -- Table: Question
    CREATE TABLE "Question" (
        "id" INTEGER NOT NULL,
        "position" INTEGER NOT NULL,
        "title" TEXT NOT NULL,
        "text" TEXT NOT NULL,
        "image" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """
    
	try:
		cursor.executescript(sql_script)

		with open('questions.json', 'r', encoding='utf-8') as file:
			questions_data = json.load(file)
		for question_data in questions_data:
			possible_answers = [
                PossibleAnswer(
                    text=answer['text'],
                    is_correct=answer['isCorrect'],
                    position=index + 1
                ) for index, answer in enumerate(question_data['possibleAnswers'])
            ]
            
			question = Question(
                position=question_data['position'],
                title=question_data['title'],
                text=question_data['text'],
                image=question_data['image'],
                possible_answers=possible_answers
            )
            
			insert_question(question)

		return "Ok",200
	except Exception as e:
		return "Fail in databse rebuild",400
	finally:
		conn.close()

	

if __name__ == "__main__":
	app.run()