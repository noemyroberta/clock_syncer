from concurrent import futures
import grpc
import time
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc

class ClockSyncServicer(rpc.ClockSyncServicer):
    def __init__(self):
        self.server_time = time.time()
        self.slave_times = {}
    
    def Sync(self, _, __):
        return clock.SyncResponse(server_time=int(time.time()))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ClockSyncServicer_to_server(ClockSyncServicer(), server)
    
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:30000')
    server.start()
    print("Server started")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
