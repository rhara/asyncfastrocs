from asyncfastrocs import state, misc
import os, time

def  make_table(config):
    st = state.State()

    now = time.time()
    since = now - config['MAX_DAYS']*60*60*24

    s = """
<table>
  <tr>
    <td></td>
    <td><b>Query</b></td>
    <td><b>Hitsize</b></td>
    <td><b>Hitlist</b></td>
    <td><b>ROCS Report</b></td>
    <td><b>DB</b></td>
    <td><b>From</b></td>
    <td><b>Timestamp</b></td>
    <td><b>OID</b></td>
  </tr>
""".lstrip()

    for r in st.get_list(since):
        oid = r['oid']
        basename = r['basename']
        ext = r['ext']
        reportable = r['reportable']
        timestamp1 = r['timestamp1']
        timestamp2 = r['timestamp2']
        hitsize = r['hitsize']
        dbname = r['dbname']
        rstatus = r['status']
        ip = r['ip']
        timestamp1 = misc.iso_time(timestamp1, millisec=True)
        rstatus_mark = ['&#x22B9;', '&#x2737;', '&#x2713;'][rstatus]
        if rstatus == 1:
            query_link = f'<a class="bred" href="/download/query/{oid}">{basename}.{ext}</a>'
        else:
            query_link = f'<a href="/download/query/{oid}">{basename}.{ext}</a>'
        result_link = ''
        report_link = ''
        tr_begin = '<tr>'
        if rstatus == 1:
            tr_begin = '<tr class="bred">'
        if rstatus == 2:
            result_link = f'<a href="/download/result/{oid}">Hits</a>'
        if reportable == 1 and rstatus == 2:
            report_link = f'<a href="/download/report/{oid}" target="_blank">PDF</a>'
        s += f"""
  {tr_begin}
    <td>{rstatus_mark}</td>
    <td>{query_link}</td>
    <td align="right">{hitsize}</td>
    <td>{result_link}</td>
    <td>{report_link}</td>
    <td>{dbname}</td>
    <td>{ip}</td>
    <td>{timestamp1}</td>
    <td><span style="font-family:monospace; font-size:80%;">{oid}</span></td>
  </tr>
""".lstrip()

    s += """
</table>
""".lstrip()

    return s

def make_dbnote():
    st = state.State()

    r = st.get_active()
    name = r['name']
    ready = True if r['ready'] == 1 else False
    path = r['path']
    molcount = r['molcount']
    confcount = r['confcount']
    basename = os.path.split(path)[1]

    info = f'{basename} ({name}): ' \
           f'{molcount:,} mols, {confcount:,} confs, ready={ready}'

    count = st.get_queue_count()

    if ready and count == 0:
        link = '<a href="/changedb_page">Change Database</a>'
    else:
        link = '<span style="color: #ccc;">Change Database</span>'

    s = f"""
<table width="100%">
  <tr>
    <td>{info}</td>
    <td align="right" style="font-size:80%;">{link}</td>
  </tr>
</table>
""".lstrip()

    return s
