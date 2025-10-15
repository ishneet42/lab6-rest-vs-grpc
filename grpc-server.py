#!/usr/bin/env python3
import grpc
from concurrent import futures
import rpc_pb2, rpc_pb2_grpc
from PIL import Image
import io, base64

class ImageMathServicer(rpc_pb2_grpc.ImageMathServicer):
    def Add(self, request, context):
        return rpc_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.data))
            w, h = img.size
            return rpc_pb2.ImageReply(width=w, height=h)
        except Exception:
            return rpc_pb2.ImageReply(width=0, height=0)

    def DotProduct(self, request, context):
        a, b = request.a, request.b
        dot = sum(x * y for x, y in zip(a, b))
        return rpc_pb2.DotReply(dot_product=dot)

    def JsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.image)
            img = Image.open(io.BytesIO(img_bytes))
            w, h = img.size
            return rpc_pb2.ImageReply(width=w, height=h)
        except Exception:
            return rpc_pb2.ImageReply(width=0, height=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc_pb2_grpc.add_ImageMathServicer_to_server(ImageMathServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()