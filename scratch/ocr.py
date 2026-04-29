import sys
import Quartz
import Vision
from Cocoa import NSURL

def extract_text(image_path):
    url = NSURL.fileURLWithPath_(image_path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    request = Vision.VNRecognizeTextRequest.alloc().init()
    handler.performRequests_error_([request], None)
    results = request.results()
    for res in results:
        print(res.topCandidates_(1)[0].string())

extract_text(sys.argv[1])
