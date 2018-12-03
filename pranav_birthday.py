from __future__ import print_function
import random
import json

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, card_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# ---------------------------- Data for the skill ------------------------------

ques = [["Saurabh","Bro i met u on the day of M.C.A interview. You are a great friend and a good human being. May this year brings you a lot of happiness and joy....keep calm coz gurditta is here"],
        ["Sonam","Prnav join next big boss yar....You would definitely impress every one there becuse you are a really good guy and could win it...."],
        ["Hemant","Happy Bdyyy Bhai Jyada din nhi hue apni dosti ko lekin hm bhut ache dost bne h "],
        ["Pradeep","You know all about me, I know all about you. We’re best friends."],
        ["Tanisha","Happiest biryhday to the most zealous and zestful person i have ever met Janamdin ki hardik shubhkamnaye"],
        ["Nitin","Are bhai bhai bhai bhai, pornhub, i mean pranav, tu iklauta masiha hai ducs ka aur ekmev bhgwan hmara."],
        ["Abhishek","Happiest birthday to the grammar-savvy, tech-savvy, people-savvy guy of DUCS. I wish you more people and more people in your contacts list."],
        ["Tanya","Happy happy happiest birthday to you pranav"],
        ["Ridhi","JAB BHI HO KOI TERE SATH HO TOH BORE HONE KI KOI BAAT NA HO"],
        ["Navya","Show off boy. but sweet ,kind hearted and good human being. khush raho aise hi maje karte raho aur apne contact list badhate raho. Happy birthday to you ladke"],
        ["Shrishti","Wish you a very very Happy Birthday . Pornab(YOU) have a category of Art of Happy Living (with FULL HD CLARITY)"],
        ["Aditya","Very Very Happy Birthday Bhai."],
        ["Sonali","Happy Birthday Praniiii."]
        ]

task = ["Take shorts from someone and wear them.",
           "Mimicry of Pradeep",
        "Go and say to a girl after seeing you I have no mood of making a girlfriend.",
           "Dance on any item song",
           "Propose a boy in SRK pose",
           "Couple dance with hemant",
           "Blind Fold",
           "Daramsharas",
           "Play aam churi chapan churi game with Pradeep",
           "Cat Walk",
           "Give honest reviews about everyone in DUCS Besties",
           "Buy Chocolates for Everyone",
           "Praise the seniors of DUCS."
        ]
hint=["Sweet and Sour relationship with me.",
    "The word starts with a P and synonym is postmortem and postobit.",
    "Your emotional Support in DUCS.",
    "Always goes together wherever you go, we are always together.",
    "Innocent and Lovely Person",
    "The word starts with an E and synonym is communicable and catching.",
    "The word starts with a S and synonym is narcotic and dull.",
    "The word starts with a C and synonym is flesh eating and predatory.",
    "The word starts with a D and synonym is tie and even steven.",
    "The word starts with a M and synonym is crown and kingdom.",
    "The word starts with a M and synonym is unbeliever and pessimist."
    ]

# --------------------------- Global variables ---------------------------------

totalQues = 13
quesInOneSession = 13
maxScore = quesInOneSession

score = 0
currQues = -1
askedQuesCount = 0
askedQues = []
session_attributes = {}
rulecount = 0
quesAnswered = True
tv=0
tdone=True

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "<p>Hello! Welcome to Pranav Birthday! For brief description and rules of this skill, just say <emphasis level='moderate'>rules!</emphasis></p> "\
                    "So, Can we find out how well you know your friends pranav? Say <emphasis level='moderate'>start quiz</emphasis> to get started with the quiz" 
    card_output = "Hello! Welcome to one word phrase game! For brief description and rules of the game, just say rules! "\
                   "So, Can we find out how well you know your friends pranav? Say start quiz to get started with the quiz"              
    reprompt_text = "Hi! I am waiting! " \
                    "Can we get started? Say begin to get started!" 

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))

def result():
    
    init = "Awesome! You completed the the quiz! " + " You got " + str(score) + " out of " + str(quesInOneSession) + " correct. "
    if score == quesInOneSession:
        init = init + " Well done! Perfect score! You really know your friends well! I am impressed! "
    elif score >= (quesInOneSession/1.5)+1:
        init = init + " Nice score! Keep enjoying with friends, will definitely keep getting better! "
    elif score >= (quesInOneSession/2.5)+1:
        init = init + " Great effort! You can do much better, I believe in you! "
    else:
        init = init + " You can do better! Way to go! Play again, get better! "

    init = init + "  Wanna play again? Just say, Replay! Otherwise, say stop!"
    
    return (init)

