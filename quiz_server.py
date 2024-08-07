import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 8000
server.bind((ip_address, port))
server.listen()
clients = []

questions = [
    "What is the capital of France?\n a) Rome\n b) Madrid\n c) Paris\n d) Berlin",
    "Which planet is known as the Red Planet?\n a) Mars\n b) Venus\n c) Jupiter\n d) Saturn",
    "Who wrote the play 'Romeo and Juliet'?\n a) Charles Dickens\n b) William Shakespeare\n c) Mark Twain\n d) J.K. Rowling",
    "What is the largest ocean on Earth?\n a) Atlantic Ocean\n b) Indian Ocean\n c) Arctic Ocean\n d) Pacific Ocean",
    "Who painted the Mona Lisa?\n a) Vincent van Gogh\n b) Pablo Picasso\n c) Leonardo da Vinci\n d) Claude Monet",
    "What is the smallest prime number?\n a) 2\n b) 3\n c) 1\n d) 5",
    "Which country is famous for inventing pizza?\n a) France\n b) Italy\n c) Greece\n d) Spain",
    "What is the chemical symbol for water?\n a) H2O\n b) CO2\n c) O2\n d) N2",
    "In which year did the Titanic sink?\n a) 1912\n b) 1905\n c) 1920\n d) 1915",
    "Who is known as the 'Father of Computers'?\n a) Isaac Newton\n b) Alan Turing\n c) Charles Babbage\n d) Thomas Edison"
]
answers = ['c', 'a', 'b', 'd', 'c', 'a', 'b', 'a', 'a', 'c']
nicknames = []

def clientthread(conn, addr):
    score = 0
    conn.send("Welcome to this quiz game!".encode("utf-8"))
    conn.send("You will recieve a question. The answer to that question should be a, b, c, or d\n".encode("utf-8"))
    conn.send("Good Luck!\n\n".encode("utf-8"))
    random_question, question, answer = get_random_question_answer()
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Correct! Your score is: {score}\n\n".encode("utf-8"))
                else:
                    conn.send("Incorrect! Better luck next time!\n\n".encode("utf-8"))
                remove_question(random_question)
                random_question, question, answer = get_random_question_answer()
            else:
                remove(conn)
        except:
            continue

def get_random_question_answer():
    random_question = random.randint(0, len(questions) - 1)
    question = questions[random_question]
    answer = answers[random_question]
    conn.send(question.encode("utf-8"))
    return random_question, question, answer

def remove_question(random_question):
    questions.pop(random_question)
    answers.pop(random_question)

def remove(conn):
    if conn in clients:
        clients.remove(conn)

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    clients.append(conn)
    nicknames.append(nickname)
    print(nickname, " connected")
    new_thread = Thread(target=clientthread, args=(conn, nickname))
    new_thread.start()