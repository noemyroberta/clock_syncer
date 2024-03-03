from concurrent import futures
from datetime import datetime
import grpc
import threading
import time
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc


class ClockSyncServicer(rpc.ClockSyncServicer):
    def __init__(self, server_time: float):
        self.server_time = server_time
        self.slave_times = {}

    def Sync(self, _, __):
        return clock.SyncResponse(server_time=float(self.server_time))

    def GetTime(self, _, __):
        return clock.TimeInfo(time=float(self.server_time))

    def UpdateTime(self, request, _):
        self.server_time += request.offset
        return clock.UpdateTimeResponse()


class Server():
    def __init__(self, servicer):
        self.servicer = servicer

    def update_slave_times(self, slave_stubs):
        while True:
            for slave_address, stub in slave_stubs.items():
                response = stub.GetTime(clock.GetTimeRequest())
                self.servicer.slave_times[slave_address] = response.time
            # NOTE: set it later if is needed
            time.sleep(10)

    def adjust_slave_times(self, slave_stubs):
        while True:
            if len(self.servicer.slave_times) > 0:
                len_slave_times = len(self.servicer.slave_times)
                counter_slave_times = sum(self.servicer.slave_times.values())

                average_offset = counter_slave_times / \
                    len_slave_times - self.servicer.server_time

                for _, stub in slave_stubs.items():
                    stub.UpdateTime(clock.UpdateTimeRequest(
                        offset=average_offset))

            # NOTE: set it later if is needed
            time.sleep(10)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rpc.add_ClockSyncServicer_to_server(self.servicer, server)

        print('Starting server. Listening...')
        server.add_insecure_port('[::]:30000')
        server.start()
        print("Server started")
        server.wait_for_termination()


if __name__ == '__main__':
    server_time_str = input(
        '(Server) What time is it? [##:##]').replace(':', '.')

    servicer = ClockSyncServicer(server_time=float(server_time_str))
    server = Server(servicer)
    server.serve()

    slave_addresses = ['localhost:30000']
    slave_stubs = {address: rpc.ClockSyncStub(
        grpc.insecure_channel(address)) for address in slave_addresses}

    update_thread = threading.Thread(
        target=server.update_slave_times(slave_stubs))
    update_thread.daemon = True
    update_thread.start()

    adjust_thread = threading.Thread(
        target=server.adjust_slave_times(slave_stubs))
    adjust_thread.daemon = True
    adjust_thread.start()