def result1():
    
    init = "<audio src='soundbank://soundlibrary/human/amzn_sfx_crowd_applause_05'/>"\
            "<say-as interpret-as=\"interjection\">Awesome.</say-as> You completed the phrase game!<break/> " + " You got " + str(score) + " out of " + str(quesInOneSession) + " correct. "
    if score == quesInOneSession:
        init = init + " <say-as interpret-as=\"interjection\">Well Done. Perfect Score!</say-as> <break/>You really know your friends well! I am impressed! "
    elif score >= (quesInOneSession/1.5)+1:
        init = init + " Nice score! Keep enjoying with friends, will definitely keep getting better! "
    elif score >= (quesInOneSession/2.5)+1:
        init = init + " Great effort! You can do much better, I believe in you! "
    else:
        init = init + " You can do better! <say-as interpret-as=\"interjection\">Way to go.</say-as> <break/> Play again, get better! "

    init = init + " Wanna play again? Just say, Replay! Otherwise, say stop! "
    
    return (init)

def ret_question():

    q = ques[currQues][1] + " . "
    return (q)

def phrase(intent, session):

    global askedQuesCount
    global currQues
    global askedQues
    global quesAnswered
    global tv

    card_title = "Wishes"

    if askedQuesCount == 0:
        init = "Alright! Let's see how many friends you know well. "
    else:
        init = ""

    speech_output = ""
    card_output=""
    reprompt_text = ""
    
    if askedQuesCount == quesInOneSession:
         
                speech_output = result1()
                card_output = result()
                reprompt_text = " Hey! Let's play again! Say Replay to play again. Or Exit to stop playing "
                should_end_session = False

                return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))
            
    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "<say-as interpret-as=\"interjection\">Uh oh.</say-as> <break/>Answer the last question I asked you."
        card_output = "Answer the last question I asked you."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))
             
    
    askedQuesCount = askedQuesCount+1   
    quesNo = askedQuesCount
    x=quesNo-1
    #x =  random.randint(0,totalQues-1)
    #while x in askedQues:
     #       x =  random.randint(0,totalQues-1)
        
    askedQues.append(x);
    currQues = x
    
    question = "Question " + str(quesNo) + ".  " + ret_question() 
    
    session_attributes['question'] = ques[x][1]
    
    quesAnswered = False
    ked= True
    
    question1 = "<audio src='soundbank://soundlibrary/musical/amzn_sfx_drum_comedy_02'/> Question " + str(quesNo) + ".  " + ret_question()
    
    speech_output = init+"<break/><emphasis level='moderate'>" + question1+"</emphasis>"
    card_output = init + question
    reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."\
                    "If you want hint then say give me hint"

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    
    #print(b['response']['outputSpeech']['text'])
    
def get_answer(intent, session):

    global score
    global quesAnswered
    global tv


    card_title = "Answer"

    if quesAnswered == True:
        speech_output = "<say-as interpret-as=\"interjection\">Haanji.</say-as> What you are trying to pull buddy?<break/> You have already answered the question."
        card_output = "Haanji! What you are trying to pull buddy? You have already answered the question."
        reprompt_text = "You can move to the next question by saying, next question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    


    if 'value' not in intent['slots']['answer']:
        speech_output = "<say-as interpret-as=\"interjection\">Hello.</say-as>You need to say an answer! Say an answer."
        card_output = "Hello! You need to say an answer! Say an answer."
        reprompt_text = "If you want hint, say hint."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))
        
    ans_input = intent['slots']['answer']['value']

    if ans_input.lower() == ques[currQues][0].lower():
        speak = "That is the correct answer!" + " Say next for the next question."
        speak1= "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_01'/>"\
                "<say-as interpret-as=\"interjection\">Yay.</say-as> That is the correct answer!" + " Say <emphasis level='moderate'>next</emphasis> for the next question."
        score = score + 1
    else:
        speak = "Oh no! That answer is incorrect. The correct answer is " + ques[currQues][0] + ". Say tell me example to know about the correct answer. " 
        speak1= "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_01'/>"\
                "<say-as interpret-as=\"interjection\">Oh no.</say-as>That answer is incorrect. <break/> The correct answer is <emphasis level='moderate'>" + ques[currQues][0] + "</emphasis><break/>."\
                " Your task is "+task[tv]+"<break time='12s'/>"\
                " Say <emphasis level='moderate'>task code</emphasis> to move further.  "
        tv=tv+1
    session_attributes['score']=score
    
    quesAnswered = True
    speech_output = speak1 
    card_output = speak 
    reprompt_text = "You can know more about this question's answer by saying, tell me example. "
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    


def get_next_question(intent, session):

    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "<say-as interpret-as=\"interjection\">Buddy.</say-as> You haven't answered the question yet.<break/> You can't move to the next question."
        card_output = "Buddy! You haven't answered the question yet. You can't move to the next question."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))
        
    return phrase(intent,session)

