from concurrent import futures
import grpc
import threading
import time
import proto.clock_pb2 as clock
import proto.clock_pb2_grpc as rpc

class ClockSyncServicer(rpc.ClockSyncServicer):
    def __init__(self):
        self.server_time = time.time()
        self.slave_times = {}
    
    def Sync(self, _, __):
        return clock.SyncResponse(server_time=int(time.time()))
    
    def GetTime(self, _, __):
        return clock.TimeInfo(time=int(time.time()))

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
            time.sleep(5) 

    def adjust_slave_times(self, slave_stubs):
        while True:
            if len(self.servicer.slave_times) > 0:
                len_slave_times = len(self.servicer.slave_times)
                counter_slave_times = sum(self.servicer.slave_times.values())

                average_offset =  counter_slave_times/ len_slave_times - self.servicer.server_time
                
                for _, stub in slave_stubs.items():
                    stub.UpdateTime(clock.UpdateTimeRequest(offset=average_offset))
            
            # NOTE: set it later if is needed
            time.sleep(10)


    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rpc.add_ClockSyncServicer_to_server(ClockSyncServicer(), server)
        
        print('Starting server. Listening...')
        server.add_insecure_port('[::]:30000')
        server.start()
        print("Server started")
        server.wait_for_termination()

if __name__ == '__main__':
    server = Server(ClockSyncServicer())
    server.serve()

    slave_addresses = ['localhost:30010', 'localhost:30012']
    slave_stubs = {address: rpc.ClockSyncStub(grpc.insecure_channel(address)) for address in slave_addresses}

    update_thread = threading.Thread(target=server.update_slave_times(slave_stubs))
    update_thread.daemon = True
    update_thread.start()

    adjust_thread = threading.Thread(target=server.adjust_slave_times(slave_stubs))
    adjust_thread.daemon = True
    adjust_thread.start()
