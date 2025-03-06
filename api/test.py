from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "success",
            "message": "测试API正常工作"
        }).encode("utf-8"))

def handler(request, context):
    """
    Vercel Serverless函数入口点
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'status': 'success',
            'message': '测试API正常工作 - Vercel函数版本'
        })
    }