def repeat_question(intent, session):

    card_title = "Question"

    if currQues == -1:
        speech_output = "<say-as interpret-as=\"interjection\">Buddy.</say-as>The quiz has not started yet!<break/> Say </emphasis level='moderate'>begin </emphasis>to get started with the quiz"
        card_output = "The quiz has not started yet! Say begin to get started with the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    
    
    if quesAnswered == True:
        speak = "Your question was. "
        re = "Say, next question, to move to the next question!"
    else:
        speak = "Your question is. "
        re = "Hey, there! I am waiting for your answer."

    speech_output = speak + ret_question()
    card_output = speak + ret_question()
    reprompt_text = re
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    
    
    
def current_score(intent, session):

    card_title = "Score"

    sc = str(score)
    if askedQuesCount == quesInOneSession:
        speak = "Cool! You finished the quiz! Your final score is "+ sc + ". Say, replay to play again."
        speak1= "<say-as interpret-as=\"interjection\">Cool.</say-as> You finished the quiz! <break/> Your final score is <emphasis level='moderate'>"+sc + ".</emphasis><break/> Say,<emphasis level='moderate'>replay </emphasis> to play again."
        re = "Say replay to start the quiz again! Or say exit to exit the game"
    else:
        if quesAnswered == True:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount) + " questions. Say next question for the next question."
            speak1= "Your score is <emphasis level='moderate'>" + sc + " </emphasis>because you have answered " + sc + " correctly, <break/>out of " + str(askedQuesCount) + " questions. Say next question for the next question.."
            re = "Move to the next question by saying, next question."
        else:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount-1) + " questions. Say my answer is your answer to answer the question."
            speak1= "Your score is <emphasis level='moderate'>" + sc + " </emphasis>because you have answered " + sc + " correctly, <break/>out of " + str(askedQuesCount-1) + " questions. Say my answer is your answer to answer the question."
            re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."

    speech_output = speak1
    card_output = speak
    reprompt_text = re
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    
'''
def tell_me_example(intent, session):

    card_title = "Tell Me Example"

    if quesAnswered == False:
        speak1 = "<say-as interpret-as=\"interjection\">Buddy.</say-as></break/>You can't know about the answer yet! <emphasis level='moderate'>Answer the question first.</emphasis>"
        speak = "Buddy, You can't know about the answer yet! Answer the question first. "
        re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."
    else:
        speak = ansInfo[currQues] + " . Say begin to continue. "
        speak1 = ansInfo[currQues] + " . Say<emphasis level='moderate'> begin</emphasis> to continue. "
        re = "Move to the next question by saying, next question."

    speech_output = speak1
    card_output = speak
    reprompt_text = re
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))  
'''
def give_me_hint(intent, session):

    card_title = "Give Me Hint"

    if quesAnswered == True:
        speak1 = "<say-as interpret-as=\"interjection\">Buddy.</say-as></break/>You can't hint about the question yet! <emphasis level='moderate'>Answer the question first.</emphasis>"
        speak = "You can't hint about the question yet! Let me ask the question first. "
        re = "I am waiting for asking you the question! Say, next question, if you want me to continue further to next question."
    else:
        speak = hint[currQues] + " . Answer the question now "
        speak1 = hint[currQues] + " .<break time='1s'/> Answer the question now "
        re = "Answer the question by saying, my answer is word."

    speech_output = speak1
    card_output = speak
    reprompt_text = re
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session)) 

def replay_quiz(intent, session):
    
    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered
    global quesAsked
    global tv
    
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    session_attributes = {}
    quesAnswered = True
    tv=0
    
    return phrase(intent, session)    


def no_response():

    card_title = "No!"
    
    speech_output = "<say-as interpret-as=\"interjection\">Sorry Buddy.</say-as></break/> I don't understand!"
    card_output = "Sorry buddy, I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    
        
