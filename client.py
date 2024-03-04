import grpc
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc
import utils


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = rpc.ClockSyncStub(channel)
    response_time_request = stub.GetTime(clock.GetTimeRequest())

    if (response_time_request.time != None):
        print('(Server) My time is ', response_time_request.time)
        client_time_str = input(
            '(Client) What is your time? [##.##] ')

        converted_client_time = utils.time_to_float(client_time_str)
        response = stub.Sync(clock.SyncRequest(
            client_time=converted_client_time))

        server_time_str = utils.float_to_time(response.server_time)
        print('(Server) My new time is: ', server_time_str)

        client_time_before_adjustment = converted_client_time
        offset = response.server_time - client_time_before_adjustment
        adjusted_time = client_time_before_adjustment + offset
        adjusted_time_str = utils.float_to_time(adjusted_time)

        print('(Client) Adjusted time to ', adjusted_time_str)


if __name__ == '__main__':
    run()
