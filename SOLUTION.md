# Lab 6 – Comparing REST and gRPC Remote Procedure Calls

All times are in milliseconds (ms).

| Method          | Local (same host) | Same Zone (us-west1-a) | Different Region (us-west1-a ↔ europe-west3-a) |
|-----------------|------------------:|------------------------:|-----------------------------------------------:|
| REST add        | 0.965             | 4.034                  | 333.791                                        |
| gRPC add        | 0.105             | 1.221                  | 165.033                                        |
| REST rawImage   | 1.786             | 8.773                  | 1310.334                                       |
| gRPC rawImage   | 1.430             | 8.208                  | 346.367                                        |
| REST dotProduct | 1.144             | 4.081                  | 335.656                                        |
| gRPC dotProduct | 0.130             | 0.967                  | 163.097                                        |
| REST jsonImage  | 10.979            | 37.440                 | 1490.544                                       |
| gRPC jsonImage  | 5.413             | 16.367                 | 350.245                                        |
| PING            | 0.154             | 0.409                  | 157                                            |



### **Observations**

- In every test, **gRPC ran faster than REST**. For small requests such as add, the difference was clear, gRPC finished several times quicker both locally and within the same zone.  
- When the message size grew (rawImage or jsonImage), **REST slowed down sharply** because of JSON formatting and HTTP overhead, while gRPC stayed more stable thanks to its binary protocol buffers.  
- Latency rose sharply when traffic went between regions (U.S. to Europe). Most of that delay comes from normal network distance rather than the API itself.  
- The advantage of gRPC becomes most obvious with **larger payloads or higher latency links**, where it uses less bandwidth and fewer CPU cycles to encode data.  
- The ping results line up with these findings: network delay alone was only fractions of a millisecond in the same zone but over a hundred milliseconds across continents.



### **Summary**

- **REST** is easier to build and read, but it carries extra overhead from text encoding and HTTP.  
- **gRPC** sends compact binary data and keeps requests lightweight, which makes it better for frequent or large-volume service calls.  
- In short, **gRPC handled both same-zone and cross-region tests more efficiently**, while REST traded speed for simplicity.

