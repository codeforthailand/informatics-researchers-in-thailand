# -*- coding: utf-8 -*-

import json
import os
import collections
import yaml

PREFIX = "::table"
Table = collections.namedtuple("Table", ["pos", "src", "node"])
URL_ICONS = {
    'webpage': '[![](./icons/webpage.svg)](%s)',
    'gscholar': '[![](./icons/gscholar.svg)](%s)',
}

def table_row(cols):
    return "|%s|" % "|".join(cols)

def join_rows(r1, r2):
    return "%s\n%s" % (r1, r2)

tables = []
with open("./templates/README.md", "r") as f:
    for pos, l in enumerate(f):
        l = l.strip()
        if PREFIX in l.strip():
            src, node = l.split("::")[2].split("->")
            tables.append(Table(pos=pos, src=src, node=node))

str_tables = dict()
for t in tables:
    with open("db.yaml", "r") as fdb:
        db = yaml.load(fdb)[t.node]

        st = table_row(["Name", "Affiliation", "Links"])
        st = join_rows(st, table_row(["---"]*3))

        for p in db:
            urls = []
            for k, v in p['urls'].items():
                urls.append(URL_ICONS[k] % v)

            st = join_rows(st,
                table_row([
                    p['name'],
                    ", ".join(p['affiliation']),
                    " ".join(urls)
                ])
            )
        str_tables[t.pos] = st

with open("./templates/README.md", "r") as f , \
    open("./README.md", "w") as fout:

    for pos, original_line in enumerate(f):
        new_line = str_tables.get(pos, original_line.strip())

        fout.write("%s\n" % new_line)