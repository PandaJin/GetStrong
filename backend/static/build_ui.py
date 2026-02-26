#!/usr/bin/env python3
"""Build script to generate the GetStrong index.html"""
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# Will be populated by subsequent writes
CSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts', 'style.css')
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts', 'body.html')
JS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts', 'app.js')

def build():
    css = open(CSS_FILE).read()
    html = open(HTML_FILE).read()
    js = open(JS_FILE).read()

    output = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>GetStrong - 智能健康助手</title>
<style>
{css}
</style>
</head>
<body>
{html}
<script>
{js}
</script>
</body>
</html>'''

    with open(OUTPUT, 'w') as f:
        f.write(output)
    print(f'Built {OUTPUT}')

if __name__ == '__main__':
    build()
