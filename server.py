from concurrent import futures
import grpc
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc
from operator import neg
import utils


class ClockSyncServicer(rpc.ClockSyncServicer):
    def __init__(self, server_time: float):
        self.server_time = server_time
        self.clients_time = {}

    def Sync(self, request, context):
        client_address = context.peer()
        client_time = round(request.client_time, 2)
        self.clients_time[client_address] = client_time
        offset = get_average_offset(servicer)
        update_server_time(servicer, offset)

        client_offset = self.server_time - client_time
        return clock.SyncResponse(offset=client_offset)

    def GetTime(self, _, __):
        return clock.TimeInfo(time=self.server_time)


def update_server_time(self, offset):
    self.server_time += offset
    server_time_str = utils.float_to_time(self.server_time)
    print(f'Server new time is ', server_time_str)


def _get_average_time(servicer):
    sum_clients_time = sum(servicer.clients_time.values())
    sum_clients_time += servicer.server_time
    len_clients = len(servicer.clients_time) + 1

    return sum_clients_time / len_clients


def get_average_offset(servicer):
    times = servicer.clients_time.values()
    average_time = _get_average_time(servicer)
    offsets = [time - average_time for time in times]
    average_offset = sum(offsets) / len(offsets)
    return average_offset


def serve(servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ClockSyncServicer_to_server(servicer, server)

    print('Starting server. Listening...')
    server.add_insecure_port('localhost:50051')
    server.start()
    print("Server started")
    server.wait_for_termination()


if __name__ == '__main__':
    server_time_str = input('What time is it? [##:##] ')
    converted_server_time = utils.time_to_float(server_time_str)
    servicer = ClockSyncServicer(server_time=converted_server_time)
    serve(servicer)
