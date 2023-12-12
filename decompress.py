import base64
import json
import os
import shutil
import re
from gzipDecompress import decodeGzipBase64 as dGB
from imageTrim import crop_image_from_url as ci
import uuid


# Initialize variables
answerLabel = ["A. ", "B. ", "C. ", "D. "]
file_directory = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "questionlist.htm")
charMap = []
mappingTable = [[36, 193, 153, 35, 139, 221, 226, 151, 137, 143, 189, 251, 183, 9, 148, 67, 107, 214, 237, 225, 122, 138, 3, 119, 179, 120, 98, 196, 218, 222, 19, 149, 94, 34, 187, 55, 228, 197, 0, 163, 230, 43, 170, 53, 111, 81, 220, 160, 127, 216, 201, 195, 68, 62, 135, 175, 252, 250, 109, 113, 239, 123, 7, 248, 156, 232, 207, 79, 155, 180, 4, 63, 54, 96, 236, 112, 45, 177, 93, 204, 141, 66, 128, 16, 38, 104, 30, 76, 69, 92, 146, 224, 176, 129, 182, 132, 245, 28, 33, 80, 243, 134, 64, 44, 41, 212, 83, 87, 238, 88, 86, 246, 169, 253, 200, 254, 39, 249, 12, 161, 181, 140, 72, 198, 50, 124, 22, 215, 8, 65, 78, 5, 231, 210, 90, 145, 159, 91, 15, 213, 13, 242, 117, 26, 171, 49, 60, 255, 172, 152, 209, 57, 241, 100, 162, 71, 191, 84, 10, 206, 75, 2, 59, 47, 32, 219, 154, 108, 1, 11, 133, 106, 223, 25, 147, 24, 89, 95, 48, 97, 74, 23, 234, 20, 73, 17, 18, 58, 77, 235, 150, 27, 168, 178, 144, 31, 105, 157, 186, 184, 205, 158, 121, 174, 37, 165, 70, 203, 56, 142, 6, 229, 208, 227, 110, 116, 233, 46, 192, 247, 190, 126, 167, 29, 130, 114, 101, 217, 21, 173, 82, 115, 125, 103, 199, 185, 118, 166, 61, 202, 188, 99, 240, 40, 51, 131, 136, 211, 244, 85, 102, 42, 194, 14, 52, 164], [195, 167, 247, 55, 12, 117, 123, 9, 41, 109, 234, 50, 140, 71, 210, 146, 13, 244, 164, 61, 255, 69, 191, 82, 53, 24, 31, 237, 34, 170, 48, 72, 184, 232, 214, 87, 62, 29, 158, 5, 2, 151, 153, 104, 21, 228, 206, 20, 208, 157, 132, 126, 97, 118, 203, 28, 250, 25, 106, 26, 58, 134, 241, 182, 39, 54, 36, 6, 89, 180, 231, 221, 92, 73, 156, 115, 16, 127, 84, 145, 173, 7, 202, 122, 137, 98, 105, 30, 107, 129, 111, 131, 225, 43, 189, 187, 130, 148, 102, 233, 194, 101, 223, 65, 74, 96, 160, 213, 59, 113, 64, 252, 149, 235, 177, 60, 22, 83, 67, 116, 251, 75, 144, 216, 17, 42, 246, 176, 136, 76, 10, 179, 238, 81, 186, 128, 108, 121, 224, 51, 95, 114, 159, 211, 35, 142, 230, 90, 110, 46, 15, 93, 139, 207, 193, 198, 70, 14, 66, 91, 79, 57, 47, 254, 152, 40, 8, 52, 171, 0, 205, 199, 133, 32, 190, 174, 212, 248, 1, 200, 197, 188, 155, 11, 196, 68, 94, 44, 78, 23, 99, 88, 86, 240, 227, 120, 154, 143, 85, 45, 150, 169, 125, 242, 162, 226, 19, 161, 253, 172, 181, 112, 245, 77, 218, 219, 18, 166, 192, 147, 141, 124, 243, 4, 37, 204, 249, 185, 178, 215, 209, 103, 138, 239, 168, 236, 27, 135, 33, 80, 220, 3, 63, 183, 175, 163, 49, 217, 165, 119, 100, 229, 56, 38, 222, 201], [57, 61, 35, 238, 120, 134, 127, 226, 113, 98, 56, 45, 231, 51, 247, 66, 132, 88, 140, 48, 201, 219, 240, 32, 43, 17, 188, 128, 225, 196, 159, 67, 60, 16, 192, 165, 92, 227, 34, 255, 122, 70, 50, 213, 102, 136, 96, 62, 26, 161, 244, 82, 185, 5, 172, 129, 116, 19, 178, 139, 214, 156, 99, 64, 14, 216, 112, 125, 209, 207, 137, 186, 144, 123, 109, 228, 131, 15, 204, 170, 23, 118, 124, 24, 111, 83, 248, 135, 71, 115, 78, 121, 224, 152, 199, 166, 4, 243, 38, 37, 179, 75, 163, 18, 30, 49, 174, 13, 103, 68, 162, 74, 42, 218, 130, 151, 114, 87, 31, 149, 198, 223, 160, 90, 53, 229, 245, 22, 146, 252, 29, 44, 101, 12, 200, 8, 241, 110, 133, 2, 239, 232, 81, 91, 197, 73, 184, 249, 3, 108, 211, 76, 69, 187, 205, 251, 80, 126, 20, 95, 157, 190, 206, 235, 119, 155, 40, 164, 237, 59, 183, 250, 147, 212, 145, 203, 85, 175, 54, 25, 222, 84, 6, 195, 117, 253, 233, 208, 65, 242, 27, 93, 7, 138, 89, 97, 180, 86, 158, 46, 210, 39, 11, 47, 0, 169, 106, 1, 52, 94, 202, 77, 41, 72, 189, 148, 150, 142, 104, 254, 28, 193, 176, 173, 141, 220, 21, 10, 246, 107, 63, 9, 177, 167, 33, 191, 182, 36, 217, 236, 234, 79, 143, 221, 100, 153, 181, 154, 230, 55, 171, 215, 194, 58, 168, 105], [101, 39, 170, 1, 124, 68, 40, 58, 88, 203, 107, 3, 93, 166, 172, 239, 161, 182, 181, 244, 19, 77, 223, 204, 35, 80, 154, 224, 104, 254, 178, 16, 201, 114, 145, 149, 157, 92, 249, 233, 218, 50, 132, 44, 95, 42, 160, 226, 175, 200, 242, 188, 143, 151, 48, 72, 220, 126, 207, 237, 216, 41, 245, 180, 23, 222, 82, 122, 121, 115, 196, 22, 165, 140, 5, 18, 250, 20, 176, 135, 153, 228, 139, 255, 94, 171, 78, 147, 8, 27, 13, 31, 234, 183, 179, 70, 136, 142, 152, 112, 128, 197, 9, 205, 238, 89, 123, 187, 6, 214, 198, 117, 130, 60, 76, 221, 57, 17, 81, 211, 230, 164, 127, 125, 46, 141, 98, 15, 144, 185, 194, 131, 199, 173, 240, 91, 137, 189, 116, 63, 191, 85, 232, 159, 146, 7, 30, 69, 100, 227, 11, 51, 169, 62, 212, 0, 210, 213, 106, 66, 243, 202, 14, 74, 168, 229, 138, 38, 155, 209, 190, 247, 177, 64, 102, 96, 53, 52, 134, 47, 235, 79, 33, 87, 241, 248, 217, 4, 61, 246, 120, 162, 59, 118, 83, 133, 99, 36, 29, 43, 26, 90, 103, 150, 45, 2, 119, 111, 231, 251, 37, 253, 105, 84, 113, 108, 12, 25, 54, 65, 86, 24, 71, 186, 219, 10, 158, 184, 109, 110, 174, 97, 225, 148, 206, 167, 163, 56, 195, 75, 193, 73, 215, 55, 67, 49, 34, 208, 156, 28, 129, 21, 236, 192, 32, 252], [168, 251, 118, 211, 115, 141, 239, 96, 6, 56, 212, 28, 233, 186, 208, 36, 21, 165, 140, 185, 240, 225, 166, 183, 189, 244, 194, 90, 200, 35, 147, 44, 13, 148, 69, 149, 146, 83, 206, 218, 162, 128, 7, 18, 20, 237, 38, 193, 105, 55, 74, 3, 231, 216, 60, 177, 120, 196, 101, 97, 100, 11, 111, 137, 47, 99, 65, 107, 203, 142, 89, 160, 14, 124, 133, 33, 159, 197, 25, 169, 182, 209, 62, 72, 39, 92, 210, 173, 108, 248, 77, 104, 53, 247, 138, 75, 16, 249, 116, 88, 199, 228, 139, 67, 236, 163, 61, 102, 94, 52, 156, 129, 29, 152, 184, 71, 246, 125, 245, 250, 243, 95, 19, 57, 153, 43, 235, 121, 91, 79, 226, 145, 80, 144, 222, 110, 10, 215, 180, 181, 214, 84, 2, 109, 213, 155, 205, 41, 198, 66, 132, 123, 58, 204, 201, 230, 232, 207, 176, 127, 81, 40, 0, 238, 54, 234, 70, 135, 119, 4, 187, 126, 143, 131, 112, 76, 130, 12, 86, 50, 42, 151, 188, 30, 229, 221, 223, 158, 73, 24, 68, 178, 114, 63, 8, 190, 195, 27, 122, 220, 37, 9, 1, 134, 242, 170, 191, 78, 48, 32, 98, 136, 252, 45, 106, 174, 22, 103, 167, 113, 5, 254, 241, 164, 154, 93, 46, 34, 179, 59, 117, 202, 219, 224, 31, 17, 82, 85, 26, 157, 175, 172, 217, 23, 227, 192, 171, 49, 87, 15, 255, 64, 150, 253, 161, 51], [209, 113, 140, 252, 243, 228, 225, 8, 141, 76, 177, 134, 246, 121, 100, 26, 4, 94, 222, 166, 73, 18, 176, 81, 35, 97, 71, 54, 136, 143, 151, 217, 186, 64, 9, 161, 2, 95, 142, 104, 168, 106, 149, 233, 220, 198, 237, 227, 105, 224, 69, 55, 144, 133, 24, 58, 65, 210, 213, 90, 212, 57, 114, 80, 41, 178, 202, 190, 36, 132, 70, 119, 160, 74, 159, 173, 17, 112, 40, 164, 21, 230, 187, 138, 6, 48, 208, 254, 85, 236, 247, 250, 165, 193, 153, 53, 82, 181, 204, 154, 182, 203, 194, 131, 32, 15, 150, 86, 0, 251, 11, 93, 45, 61, 16, 83, 99, 180, 201, 28, 232, 108, 14, 96, 253, 101, 52, 255, 60, 148, 219, 123, 13, 174, 23, 117, 235, 158, 139, 239, 163, 56, 103, 169, 185, 147, 207, 137, 216, 66, 1, 50, 109, 242, 29, 120, 62, 162, 197, 226, 51, 184, 125, 102, 211, 234, 245, 39, 146, 205, 135, 42, 34, 172, 240, 167, 231, 10, 124, 183, 25, 157, 46, 75, 118, 241, 179, 110, 192, 152, 59, 248, 191, 92, 127, 195, 68, 128, 238, 175, 38, 155, 244, 98, 44, 30, 189, 206, 196, 78, 20, 47, 115, 200, 88, 215, 223, 170, 111, 84, 79, 218, 27, 199, 12, 171, 221, 130, 145, 33, 72, 156, 49, 19, 37, 229, 5, 129, 126, 87, 107, 122, 63, 22, 7, 67, 214, 3, 116, 43, 31, 89, 91, 77, 188, 249], [101, 163, 16, 250, 52, 62, 147, 149, 162, 105, 228, 80, 134, 56, 130, 97, 244, 106, 222, 78, 40, 20, 67, 6, 35, 127, 242, 11, 99, 255, 10, 187, 167, 123, 94, 125, 188, 144, 156, 171, 71, 17, 19, 59, 9, 13, 253, 151, 236, 252, 53, 169, 164, 216, 210, 209, 28, 50, 192, 176, 114, 100, 74, 0, 87, 211, 73, 1, 84, 168, 57, 122, 102, 121, 214, 27, 185, 154, 175, 119, 88, 25, 137, 86, 178, 72, 18, 43, 206, 42, 225, 232, 152, 131, 70, 190, 49, 215, 195, 91, 104, 111, 21, 181, 75, 46, 64, 159, 118, 69, 227, 47, 203, 23, 90, 76, 142, 138, 238, 170, 95, 148, 7, 251, 103, 15, 224, 245, 197, 186, 12, 83, 22, 173, 55, 115, 229, 36, 126, 24, 3, 247, 157, 136, 166, 63, 246, 198, 213, 177, 205, 202, 66, 240, 234, 237, 135, 230, 48, 201, 183, 44, 93, 204, 45, 39, 89, 184, 193, 226, 212, 112, 223, 108, 2, 143, 5, 150, 31, 254, 189, 220, 182, 217, 98, 32, 61, 37, 79, 219, 33, 249, 145, 200, 113, 92, 172, 165, 110, 140, 38, 128, 158, 146, 199, 233, 26, 133, 109, 96, 51, 231, 241, 139, 174, 129, 161, 120, 117, 235, 30, 29, 77, 65, 60, 82, 141, 85, 208, 54, 153, 8, 116, 4, 81, 58, 107, 132, 207, 160, 179, 194, 180, 191, 239, 196, 14, 243, 221, 68, 41, 218, 124, 155, 34, 248], [60, 227, 182, 150, 239, 148, 138, 123, 161, 86, 31, 69, 210, 222, 192, 174, 54, 105, 194, 134, 176, 39, 249, 243, 93, 41, 6, 27, 35, 234, 187, 4, 225, 217, 102, 1, 144, 21, 30, 246, 171, 202, 33, 114, 189, 28, 36, 175, 8, 63, 104, 251, 70, 37, 48, 236, 240, 166, 77, 32, 7, 9, 160, 55, 199, 145, 91, 139, 127, 49, 51, 13, 67, 3, 191, 184, 50, 178, 204, 207, 168, 206, 126, 129, 128, 226, 100, 95, 107, 111, 130, 248, 124, 61, 20, 244, 143, 97, 84, 163, 135, 56, 241, 232, 159, 238, 154, 16, 181, 121, 0, 142, 88, 183, 186, 228, 78, 242, 117, 45, 164, 152, 179, 146, 15, 212, 147, 24, 203, 79, 195, 245, 47, 230, 118, 40, 116, 156, 11, 34, 140, 53, 85, 250, 58, 65, 29, 235, 188, 219, 155, 185, 90, 101, 252, 136, 201, 180, 64, 10, 214, 254, 73, 18, 68, 66, 132, 224, 208, 5, 62, 120, 92, 52, 190, 22, 198, 23, 149, 153, 162, 59, 83, 193, 211, 108, 131, 221, 167, 172, 247, 165, 82, 231, 99, 205, 233, 173, 253, 14, 17, 177, 12, 151, 220, 74, 71, 112, 216, 2, 89, 42, 113, 75, 98, 25, 169, 110, 237, 103, 122, 19, 44, 76, 43, 96, 81, 119, 38, 215, 87, 200, 46, 137, 125, 213, 196, 57, 170, 209, 80, 218, 72, 157, 94, 141, 229, 26, 115, 158, 255, 223, 133, 109, 197, 106], [167, 93, 14, 223, 21, 132, 236, 77, 185, 35, 122, 194, 235, 98, 50, 10, 72, 17, 84, 196, 133, 19, 179, 245, 82, 153, 104, 76, 229, 67, 253, 60, 160, 41, 117, 191, 238, 11, 22, 209, 44, 224, 147, 168, 136, 49, 5, 32, 47, 16, 218, 91, 111, 175, 187, 127, 233, 146, 137, 7, 215, 65, 250, 45, 251, 249, 225, 68, 75, 39, 103, 123, 220, 237, 240, 206, 216, 1, 79, 149, 59, 113, 174, 12, 86, 43, 201, 97, 203, 112, 125, 208, 74, 157, 180, 212, 37, 150, 8, 252, 173, 178, 255, 57, 205, 217, 69, 15, 141, 200, 241, 171, 190, 192, 202, 116, 210, 61, 109, 102, 199, 30, 164, 2, 176, 219, 170, 189, 25, 3, 105, 118, 144, 161, 138, 29, 244, 4, 96, 231, 184, 158, 124, 145, 58, 188, 42, 172, 55, 64, 23, 51, 78, 228, 115, 148, 27, 70, 131, 134, 53, 214, 87, 83, 221, 165, 106, 33, 62, 156, 36, 108, 162, 177, 56, 99, 0, 26, 63, 94, 46, 181, 129, 155, 211, 48, 40, 204, 89, 121, 186, 166, 100, 183, 135, 246, 66, 139, 154, 242, 13, 247, 142, 92, 18, 71, 195, 143, 152, 198, 85, 9, 207, 88, 81, 232, 151, 169, 243, 95, 222, 107, 239, 254, 226, 140, 248, 114, 52, 128, 54, 110, 31, 182, 234, 34, 80, 20, 130, 213, 197, 6, 163, 24, 90, 119, 227, 230, 28, 73, 101, 120, 193, 38, 126, 159], [150, 68, 35, 8, 169, 184, 52, 102, 107, 207, 116, 122, 14, 64, 255, 238, 179, 219, 236, 189, 53, 13, 224, 4, 146, 239, 66, 212, 118, 111, 161, 214, 9, 175, 25, 190, 246, 247, 210, 40, 220, 159, 249, 85, 172, 100, 46, 240, 235, 87, 94, 34, 195, 218, 42, 76, 222, 176, 72, 163, 245, 198, 181, 80, 44, 49, 233, 75, 54, 132, 97, 16, 88, 130, 242, 188, 112, 154, 194, 78, 24, 47, 127, 205, 156, 192, 124, 93, 229, 23, 63, 7, 158, 237, 136, 121, 201, 103, 203, 10, 223, 166, 209, 225, 105, 217, 27, 12, 58, 59, 137, 57, 98, 241, 62, 11, 113, 216, 126, 18, 221, 142, 99, 208, 28, 151, 171, 133, 165, 129, 20, 65, 92, 36, 83, 89, 167, 182, 183, 51, 33, 162, 139, 73, 77, 228, 138, 174, 180, 204, 19, 115, 125, 2, 29, 186, 48, 250, 30, 60, 147, 185, 43, 0, 50, 108, 253, 91, 141, 211, 104, 71, 84, 193, 144, 56, 232, 140, 106, 128, 109, 153, 215, 131, 69, 152, 200, 17, 196, 157, 244, 164, 70, 168, 120, 3, 110, 149, 178, 5, 160, 117, 177, 148, 123, 202, 41, 234, 101, 86, 22, 197, 45, 230, 96, 206, 243, 82, 74, 39, 135, 251, 155, 213, 79, 67, 173, 254, 191, 252, 32, 37, 134, 61, 26, 6, 231, 81, 199, 143, 114, 90, 187, 55, 1, 227, 145, 119, 170, 95, 31, 38, 226, 248, 21, 15]]


