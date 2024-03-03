import grpc
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = rpc.ClockSyncStub(channel)
    response_time_request = stub.GetTime(clock.GetTimeRequest())

    if (response_time_request.time != None):
        print('(Server) My time is ', response_time_request.time)
        client_time_str = input('(Client) What is your time? [##.##] ').replace(':', '.')
        response = stub.Sync(clock.SyncRequest(client_time=float(client_time_str)))
        print('RESPONSE: ', response.server_time)


if __name__ == '__main__':
    run()
