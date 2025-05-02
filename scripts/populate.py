from sqlalchemy.orm import Session
from app.models import QuestionCategory, Question, User, Interviews, InterviewQuestion, InterviewFeedback, InterviewMistake, MistakeCategory, CompetencyLevel
from app.database import SessionLocal
from faker import Faker

fake = Faker()

def populate_db():
    populate_competency_levels()
    populate_question_categories()
    populate_questions()
    populate_users()
    populate_interviews()
    populate_interview_questions()  
    populate_interview_feedback()
    populate_mistake_categories()
    populate_interview_mistakes()
    
def populate_users():
    db = SessionLocal()
    try:
        competency_levels = db.query(CompetencyLevel).all()

        if not competency_levels:
            print("No hay niveles de competencia para asignar en User.")
            return
        
        for _ in range(5):  
            user = User(
                email=fake.email(),
                hashed_password=fake.password(),
                b2c=fake.boolean(),
                interview_count=fake.random_int(min=0, max=100),
                linkedin_url=fake.url(),
                clarity_level=competency_levels[0].id,  
                structure_level=competency_levels[1].id,  
                communication_level=competency_levels[2].id
            )
            db.add(user)
        db.commit()
        print("5 usuarios fueron agregados correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def populate_interviews():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        for user in users:
            for _ in range(3):  
                interview = Interviews(
                    completed_at=fake.date_time_this_year(),
                    user_id=user.id
                )
                db.add(interview)
        
        db.commit()
        print("Se han agregado entrevistas para los usuarios.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def populate_questions():
    db = SessionLocal()
    try:
        categories = db.query(QuestionCategory).all()

        if not categories:
            print("No hay categorías de preguntas para asignar.")
            return

        question_pool = [
            "Describe una situación en la que hayas liderado un equipo. ¿Cómo manejaste los desafíos?",
            "Cuéntame sobre un proyecto en el que tuviste que trabajar bajo presión. ¿Cómo lo manejaste?",
            "¿Cuál es tu enfoque para resolver conflictos en un equipo de trabajo?",
            "¿Cómo manejas situaciones donde no estás de acuerdo con un compañero de trabajo?",
            "Describe un momento en el que tuviste que tomar una decisión difícil en el trabajo. ¿Cómo lo hiciste?",
            "¿Cómo priorizas tus tareas cuando tienes múltiples proyectos con plazos ajustados?",
            "Háblame sobre una vez que tuviste que adaptarte a un cambio importante en tu entorno laboral.",
            "¿Cuál es tu enfoque para mantener una buena comunicación en tu equipo de trabajo?",
            "Descríbeme cómo manejas el feedback negativo. ¿Cómo lo usas para mejorar?",
            "En tu experiencia, ¿cómo equilibras las tareas laborales y el trabajo en equipo?"
        ]
        
        for category in categories:
            for i in range(5):  
                question_text = question_pool[i % len(question_pool)]  
                question = Question(
                    text=question_text,
                    category_id=category.id  
                )
                db.add(question)

        db.commit()
        print(f"Se han agregado preguntas para {len(categories)} categorías.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()


def populate_question_categories():
    db = SessionLocal()
    try:
        categories = [
            {"category": "Technical", "description": "Questions related to technical skills."},
            {"category": "Behavioral", "description": "Questions related to behavioral assessment."},
            {"category": "Management", "description": "Questions related to leadership and management skills."},
            {"category": "HR", "description": "Questions related to human resources and company culture."},
            {"category": "Problem-solving", "description": "Questions related to problem-solving and critical thinking."}
        ]
        
        for category in categories:
            question_category = QuestionCategory(
                category=category["category"],
                description=category["description"]
            )
            db.add(question_category)
        
        db.commit()
        print("5 question categories fueron agregadas correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def populate_interview_questions():
    db = SessionLocal()
    try:
        interviews = db.query(Interviews).all()
        questions = db.query(Question).all()

        for interview in interviews:
            for question in questions:
                interview_question = InterviewQuestion(
                    interview_id=interview.id,
                    question_id=question.id
                )
                db.add(interview_question)

        db.commit()
        print(f"Se han asignado preguntas a {len(interviews)} entrevistas.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()
        
def populate_interview_feedback():
    db = SessionLocal()
    try:
        interviews = db.query(Interviews).all()

        if not interviews:
            print("No hay entrevistas para asignar feedback.")
            return
        
        competency_levels = db.query(CompetencyLevel).all()

        if not competency_levels:
            print("No hay niveles de competencia para asignar.")
            return
        
        feedback_pool = [
            "Excelente desempeño, muy preparado para el puesto.",
            "El candidato mostró grandes habilidades técnicas, pero le falta experiencia en trabajo en equipo.",
            "Faltó un poco de claridad en las respuestas, pero mostró un buen nivel de compromiso.",
            "Muy buena comunicación, pero podría mejorar en la toma de decisiones bajo presión.",
            "El candidato tiene mucho potencial, pero debe trabajar en su enfoque hacia los problemas.",
            "El desempeño fue sobresaliente en términos de creatividad y resolución de problemas.",
            "Muy buena presentación personal y claridad en la explicación de conceptos técnicos.",
            "El candidato mostró una actitud positiva, pero necesita mejorar en la gestión del tiempo.",
            "Se destacó en la resolución de conflictos, pero debe mejorar en la comunicación asertiva.",
            "Muy bien en el manejo de situaciones complejas, pero se puede mejorar en la adaptabilidad."
        ]
        
        recommendations_pool = [
            "Recomendaría mejorar la comunicación con los miembros del equipo para lograr mayor eficiencia.",
            "Sería útil que el candidato trabajara en mejorar sus habilidades de organización y gestión del tiempo.",
            "Recomiendo enfocarse más en el trabajo en equipo y aprender a delegar tareas cuando sea necesario.",
            "Sería beneficioso para el candidato asistir a talleres sobre resolución de conflictos.",
            "Recomendaría practicar más entrevistas técnicas para mejorar la rapidez en las respuestas.",
            "Sería bueno que el candidato tuviera más experiencia en proyectos de mayor escala.",
            "Recomiendo que el candidato trabaje en su empatía para mejorar las interacciones con sus compañeros.",
            "Sería ideal que el candidato se exponga a diferentes tipos de proyectos y situaciones para fortalecer su adaptabilidad.",
            "Recomendaría seguir desarrollando habilidades de liderazgo en situaciones de alto estrés.",
            "Sería útil que el candidato se enfoque más en el feedback y en el aprendizaje de los errores."
        ]
        
        for interview in interviews:
            interview_feedback = InterviewFeedback(
                feedback=fake.random_element(feedback_pool),  
                general_score=fake.random_int(min=1, max=10),
                recommendations=fake.random_element(recommendations_pool),  
                interview_id=interview.id,
                clarity_level=competency_levels[0].id, 
                structure_level=competency_levels[1].id,
                communication_level=competency_levels[2].id
            )
            db.add(interview_feedback)
        
        db.commit()
        print(f"Se han agregado feedbacks a {len(interviews)} entrevistas.")
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()


def populate_mistake_categories():
    db = SessionLocal()
    try:
        categories = [
            {"category": "Technical Issue", "description": "Issues related to technical performance."},
            {"category": "Communication Issue", "description": "Issues related to communication problems."},
            {"category": "Behavioral Issue", "description": "Issues related to behavior or attitude."}
        ]
        
        for category in categories:
            mistake_category = MistakeCategory(
                category=category["category"],
                description=category["description"]
            )
            db.add(mistake_category)

        db.commit()
        print("3 Mistake Categories were added successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()
        
def populate_interview_mistakes():
    db = SessionLocal()
    try:
        interview_feedbacks = db.query(InterviewFeedback).all()
        mistake_categories = db.query(MistakeCategory).all()

        for interview_feedback in interview_feedbacks:
            for mistake_category in mistake_categories:
                interview_mistake = InterviewMistake(
                    interview_id=interview_feedback.interview_id,
                    category_id=mistake_category.id
                )
                db.add(interview_mistake)

        db.commit()
        print("Assigned mistake categories to Interview Feedback successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()

def populate_competency_levels():
    db = SessionLocal()
    try:
        competency_levels = [
            {"competency": "Technical", "description": "Related to technical skills.", "level": "Beginner"},
            {"competency": "Behavioral", "description": "Related to behavioral skills.", "level": "Intermediate"},
            {"competency": "Leadership", "description": "Related to leadership skills.", "level": "Advanced"},
            {"competency": "Communication", "description": "Related to communication skills.", "level": "Expert"}
        ]
        
        for competency in competency_levels:
            competency_level = CompetencyLevel(
                competency=competency["competency"],
                description=competency["description"],
                level=competency["level"]
            )
            db.add(competency_level)

        db.commit()
        print("Competency levels were added successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()