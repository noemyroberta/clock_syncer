from concurrent import futures
import grpc
import threading
import time
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc


class ClockSyncServicer(rpc.ClockSyncServicer):
    def __init__(self, server_time: float):
        self.server_time = server_time
        self.clients_time = {}

    def Sync(self, request, context):
        client_address = context.peer()
        print(f'Client {client_address} requested for sync')
        self.clients_time[client_address] = request.client_time
        offset = get_offset(self)
        self.server_time += offset
        return clock.SyncResponse(server_time=float(offset))

    def GetTime(self, _, context):
        new_client = context.peer()
        print(f'Client {new_client} requested for server time')
        self.clients_time[new_client] = None
        return clock.TimeInfo(time=self.server_time)

    def UpdateTime(self, request, _):
        return clock.UpdateTimeResponse()


def get_offset(servicer):
    print('Clients: ', servicer.clients_time)

    # NOTE: sleep until there's more than one client connected
    while len(servicer.clients_time) <= 1:
        time.sleep(1)

    len_nodes = len(servicer.clients_time) + 1
    sum_nodes_time = sum(servicer.clients_time.values()) + servicer.server_time

    # NOTE: decrease server_time to remove the "hour"
    average_offset = sum_nodes_time / len_nodes

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
    server_time_str = input('What time is it? [##:##] ').replace(':', '.')
    servicer = ClockSyncServicer(server_time=float(server_time_str))
    serve(servicer)