import sqlite3
conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserProjects (
    id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES Users(id)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS ProjectsQuestions (
    project_id TEXT NOT NULL,
    question_text TEXT NOT NULL
);
''')

conn.commit()
conn.close()

# Function to check if a user exists
def user_exists(user_id):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    SELECT 1 FROM Users WHERE id = ?
    '''
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:      # user already exists
        return True 
    else:           # user does not exists
        return False
    
# Function to insert data into Users table
def insert_into_users_table(id, password):
    if user_exists(id):
        return False  # User already exists
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    INSERT INTO Users (id, password)
    VALUES (?, ?)
    '''
    cursor.execute(query, (id, password))
    conn.commit()
    conn.close()
    return True

# Other functions (unchanged)
def insert_into_userprojects_table(id, project_id):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    INSERT INTO UserProjects (id, project_id)
    VALUES (?, ?)
    '''
    cursor.execute(query, (id, project_id))
    conn.commit()
    conn.close()

def insert_into_projectsquestions_table(project_id, question_text):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    INSERT INTO ProjectsQuestions (project_id, question_text)
    VALUES (?, ?)
    '''
    cursor.execute(query, (project_id, question_text))
    conn.commit()
    conn.close()

def check_user_credentials(user_id, password):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    SELECT 1 FROM Users WHERE id = ? AND password = ?
    '''
    cursor.execute(query, (user_id, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_project_ids(user_id):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    SELECT project_id 
    FROM UserProjects 
    WHERE id = ?
    '''
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    conn.close()
    project_ids = [result[0] for result in results] if results else []
    return project_ids

def get_question_texts(project_id):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    query = '''
    SELECT question_text
    FROM ProjectsQuestions 
    WHERE project_id = ?
    '''
    cursor.execute(query, (project_id,))
    results = cursor.fetchall()
    conn.close()
    question_texts = [result[0] for result in results]
    return question_texts

insert_into_users_table("user2",password="password124")
insert_into_userprojects_table("user2",project_id="proj3")
insert_into_projectsquestions_table("proj3","Will a Learner earn Credits & certificate after going through the MOOCs on SWAYAM?")
insert_into_projectsquestions_table("proj3","Has Government embarked upon an ICT Programme in the Past?")
insert_into_projectsquestions_table("proj3","What are the outcomes of the SWAYAM.")


insert_into_users_table("user20",password="password1220")
insert_into_userprojects_table("user20",project_id="client_trainer_1")
insert_into_projectsquestions_table("client_trainer_1","Can a learner see the last login information on Swayam portal?")
insert_into_projectsquestions_table("client_trainer_1","How can I select a course on Swayam?")
insert_into_projectsquestions_table("client_trainer_1","What different activities can a learner do within a discussion forum?")


insert_into_users_table("user20",password="password1220")
insert_into_userprojects_table("30",project_id="client_trainer_1")
insert_into_projectsquestions_table("client_trainer_1","")
insert_into_projectsquestions_table("client_trainer_1","How can I select a course on Swayam?")
insert_into_projectsquestions_table("client_trainer_1","What different activities can a learner do within a discussion forum?")


insert_into_users_table(id="user10",password="password1210")
insert_into_userprojects_table(id="user10",project_id="client_trainer")
insert_into_projectsquestions_table("client_trainer","Will a Learner earn Credits & certificate after going through the MOOCs on SWAYAM?")
insert_into_projectsquestions_table("client_trainer","Has Government embarked upon an ICT Programme in the Past?")
insert_into_projectsquestions_table("client_trainer","What are the outcomes of the SWAYAM.")