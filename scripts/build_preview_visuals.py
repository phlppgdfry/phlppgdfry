"""Generate the code-native harbor tiles, project covers and editorial GIFs."""
from html import escape
import math
from build_visuals import OUT, BG, PANEL, LINE, LIME, CYAN, WHITE, MUTED, base, font, save


def motif(kind, color):
    if kind == 'apps':
        return f'<rect x="700" y="42" width="190" height="119" rx="12" fill="{PANEL}" stroke="{color}" stroke-width="3"/><path d="M700 68H890" stroke="{LINE}"/><circle cx="718" cy="56" r="4" fill="{color}"/><path d="M742 99H850M742 117H825M742 135H862" stroke="{color}" stroke-width="6"/>'
    if kind == 'data':
        return ''.join(f'<rect x="{694+i*27}" y="{43+i*39}" width="160" height="30" rx="7" fill="{PANEL}" stroke="{c}" stroke-width="2"/><text x="{716+i*27}" y="{64+i*39}" fill="{c}" font-size="15" font-family="monospace">{label}</text>' for i,(label,c) in enumerate([('BRONZE','#dfa46d'),('SILVER','#c2d1dd'),('GOLD',LIME)]))
    if kind == 'ai':
        return f'<circle cx="793" cy="105" r="51" fill="{PANEL}" stroke="{color}" stroke-width="2"/><path d="M793 54V20M793 156V184M742 105H695M844 105H905" stroke="{color}" stroke-width="2"/><text x="771" y="115" font-family="monospace" font-size="30" fill="{WHITE}">AI</text><circle cx="705" cy="105" r="6" fill="{color}"/><circle cx="892" cy="105" r="6" fill="{color}"/>'
    if kind == 'mobile':
        return f'<rect x="744" y="25" width="100" height="150" rx="13" fill="{PANEL}" stroke="{color}" stroke-width="3"/><path d="M775 39H813M762 69H825M762 94H825M762 119H812" stroke="{color}" stroke-width="4"/><circle cx="794" cy="159" r="4" fill="{color}"/>'
    return f'<path d="M733 171V43H914M714 171H757M733 43L769 21L805 43M864 43V92" fill="none" stroke="{color}" stroke-width="4"/><rect x="826" y="93" width="77" height="42" rx="4" fill="{color}"/><path d="M697 188H929" stroke="{LINE}" stroke-width="3"/>'


def panel(filename, eyebrow, title, sub, kind, color=LIME, district=False):
    height=210
    extra=f'<path d="M0 196H960" stroke="{CYAN}" stroke-width="3"/><path d="M30 205H130M175 205H275M320 205H420M465 205H565M610 205H710M755 205H855" stroke="{LINE}" stroke-width="2"/>' if district else ''
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-label="{escape(title)}">
<rect width="960" height="{height}" rx="16" fill="{BG}"/><path d="M654 20V185" stroke="{LINE}"/>
<text x="30" y="38" font-size="14" font-family="monospace" fill="{color}">{escape(eyebrow)}</text>
<text x="30" y="96" font-size="43" font-weight="bold" font-family="Arial,sans-serif" fill="{WHITE}">{escape(title)}</text>
<text x="32" y="135" font-size="19" font-family="Arial,sans-serif" fill="{MUTED}">{escape(sub)}</text>
<text x="32" y="176" font-size="13" font-family="monospace" fill="{color}">{'ENTER THIS DISTRICT →' if district else 'PHLPPGDFRY / SELECTED WORK'}</text>
{motif(kind,color)}{extra}</svg>'''
    (OUT/filename).write_text(svg)


def editorial_gifs():
    frames=[]
    for i in range(50):
        im,d=base(600,235,'EXHIBIT 01 / THE QUERY HAD OTHER PLANS')
        fixed=i>=27
        d.text((25,66),'ToString() meets SQLite',font=font(23),fill=WHITE)
        d.text((25,107),'no such function: tostring' if not fixed else 'enum value -> query parameter',font=font(18),fill='#f58b8b' if not fixed else LIME)
        d.rounded_rectangle((25,154,575,193),7,fill=PANEL)
        d.rounded_rectangle((27,156,27+int(546*min(i/35,1)),191),6,fill=LIME if fixed else CYAN)
        d.text((40,164),'READ THE QUERY. THEN TEST THE BUILD.',font=font(13),fill=BG)
        frames.append(im)
    save('query-plot-twist.gif',frames,110)
    frames=[]
    for i in range(48):
        im,d=base(600,235,'EXHIBIT 02 / THE RELEASE IS THE PRODUCT')
        d.text((25,66),'Code ready != download ready',font=font(22),fill=WHITE)
        for j,label in enumerate(['BUILD','SIGN','NOTARIZE','RELEASE']):
            x=25+j*145
            done=i>=j*9+5
            d.rounded_rectangle((x,120,x+125,170),8,fill=PANEL,outline=LIME if done else LINE,width=2)
            d.text((x+12,138),label,font=font(15),fill=LIME if done else MUTED)
        d.text((25,199),'The ZIP gets the final vote.',font=font(15),fill=CYAN)
        frames.append(im)
    save('release-checklist.gif',frames,110)


if __name__=='__main__':
    districts=[('apps','01 / WEST QUAY','App Dock','Mac utilities, native interfaces and product decisions.','apps',LIME),('data','02 / NORTH QUAY','Data Warehouse','Pipelines, analytics and useful answers.','data',CYAN),('ai','03 / EAST QUAY','AI Lab','Local models, evidence and controlled experiments.','ai','#bc9cff'),('operations','04 / CONTROL QUAY','Operations Tower','Ports, workflows and the business behind the software.','ports','#ffbc79')]
    for key,eyebrow,title,sub,kind,c in districts:panel('district-'+key+'.svg',eyebrow,title,sub,kind,c,True)
    covers=[('logistics','01 / PORTFOLIO HUB','Logistics Master','Operational ideas, from yard capacity to vessel calls.','ports',LIME),('portops','02 / LOCAL PROTOTYPE','PortOps AI','Which vehicles need attention, and why?','ai','#bc9cff'),('clicktrack','03 / MAC APP','ClickTrack','Your activity. Your Mac. Your data.','apps',CYAN),('mirrormate','04 / MAC APP','MirrorMate','A quick mirror, one shortcut away.','apps','#ffbc79'),('fabric','05 / EARLY LEARNING BUILD','Fabric Data Platform','Raw events. Clear layers. A useful destination.','data',LIME),('docurelay','06 / WORKING PORTFOLIO DEMO','DocuRelay Field','Capture now. Queue safely. Sync when ready.','mobile',CYAN)]
    for key,eyebrow,title,sub,kind,c in covers:panel('cover-'+key+'.svg',eyebrow,title,sub,kind,c)
    for key,label,color in [('download','DOWNLOAD A MAC APP',LIME),('demo','TRY A TERMINAL SIM',CYAN),('watch','WATCH A WORKFLOW','#bc9cff')]:
        (OUT/f'action-{key}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="258" height="42" viewBox="0 0 258 42" role="img" aria-label="{label}"><rect width="258" height="42" rx="5" fill="{color}"/><text x="129" y="26" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" letter-spacing="1" fill="{BG}">{label}</text></svg>')
    editorial_gifs()
