import grpc
import time
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc

class ClockSyncServicer(rpc.ClockSyncServicer):
    def Sync(self, request, context):
        return clock.SyncResponse(server_time=int(time.time()))

def serve():
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    rpc.add_ClockSyncServicer_to_server(ClockSyncServicer(), server)
    server.add_insecure_port('[::]:30000')
    server.start()
    print("Server started")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