# Decode custom encoding type
def decodeCustomEncodingType():
    # Decode base64
    with open(os.path.join(file_directory, "encodedfile.txt"), "r", encoding="utf-8") as f:
        a = f.read()
    decodedString = base64.urlsafe_b64decode(a)

    # Get the original byte
    origbyte = decodedString[:-1]
    # print(origbyte)

    # Get the last byte
    lastbyte = decodedString[-1:][0]

    # Convert byte to char map
    charMap = [x for x in origbyte]

    # Return charMap back to original values
    for x in range(len(charMap)):
        charMap[x] = mappingTable[lastbyte].index(charMap[x])

    # Convert bytearray back to Byte
    replacedCharMap = bytes(bytearray(charMap) )  

    # DecodeByteObject
    jsonParsedContent = replacedCharMap.decode("utf-8")
    try:
        questions = json.loads(jsonParsedContent)["questionObjs"]
        if questions:
            questionAndAnswerParser(questions)
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(jsonParsedContent)        
    except KeyError:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(jsonParsedContent)
            resultTrack = json.loads(jsonParsedContent)["resultTrack"][4:]
            e = dGB(resultTrack).decode("utf-8")
            print("Your answer: ", e)
            
    
# Parse question and answer   
def questionAndAnswerParser(questions):
    # Get all the questions and answers:
    with open(file_path, "w+", encoding="utf-8") as f:
        for x in range(len(list(questions))):
            f.write(f"Câu {x + 1}:<br>")
            f.write(questions[x]["content"])
            for y in range(len(list(questions[x]["answers"]))):
                f.write("<br>")
                f.write(answerLabel[y])
                f.write(questions[x]["answers"][y]["content"])
                f.write("<br>")
            f.write("<br>")

        # Check if image exists and get the link
        f.seek(0)
        imageLinks = re.findall(r"@\[\].+?@\[\]", f.read())
        if imageLinks:
            parseImage(imageLinks)
        else:
            pass
 

