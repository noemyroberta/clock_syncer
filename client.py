import grpc
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc
import utils
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = rpc.ClockSyncStub(channel)
    response_time_request = stub.GetTime(clock.GetTimeRequest())

    print('Server time is ', response_time_request.time)
    client_time_str = input('What is your time? [##.##] ')
    client_time_float = utils.time_to_float(client_time_str)

    while True:
        time.sleep(3)
        response = stub.Sync(clock.SyncRequest(client_time=client_time_float))

        offset = utils.float_to_time(response.offset)

        client_time_float += offset
        client_time_str = utils.float_to_time(client_time_float)

        print('Adjusted time to ', client_time_str)

if __name__ == '__main__':
    run()
