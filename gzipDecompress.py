import gzip
import base64


def decodeGzipBase64(resultTrack):
    return gzip.decompress(base64.b64decode(resultTrack))
    

if __name__ == "__main__":
    decodeGzipBase64()
