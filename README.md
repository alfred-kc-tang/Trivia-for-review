# Trivia

This Trivia web app had been built with its frontend using React, but its API experience had been limited. My job was to implement and test the API for this application that has the following functionalities:

1) Display questions - both all questions and by category. The question, category, difficulty rating are shown by default, and the answer can be shown or hidden. 
2) Add questions.
3) Delete questions.
4) Search for questions.
5) Play the quiz game, with randomized questions from either all questions or within a specific category.

# Installation

## Frontend

### Installing Dependencies

This project depends on Node.js and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Running in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Backend

### Installing Dependencies


1. First install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

2. Then restore a database using the trivia.psql file given. With Postgres running, run the following in terminal:

```bash
psql trivia < trivia.psql
```

3. To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

# API Reference

## Introduction
* Base URL: This app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `localhost:5000` or `127.0.0.1:5000`, which is set as a proxy in the frontend configuration. The frondend is hosted at the port `3000`.
* Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format

```bash
{
    "sucess": False,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return four error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable
* 500: Internal Server Error

## Endpoints

* [GET /categrories](#get-categories)
* [GET /questions](#get-questions)
* [DELETE /questions/<question_id>](#delete-questionsquestion_id)
* [POST /questions](#post-questions)
* [POST /search](#post-search)
* [GET /categories/<category_id>/questions](#get-categoriescategory_idquestions)
* [POST /play](#post-play)

### GET /categories

- Fetches a dictionary of categories with ids and types as the key-value pairs
- Request Arguments: None 
- Sample Request: `curl http://127.0.0.1/categories`
- Response: a JSON object with the key " categories" that contains a object of id:type key:value pairs, as well as the "success" key.
- Sample Response:
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

## GET /questions
- Fetches a list of questions, each with a dictionary containing the id, the question itself, the answer, the category id, and the difficulty score, as well as the total number of questions
- Request Arguments: None
- Sample Request: `curl http://127.0.0.1/questions`
- Response: a JSON object with keys of categories, current_category, questions, which contains a list of dictionaries, as well as total_questions and success.
- Sample Response:
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```

## DELETE /questions/<question_id>
- Deletes a question
- Request Arguments: question id
- Sample Request: `curl DELETE http://127.0.0.1/questions/<question_id>`
- Response: a JSON object with keys of success and deleted_question indicating the removed question id
- Sample Response:
```bash
{
    "deleted_question": "21",
    "success": true
}
```

## POST /questions
- Posts a question
- Request Arguments: question and answer texts, category id, and difficutly score
- Sample Request: `curl --header "Content-Type: application/json" --request POST --data{"question": "<question_text>", "answer": "<answer_text>", "category": "<category_id>", "difficulty": "<difficulty_score>"} http://127.0.0.1/questions`
- Response: a JSON object with keys of success and created_question indicating the newly added question id
- Sample Response:
```bash
{
    "created_question": "22",
    "success": true
}
```

## POST /search
- Searches questions containing the search term
- Request Argument: search term
- Sample Request: `curl --header "Content-Type: application/json" --request POST --data{"searchTerm": "hanks"} http://127.0.0.1/search`
- Reponse: a JSON object with keys of success, total_questions, current_category and questions that contain a list of dictionaries each with question information
- Sample Response:
```bash
{
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

## GET /categories/<category_id>/questions
- Fetches a list of questions by category, each with a dictionary containing the id, the question itself, the answer, the category id, and the difficulty score, as well as the total number of questions
- Request Argument: category id
- Sample Request: `curl http://127.0.0.1/categories/2/questions`
- Reponse: a JSON object with keys of categories, current_category, questions, which contains a list of dictionaries, as well as total_questions and success.
- Sample Response:
```bash
{
    "current_category": "2",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

## POST /play
- Enable the quiz game by fetching a randomized question from either all questions or within a specified category that has not yet appeared in previous questions
- Request Argument: (1) list of previous questions (could be empty list) and (2) quiz question category (optional)
- Sample Request: `curl --header "Content-Type: application/json" --request POST --data{"previous_questions": [16, 19], "quiz_category": {"id": 2, "type": "Art"}} http://127.0.0.1/play`
- Reponse: a question randomly drawn that are not in the list of previous questions
- Sample Response:
```bash
{
    "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
}
```


# Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
