# Clock Syncer - Guide & Docs

This project works around physical clock syncronization using Berkeley's algorithm with gRPC (Google Remote Procedure Call) technique.

## Berkeley's algorithm approach

### 1. Keywords

- **Master daemon** or **Master node** -> **Server**: The choosen node to reference the clock's offset for slaves.

- **Slave node** -> **Client**: Nodes in the network that requests the master's timestamp.

- **Offset**: The difference between the slave and master nodes time.

### 2. Approach

Pass 1. Time daemon (master node) requests timestamps from all the slave nodes.

Pass 2. Slave nodes responds their timestamps to master node.

Pass 3. Master node computes fault tolerant average.

Pass 4.The average time difference is added to the current time at master's system clock and broadcasted over the network.

## Install

First, you get to clone the repository by running the command:

`git clone https://github.com/noemyroberta/clock_syncer.git`

In order to install and run the code, you need to install all gRPC dependencies by placing the command:

`pip install grpcio grpcio-tools`

---

**NOTE**: You may not need to run the protobuffer generated files, but in that case, you can generate the files by running:

`python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. proto/clock.proto`

Just make sure you use the correct version of `python`.

---

## Run & Test

Ready to get started, you run the server by command line or IDE executor, in this example I'll use the command line for general purposes.

`python3 server.py`

---

**NOTE**: In this case, we don't use the local time properly and actually the server requires it from user (for testing purpose), then you make sure to enter the hour on the indicated format.

---

and right after, the client:

`python3 client.py`

## Result

The expected result must be a new adjusted time for server and client.