# Trim image (if exists) 
def parseImage(imageLinks):
    iLRs = []
    dataImages = []
    filenames = []   
        
    try:
        print("Creating Folder")
        os.makedirs(os.path.join(file_directory, "AzotaImages"))
    
    except FileExistsError:
        print("File existed! Putting image files")
        for filename in os.listdir(os.path.join(file_directory, "AzotaImages")):
            filename = os.path.join(file_directory, "AzotaImages", filename)
            try:
                if os.path.isfile(filename) or os.path.islink(filename):
                    os.unlink(filename)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filename, e))
    
    finally:
        with open(file_path, "r+", encoding="utf-8") as f:   
            a = f.read()
            for i in range(len(imageLinks)):
                iLRs.extend(re.findall(r"(?<=@\[\]{\"link\":\").+?(?=\")", imageLinks[i]))
                dataImages.extend(re.findall(r"(?<=\"data\":).+?(?=}@)", imageLinks[i]))
                dataImages[i] = (int(json.loads(dataImages[i])["x"]), int(json.loads(dataImages[i])["y"]), int(json.loads(dataImages[i])["x"]) + int(json.loads(dataImages[i])["width"]), int(json.loads(dataImages[i])["y"]) + int(json.loads(dataImages[i])["height"]))
                filenames.append(os.path.join(file_directory, "AzotaImages", uuid.uuid4().hex) + ".png")
                ci(iLRs[i], dataImages[i], filenames[i])
                a = a.replace(imageLinks[i], f"<img src=\"{filenames[i]}\"><br><br>")
                            
                f.seek(0)
                f.truncate(0)
                f.write(a)

        
if __name__ == "__main__":
    decodeCustomEncodingType()
