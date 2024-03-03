import grpc
import threading
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc

def run():
    channel = grpc.insecure_channel('localhost:30000')
    stub = rpc.ClockSyncStub(channel)

    str_time = input('(Client) What time is it? [##:##] ').replace(':', '.')

    response = stub.Sync(clock.SyncRequest(client_time=float(str_time)))
    print("Server time:", response.server_time)

    time_before_adjustment = float(str_time)
    offset = response.server_time - time_before_adjustment
    print('Offset: ', offset)
    adjusted_time = time_before_adjustment + offset
    
    print("Adjusted client time:", adjusted_time)

if __name__ == '__main__':
    thread = threading.Thread(target=run)
    thread.start()

    
