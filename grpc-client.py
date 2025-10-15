#!/usr/bin/env python3
import grpc, rpc_pb2, rpc_pb2_grpc, random, base64, time
from PIL import Image

def doAdd(stub, debug=False):
    response = stub.Add(rpc_pb2.AddRequest(a=5, b=10))
    if debug: print("Add result:", response.sum)

def doRawImage(stub, debug=False):
    with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
        data = f.read()
    response = stub.RawImage(rpc_pb2.ImageData(data=data))
    if debug: print("RawImage:", response.width, response.height)

def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    response = stub.DotProduct(rpc_pb2.Vectors(a=a, b=b))
    if debug: print("DotProduct:", response.dot_product)

def doJsonImage(stub, debug=False):
    with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    response = stub.JsonImage(rpc_pb2.JsonImageData(image=encoded))
    if debug: print("JsonImage:", response.width, response.height)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
        sys.exit(1)

    host = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])
    addr = f"{host}:50051"

    with grpc.insecure_channel(addr) as channel:
        stub = rpc_pb2_grpc.ImageMathStub(channel)
        print(f"Running {reps} reps against {addr} using {cmd}")

        start = time.perf_counter()
        for _ in range(reps):
            if cmd == "add":
                doAdd(stub)
            elif cmd == "rawImage":
                doRawImage(stub)
            elif cmd == "dotProduct":
                doDotProduct(stub)
            elif cmd == "jsonImage":
                doJsonImage(stub)
            else:
                print("Unknown command")
                sys.exit(1)
        delta = ((time.perf_counter() - start)/reps)*1000
        print("Took", delta, "ms per operation")
