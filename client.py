import time
import grpc
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc

def run():
    channel = grpc.insecure_channel('localhost:30000')
    stub = rpc.ClockSyncStub(channel)
    
    response = stub.Sync(clock.SyncRequest(client_time=int(time.time())))
    print("Server time:", response.server_time)

if __name__ == '__main__':
    run()
