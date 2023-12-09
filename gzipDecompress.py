import gzip
import base64


def decodeGzipBase64():
    print(gzip.decompress(base64.b64decode("")))


if __name__ == "__main__":
    decodeGzipBase64()
