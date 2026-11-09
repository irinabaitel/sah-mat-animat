import os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
REPO = r'C:/Users/irina/SahMatAnimat'
head = open(os.path.join(D, 'head.txt'), encoding='utf-8').read()
css = open(os.path.join(D, 'css.txt'), encoding='utf-8').read()
common = open(os.path.join(D, 'common.js'), encoding='utf-8').read()
for f in sys.argv[1:]:
    src = open(os.path.join(D, f + '.tpl'), encoding='utf-8').read()
    sec = dict(re.findall(r'===(\w+)===\n(.*?)(?=\n===\w+===\n|\Z)', src, re.S))
    html = (head + '<title>' + sec['TITLE'].strip() + '</title>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;900&family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">\n'
        '<link rel="stylesheet" href="master-template.css?v=20261016">\n<style>' + css + sec.get('CSS', '') + '</style>\n'
        '<link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v=6">\n'
        '<link rel="apple-touch-icon" href="/img/favicon-64.png?v=6">\n'
        '<script src="minijocuri-nav.js?v=20261109c"></script>\n</head>\n<body>\n<div class="page-wrapper">\n\n'
        '  <header class="page-header" role="banner">\n    <span class="header-title">' + sec['HEADER'].strip() + '</span>\n'
        '    <div class="header-progress"><span class="game-badge">Joc</span></div>\n  </header>\n\n'
        '  <main class="page-main" role="main">\n    <div class="board-col"><div class="board-wrapper"><div id="board"></div></div></div>\n'
        '    <div class="panel-col">\n      <div class="panel-scroll">\n' + sec['PANEL'] + '\n      </div>\n'
        '      <div class="feedback-bar" id="feedbackBar"></div>\n    </div>\n  </main>\n\n'
        '  <footer class="page-footer" role="navigation"></footer>\n</div>\n\n'
        '<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>\n'
        '<script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>\n'
        '<script src="board-utils.js"></script>\n<script>\n' + sec['SCRIPT'].split('/*COMMON*/')[0] + common + sec['SCRIPT'].split('/*COMMON*/')[1] + '</script>\n</body>\n</html>\n')
    out = os.path.join(REPO, sec['FILE'].strip())
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out, len(html))