def yes_response():

    card_title = "Yes!"
    
    speech_output = "<say-as interpret-as=\"interjection\">Well well.</say-as> nice trying but I don't understand!"\
                    " If you want to answer the given question then just say,<emphasis level='moderate'> my answer is word.</emphasis>"
    card_output = "Well well! Nice trying but I don't understand!"\
                " If you want to answer a given question then just say, my answer is word."
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))    

    
def get_help_response(intent, session):
    
    global rulecount
    
    card_title = "Rules"
    #session_attributes={}
    should_end_session = False
    
    rulecount = rulecount + 1
    if rulecount == 1:
        speech_output = "This is a one word english phrase quiz and the rules are very simple. " \
                        "I will ask you a question. You say one word by saying, my answer is word "\
                        "I will tell you, if you were correct. Move to the next question by saying next. "
        speech_output1 = "This is a one word english phrase quiz and the rules are very simple. <break/>" \
                        "I will ask you a question. You say one word by saying, <emphasis level = 'moderate'> my answer is word </emphasis>"\
                        "<break/>I will tell you, if you were correct. <break/> "\
                        "Move to the next question by saying <emphasis level='moderate' > next. </emphasis>"
        #rulecount=0
    else:
        speech_output = "Hello! Welcome to Guess Me! " \
                        "This is a one word elglish phrase quiz and the rules are very simple. " \
                        "After you start the game, you will be prompted with a question. "\
                        "You have to say one word answer, by saying, my answer is your answer like democracy " \
                        "After you answer the question, I will tell you, whether you were right, or not. Then say, next question, to move to the next question. "\
                        "You can get a question repeated, by saying, Repeat question."\
                        "You can also know more about the answer, of a question, by saying, tell me example. "\
                        "You can also get a hint for the question, by saying, hint "\
                        "You will be asked 5 questions. You will get the final score after the game. To get your score between the game, you can ask, what is my score. "\
                        "To exit the skill, say stop."
        
        speech_output1= "Hello! Welcome to <emphasis level='moderate'>Guess Me!</emphasis> <break/>"\
                        "This is a one word english phrase quiz and the rules are very simple. <break/>" \
                        "After you start the game, you will be prompted with a question. <break/>"\
                        "You have to say one word answer, by saying,<emphasis level = 'moderate'> my answer is your answer like democracy. </emphasis> <break/>" \
                        "After you answer the question, I will tell you, whether you were right, or not. Then say, <emphasis level= 'moderate'> next question</emphasis>, to move to the next question. <break/>"\
                        "You can get a question repeated, by saying, <emphasis level='moderate'> Repeat question</emphasis><break/>"\
                        "You can also know more about the answer, of a question, by saying, <emphasis level='moderate' >tell me example. </emphasis><break/>"\
                        "You can also get a hint for the question, by saying <emphasis level='moderate'> hint.</emphasis>"\
                        "You will be asked <emphasis level='strong'>5 questions</emphasis>. You will get the final score after the game. To get your score between the game, you can ask, <emphasis level = 'moderate' >what is my score.</emphasis> "\
                        "To exit the skill, say stop."
        rulecount = 0                
    #session_attributes['rulecount'] = rulecount
    if askedQuesCount == 0:
        speech_output = speech_output + "That's all! We're all set to begin! Say begin to get started!"
        speech_output1 = speech_output1 + "That's all! <break time='1s'/>We're all set to begin! Say <emphasis level='moderate'>begin</emphasis> to get started!"
    else:
        speech_output = speech_output + "Alright! Shall we continue? Say begin to continue!"
        speech_output1 = speech_output1 + "Alright!<break time='1s'/> Shall we continue? Say <emphasis level='moderate'>begin</emphasis> to continue!"
                    
    speech_output = speech_output1 + " For detailed rules, say <emphasis level='moderate'>rules</emphasis> again. "
    card_output = speech_output + " For detailed rules, say rules again. "
    reprompt_text = "Hey there! What are you waiting for? " \
                    "Say begin!"
                    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, card_output, reprompt_text, should_end_session))

def handle_session_end_request():

    card_title = "Session Ended"
    speech_output = "<say-as interpret-as=\"interjection\">All for now folks.</say-as>"\
                    "I hope you had fun!<break/> " \
                    "Good day!<break/> Come back for more!<break/> Goodbye!"\
                    "<say-as interpret-as=\"interjection\">Ta ta! See you later.</say-as>"
    card_output = "All for now folks! "\
                    "I hope you had fun! " \
                    "Good day! Come back for more! Goodbye!"\
                    " Ta ta! See you later!"
                    
    should_end_session = True
    
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):

    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered
    global tv

    session_attributes = {}
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    quesAnswered = True
    tv=0

def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent)
    
    if intent_name == "QuizIntent":
        return phrase(intent, session)
    elif intent_name == "AnswerIntent":
        return get_answer(intent, session)
    elif intent_name == "NextQuestionIntent":
        return get_next_question(intent, session)
    elif intent_name == "RepeatQuestionIntent":
        return repeat_question(intent, session)
    elif intent_name == "ReplayIntent":
        return replay_quiz(intent, session)
    elif intent_name == "WhatsMyScoreIntent":
        return current_score(intent, session)
    elif intent_name == "TellMeExampleIntent":
        return tell_me_example(intent, session)
    elif intent_name=="GiveMeHintIntent":
        return give_me_hint(intent,session)
    elif intent_name == "NoIntent":
        return no_response(intent, session)
    elif intent_name == "YesIntent":
        return yes_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(intent,session)
   # elif intent_name== "AMAZON.FallbackIntent":
    #    return fallbackfunction()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        
def on_session_ended(session_ended_request, session):
    session_attributes = {}

# --------------- Main handler ------------------

session_attributes = {}

def lambda_handler(event, context):
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
	   
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])