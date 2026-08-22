#!/usr/bin/env python3
"""Render a cover letter as HTML that Google Drive converts into a native
Google Doc carrying Joaquin's house format.

Upload with create_file(contentMimeType='text/html', textContent=<this output>)
and DO NOT set disableConversionToGoogleType.
"""
import sys, json, html

FONT = "font-family:'Times New Roman',serif;font-size:11pt;"
P     = FONT + "margin:0 0 10pt 0;text-align:left;"
CTR   = FONT + "margin:0;text-align:center;"
CTR2  = FONT + "margin:0 0 15pt 0;text-align:center;"

NAME  = "Joaquin Zarazua"
CITY  = "Centennial, CO"
PHONE = "720-435-0880"
EMAIL = "joaquinz0721@gmail.com"
LI_T  = "linkedin.com/in/joaquinzarazua"
LI_U  = "http://linkedin.com/in/joaquinzarazua"

def build(date_line, hiring_team, paragraphs):
    if len(paragraphs) != 5:
        raise ValueError('expected 5 paragraphs (4 body + closing), got %d' % len(paragraphs))
    e = html.escape
    out = ['<html><head><meta charset="utf-8"></head><body>']
    out.append(f'<p style="{CTR}"><b>{e(NAME)}</b></p>')
    out.append(
        f'<p style="{CTR2}">{e(CITY)}&nbsp; |&nbsp; {e(PHONE)}&nbsp; | {e(EMAIL)}&nbsp; |&nbsp; '
        f'<a href="{LI_U}">{e(LI_T)}</a></p>')
    out.append(f'<p style="{P}">{e(date_line)}</p>')
    out.append(f'<p style="{P}">{e(hiring_team)}</p>')
    out.append(f'<p style="{P}">Dear Hiring Manager,</p>')
    out.append(f'<p style="{P}">&nbsp;</p>')
    for para in paragraphs:
        out.append(f'<p style="{P}">{e(para)}</p>')
    out.append(f'<p style="{P}">&nbsp;</p>')
    out.append(f'<p style="{P}">Sincerely,</p>')
    out.append(f'<p style="{P}">{e(NAME)}</p>')
    out.append('</body></html>')
    return "\n".join(out)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    h = build(spec['date'], spec['hiring_team'], spec['paragraphs'])
    dest = spec.get('html_out', spec['out'].rsplit('.',1)[0] + '.html')
    open(dest,'w').write(h)
    print(dest)
