import os
import random

from flask import Flask, request, abort, jsonify, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Paginate questions returned
def paginate_questions(request, questions):
  PAGE = request.args.get('page', 1, type=int)
  START = (PAGE - 1) * QUESTIONS_PER_PAGE
  END = START + QUESTIONS_PER_PAGE

  question_lists = [question.format() for question in questions]
  current_questions = question_lists[START:END]

  return current_questions

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # Set up CORS that allows any origins for the api resources
  cors = CORS(app, resources={r"/api/*": {"origin": "*"}})

  # Set Access-Control-Allow headers and methods
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  # Handle GET requests for all available categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  # Handle GET requests for questions that are paginated
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    categories = Category.query.order_by(Category.id).all()
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })

  # Handle DELETE requests for questions with a question id
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      questions = Question.query.order_by(Question.id).all()
      updated_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True, 
        'deleted_question': question_id,
        'questions': updated_questions,
        'total_questions': len(questions),
        })
    except:
      abort(422)
  
  # Handle POST requests for questions, where the question and
  # answer text, category and difficulty score are required.
  @app.route('/questions', methods=['POST'])
  def post_questions():
    request_body = request.get_json()
    posted_question = request_body.get('question')
    answer = request_body.get('answer')
    difficulty = request_body.get('difficulty')
    category = request_body.get('category')
    # Return 422 error if either input is empty
    if posted_question is None or answer is None or difficulty is None or category is None:
      abort(422)
    
    try:
      question = Question(question=posted_question, 
                          answer=answer,
                          difficulty=difficulty,
                          category=category)
      question.insert()
      questions = Question.query.order_by(Question.id).all()
      updated_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'created_question': question.id,
        'questions': updated_questions,
        'total_questions': len(questions)
      })
    except:
      abort(422)

  # Handle search on questions using POST endpoint
  @app.route('/search', methods=['POST'])
  def search_questions():
    request_body = request.get_json()
    search_term = request_body.get('searchTerm')
    if search_term is None or search_term == '':
      abort(422)
    
    # Case-insensitive search term
    results = Question.query.filter(Question.question.ilike("%" + search_term + "%")).all()
    if len(results) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': [question.format() for question in results],
      'total_questions': len(results),
      'current_category': None
    })

  # Handle GET requests for questions based on category
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    if len(questions) == 0:
      abort(404)
      
    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions],
      'total_questions': len(questions),
      'current_category': category_id
    })

  # Handle questions for playing the quiz with POST endpoint
  @app.route('/play', methods=['POST'])
  def get_quizzes():
    request_body = request.get_json()
    previous_questions = request_body.get('previous_questions')
    quiz_category = request_body.get('quiz_category')
    
    # Check the format of quiz_category
    if isinstance(quiz_category, dict) == False:
      abort(422)

    # Check if the id is non-zero and null, the category is 
    # specified if both are true
    if quiz_category['id'] >= 1:
      quiz_category_id = quiz_category['id']
      questions = Question.query.filter_by(category=quiz_category_id).all()
    # If the id is zero or null, the category is unspecified
    else:
        questions = Question.query.all()

    available_questions = [question.id for question in questions]
    # If previous_questions is defined with values in it
    if previous_questions:
      # If any available questions is already in the list of
      # previous_questions, remove it from the available questions
      for i in previous_questions:
        if i in available_questions:
          available_questions.remove(i)
    
    # If none remains in the list of available questions,
    # return none for question
    if len(available_questions) == 0:
      return jsonify({
        'success': True,
        'question': None
      })
    # Otherwise, randomly select one from the available list
    else:
      quiz_question_id = random.choice(available_questions)
      quiz_question = Question.query.get(quiz_question_id)
      return jsonify({
        'success': True,
        'question': quiz_question.format()
      })

  # Create error handlers for all expected errors
  @app.errorhandler(400)
  def bad_request_error(error):
    return jsonify({
      'success': False,
      'error': '400',
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      'success': False,
      'error': '404',
      'message': 'Not Found'
    }), 404

  @app.errorhandler(405)
  def not_allowed_error(error):
    return jsonify({
      'success': False,
      'error': '405',
      'message': 'Method Not Allowed'
    }), 405
  
  @app.errorhandler(422)
  def unprocessable_error(error):
    return jsonify({
      'success': False,
      'error': '422',
      'message': 'Unprocessable'
    }), 422
  
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': '500',
      'message': 'Internal Server Error'
    }), 500

  return app