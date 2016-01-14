
from __future__ import print_function

from subprocess import Popen, PIPE
import os
import io

from nltk import word_tokenize

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

def tokenize_directory(data_dir='data/', tokenized_dir='tokendir/'):
    for filename in os.listdir(data_dir):
        infile = filename
        toktok_cmd = 'perl tok-tok.pl < {datadir}/{inputfile} > {tokdir}/{inputfile}'
        os.system(toktok_cmd.format(datadir=data_dir, tokdir=tokenized_dir, inputfile=infile))
    
def loop_file_for_sent(indir):
    for filename in os.listdir(indir):
        infile = indir + filename
        with io.open(infile, 'r', encoding='utf8') as fin:
            for line in fin:
                yield infile, line.strip()


# This says that I'm storing filenam and content into the index.
schema = Schema(filename=TEXT(stored=True), content=TEXT(stored=True))
ix = create_in("indexdir", schema)
# Creates an instance of an index writer.
writer = ix.writer()

for _filename, sentence in loop_file_for_sent('tokendir/'):
    writer.add_document(filename=_filename, content=sentence)

writer.commit()


with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("forma que tiene")
    results = searcher.search(query)
    for r in results:
        print (r['content'])