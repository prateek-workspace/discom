import google.generativeai as genai
from django.conf import settings
import random
import string
from ..models import Quiz, QuizQuestion

# Configure the API
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_quiz_id():
    # Generate a random 6-character alphanumeric quiz ID
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_ai_response(message_text):
    try:
        # Use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(
            f"""As a knowledgeable and friendly AI assistant, provide a clear and well-structured response to the following question:

            Question: {message_text}

            Format your response as follows:
            
            💡 Answer:
            [Provide a concise but comprehensive answer]

            🔍 Additional Context:
            [Provide relevant background information or examples]

            💭 Pro Tips:
            • [Helpful tip 1]
            • [Helpful tip 2]
            • [Helpful tip 3]

            Keep the tone friendly and professional, and ensure explanations are easy to understand."""
        )
        
        return response.text
    except Exception as e:
        return f"Error generating AI response: {str(e)}" 

def get_summary(content):
    try:
        # Use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate summary
        response = model.generate_content(
            f"""Please provide a clear and comprehensive summary of the following content:

            {content}
            
            Format your response as follows:

            📝 Executive Summary:
            [A concise 2-3 sentence overview of the main content]

            🎯 Key Points:
            • [Major point 1 with brief explanation]
            • [Major point 2 with brief explanation]
            • [Major point 3 with brief explanation]

            🔍 Detailed Analysis:
            [Break down complex concepts into simple, clear explanations]

            💡 Important Takeaways:
            1. [Key takeaway 1]
            2. [Key takeaway 2]
            3. [Key takeaway 3]

            Keep the language clear and professional, avoiding jargon when possible."""
        )
        
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def get_grade(content):
    try:
        # Use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate grading analysis
        response = model.generate_content(
            f"""As an expert academic evaluator, provide a comprehensive analysis of the following assignment:

            Assignment Content:
            {content}
            
            Format your response as follows:

            📊 Quality Assessment:
            ┌──────────────────────┬─────────┬────────────────────────┐
            │ Criteria            │ Score   │ Quick Feedback         │
            ├──────────────────────┼─────────┼────────────────────────┤
            │ Content Quality     │ [_/10]  │ [Brief comment]        │
            │ Structure          │ [_/10]  │ [Brief comment]        │
            │ Language & Grammar  │ [_/10]  │ [Brief comment]        │
            └──────────────────────┴─────────┴────────────────────────┘

            🤖 AI Detection Analysis:
            • Probability: [High | Medium | Low]
            • Key Indicators:
              - [Specific indicator 1]
              - [Specific indicator 2]
              - [Specific indicator 3]

            🔍 Originality Check:
            • Originality Score: [_/10]
            • Potential Concerns:
              - [Concern 1, if any]
              - [Concern 2, if any]
            • Strengths:
              - [Strength 1]
              - [Strength 2]

            💯 Final Evaluation:
            • Grade: [A/B/C/D/F]
            • Overall Score: [_/100]

            📈 Summary Statistics:
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            Content: [_/10] | AI Prob: [_%] | Originality: [_/10] | Grade: [_]
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            💡 Improvement Suggestions:
            1. [Specific actionable suggestion 1]
            2. [Specific actionable suggestion 2]
            3. [Specific actionable suggestion 3]

            Keep learning! 📚"""
        )
        
        return response.text
    except Exception as e:
        return f"Error analyzing assignment: {str(e)}"

