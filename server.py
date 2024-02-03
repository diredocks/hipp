from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import quote
import json

class SimpleRESTHandler(BaseHTTPRequestHandler):
    def throw_Response(self, response_code, message):
        self.send_response(response_code)
        self.end_headers()
        self.wfile.write(message)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # 根据请求的路径和参数返回相应的数据
        if parsed_path.path == '/quote':
            quote_type = query_params.get('type', [None])[0]
            if quote_type:
                #response_data = {'id': data_id, 'message': 'Data with ID {} retrieved'.format(data_id)}
                response_data = quote.fetch_quote(quote_type)
                if response_data != 404:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode())
                else:
                    self.throw_Response(404, b'Given type not found')
            else:
                self.throw_Response(400, b'Missing "type" parameter')
        else:
            self.throw_Response(404, b'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == '/quote':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                parsed_data = json.loads(post_data.decode())
            except:
                self.throw_Response(400, b'No data received')

            if all(key in parsed_data for key in ('quote_type', 'source', 'author', 'quote', 'token')):
                result = quote.add_quote(parsed_data['quote_type'], 
                                         parsed_data['source'],
                                         parsed_data['author'], 
                                         parsed_data['quote'], 
                                         parsed_data['token'])
                if result == 200:
                    self.throw_Response(200, b'Succeed')
                else:
                    self.throw_Response(401, b'Unauthorized Token')
            else:
                self.throw_Response(400, b'Missing parameter')
        else:
            self.throw_Response(404, b'Not Found')
        # 在这里处理 POST 请求并返回响应
        #response_data = {'message': 'Received POST request with data: {}'.format(parsed_data)}
        #self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        #self.end_headers()
        #self.wfile.write(json.dumps(response_data).encode())

    #def do_PUT(self):
        #content_length = int(self.headers['Content-Length'])
        #put_data = self.rfile.read(content_length)
        #parsed_data = json.loads(put_data.decode())

        # 在这里处理 PUT 请求并返回响应
        #response_data = {'message': 'Received PUT request with data: {}'.format(parsed_data)}
        #self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        #self.end_headers()
        #self.wfile.write(json.dumps(response_data).encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # 根据请求的路径和参数处理删除操作
        if parsed_path.path == '/quote':
            data_id = query_params.get('id', [None])[0]
            if data_id:
                # 这里可以执行删除操作，此处只返回一个示例响应
                response_data = {'id': data_id, 'message': 'Data with ID {} deleted'.format(data_id)}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing "id" parameter')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

def run():
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleRESTHandler)
    print(f'Starting server... at {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

