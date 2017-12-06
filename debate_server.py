import grpc

import debate_pb2
import debate_pb2_grpc
import consultation_pb2
import consultation_pb2_grpc
import time
from random import *
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def questionCheck(question):    
    words = ['who','what','when','how','why']
    firstWord = question.split(" ")
    if (firstWord[0].lower() in words):
        return True
    else:
        return False    

def defaultAnswer():
    answers = ["your 3 cent titanium tax goes too far", 
                "your 3 cent titanium tax doesn't go too far enough"]
    return answers[randint(0, 1)]

def dynamicAnswer(question):
    question = question.split(" ")    
    for i in range(0, len(question)):
        if question[i] == "you":
            question[i] = "I"
        elif question[i] == "your":
            question[i] = "my"
    return " ".join(question)

def consult(question):
    channel = grpc.insecure_channel('23.236.49.28:50051')
    stub = consultation_pb2_grpc.CampaignManagerStub(channel)
    retort = stub.Retort(consultation_pb2.RetortRequest(original_question=question))    
    return "You asked me " + question + " but I want to say that " + retort.retort

def elaborate(topic, numArray):
    blahList = []
    for num in numArray:
        blahs = ""
        for i in range(0, num):
            if (blahs == ""):
                blahs += "blah"
            else:
                blahs += " blah"
            if (i == num-1):
                blahList.append(blahs)

    topic = " " + topic + " "
    return topic.join(blahList)

class Candidate(debate_pb2_grpc.CandidateServicer):    
    def Answer(self, request, context):
        if (questionCheck(request.question) is False ):
            answer = defaultAnswer()
            return debate_pb2.AnswerReply(answer=answer)
        else:
            switch = dynamicAnswer(request.question)
            answer = consult(switch)
            return debate_pb2.AnswerReply(answer=answer)        

    def Elaborate(self, request, context):
        elaboration=elaborate(request.topic, request.blah_run)
        return debate_pb2.AnswerReply(answer=elaboration)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    debate_pb2_grpc.add_CandidateServicer_to_server(Candidate(), server)
    server.add_insecure_port('[::]:50051')
    server.start()  
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

serve()