def get_quiz(topic, user):
    try:
        # Use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate a unique quiz ID
        quiz_id = generate_quiz_id()
        while Quiz.objects.filter(quiz_id=quiz_id).exists():
            quiz_id = generate_quiz_id()
        
        # Create the quiz in database
        quiz = Quiz.objects.create(
            quiz_id=quiz_id,
            topic=topic,
            created_by=user
        )
        
        # Generate quiz content
        response = model.generate_content(
            f"""Generate an engaging 10-question quiz on {topic}. For each question, provide:
            1. Question text
            2. Four options (A, B, C, D)
            3. The correct answer
            4. A detailed explanation
            
            Format: JSON array of 10 objects with keys: question, options (array), correct_answer, explanation"""
        )
        
        # Parse the response and store questions
        questions_data = eval(response.text)  # Note: In production, use proper JSON parsing
        for i, q in enumerate(questions_data, 1):
            QuizQuestion.objects.create(
                quiz=quiz,
                question_number=i,
                question_text=q['question'],
                option_a=q['options'][0],
                option_b=q['options'][1],
                option_c=q['options'][2],
                option_d=q['options'][3],
                correct_answer=q['correct_answer'],
                explanation=q['explanation']
            )
        
        # Format the quiz for display
        return f"""
            ╔══════════════════════════════════════════════════════════╗
            ║                     📚 {topic} Quiz                      ║
            ╠══════════════════════════════════════════════════════════╣
            ║ 🎯 Instructions:                                         ║
            ║ • Time Limit: 15 minutes                                ║
            ║ • Each question: 10 points                              ║
            ║ • Total points: 100                                     ║
            ║ • Quiz ID: #{quiz_id}                                   ║
            ╠══════════════════════════════════════════════════════════╣
            ║                      📝 Questions                        ║
            ╠══════════════════════════════════════════════════════════╣

            {"".join(f'''
            Q{q.question_number}. {q.question_text}
               ┌──────────────────────────────────────────────────────┐
               │ A) {q.option_a}                                      │
               │ B) {q.option_b}                                      │
               │ C) {q.option_c}                                      │
               │ D) {q.option_d}                                      │
               └──────────────────────────────────────────────────────┘
            ''' for q in quiz.questions.all())}

            ╠══════════════════════════════════════════════════════════╣
            ║ 📋 How to Submit:                                       ║
            ║ Use the /check command with your Quiz ID and answers:   ║
            ║ /check #{quiz_id} A,B,C,D,A,B,C,D,A,B                 ║
            ╚══════════════════════════════════════════════════════════╝

            Good luck! 🍀"""
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def check_quiz_answers(quiz_id, answers):
    try:
        # Get the quiz from database
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        answers = answers.upper().split(',')
        
        if len(answers) != 10:
            return "❌ Error: Please provide exactly 10 answers."
        
        # Get all questions in order
        questions = quiz.questions.order_by('question_number')
        correct_count = 0
        result_rows = []
        
        # Check each answer
        for q, ans in zip(questions, answers):
            is_correct = q.correct_answer == ans
            if is_correct:
                correct_count += 1
            result_rows.append(f"│ {q.question_number:2d}     │ {ans:10s} │ {'✓' if is_correct else '✗':7s} │ {q.question_text[:30]:30s} │")
        
        score = correct_count * 10
        
        return f"""
            📝 Quiz Results
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            Question-wise Analysis:
            ┌────────┬────────────┬─────────┬────────────────────────┐
            │ Q.No   │ Your Ans   │ Correct │ Question               │
            ├────────┼────────────┼─────────┼────────────────────────┤
            {"".join(result_rows)}
            └────────┴────────────┴─────────┴────────────────────────┘

            📊 Performance Summary:
            • Correct Answers: {correct_count}/10
            • Total Score: {score}/100
            • Accuracy: {score}%

            To see detailed explanations, use:
            /explain-quiz {quiz_id}
            """
    except Quiz.DoesNotExist:
        return f"❌ Error: Quiz with ID #{quiz_id} not found."
    except Exception as e:
        return f"Error checking answers: {str(e)}"

def explain_quiz(quiz_id):
    try:
        # Get the quiz from database
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        questions = quiz.questions.order_by('question_number')
        
        explanations = []
        for q in questions:
            explanations.append(f"""
            Q{q.question_number}. {q.question_text}
               ┌──────────────────────────────────────────────────────┐
               │ ✅ Correct Answer: {q.correct_answer}) {getattr(q, f'option_{q.correct_answer.lower()}')} │
               └──────────────────────────────────────────────────────┘
               
               📝 Explanation:
               {q.explanation}
               
               ──────────────────────────────────────────────────────""")
        
        return f"""
            ╔══════════════════════════════════════════════════════════╗
            ║                   📚 Quiz Explanations                   ║
            ║                     Quiz ID: #{quiz_id}                  ║
            ╠══════════════════════════════════════════════════════════╣

            {"".join(explanations)}

            ╠══════════════════════════════════════════════════════════╣
            ║                    🎯 Key Takeaways                      ║
            ╠══════════════════════════════════════════════════════════╣
            ║ • Review questions you got wrong                         ║
            ║ • Practice similar questions to improve                  ║
            ║ • Use explanations to understand concepts better         ║
            ╚══════════════════════════════════════════════════════════╝

            📚 Keep learning and practicing!"""
    except Quiz.DoesNotExist:
        return f"❌ Error: Quiz with ID #{quiz_id} not found."
    except Exception as e:
        return f"Error generating explanations: {str(e)}"