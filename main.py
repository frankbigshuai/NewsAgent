
from flask import Flask
import os

# 创建Flask应用实例
app = Flask(__name__)

# 路由定义
@app.route('/')
def home():
    return '''
    <h1>NewsAgent</h1>

    '''

@app.route('/about')
def about():
    return '''
    <h1>AI agent</h1>
    '''


@app.route('/api/status')
def status():
    return {
        'status': 'success',
        'message': 'Flask应用运行正常',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    # Railway会设置PORT环境变量
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)