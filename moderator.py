import grpc
import sys
import debate_pb2
import debate_pb2_grpc

def run():
    firstArg = sys.argv[1]
    secondArg = sys.argv[2]

    channel = grpc.insecure_channel('localhost:50051')
    stub = debate_pb2_grpc.CandidateStub(channel)

    if (firstArg == "answer"):
        answer = stub.Answer(debate_pb2.AnswerRequest(question=secondArg))    
        print(answer.answer)
    if (firstArg == "elaborate"):        
        numBlahs = [ int(x) for x in sys.argv[3:] ]
        elaboration = stub.Elaborate(debate_pb2.ElaborateRequest(topic=secondArg, blah_run=numBlahs))    
        print(elaboration.answer)        

run()