def generate_minimal_pawn_svg(fill_color):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
    <g fill="{fill_color}">
        <path d="M 100,450 A 10,10 0 0 0 110,460 L 290,460 A 10,10 0 0 0 300,450 L 300,435 A 10,10 0 0 0 290,425 L 110,425 A 10,10 0 0 0 100,435 Z" />
        <path d="M 120,425 L 280,425 L 270,395 L 130,395 Z" />
        <path d="M 130,395 C 110,340 140,270 200,270 C 260,270 290,340 270,395 Z" />
        <circle cx="200" cy="210" r="42" />
        <path d="M 160,182 C 152,130 135,140 135,140 L 170,155 L 200,105 L 230,155 L 265,140 C 265,140 248,130 240,182 A 42,42 0 0 1 160,182 Z" />
        <circle cx="135" cy="132" r="5" />
        <circle cx="200" cy="95" r="7" />
        <circle cx="265" cy="132" r="5" />
        <path d="M 160,172 Q 200,178 240,172" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
        <path d="M 163,164 Q 200,170 237,164" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>
</svg>"""

open(r'C:\Users\irina\SahMatAnimat\img\pion-gemini-blue.svg', 'w').write(generate_minimal_pawn_svg('#1E40AF'))
open(r'C:\Users\irina\SahMatAnimat\img\pion-gemini-orange.svg', 'w').write(generate_minimal_pawn_svg('#C25E1A'))
print('salvat')
