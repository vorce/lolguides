from paver.easy import *
from paver.setuputils import setup
import sys
import os
sys.path.append(os.path.abspath('.'))
import genwok
import getguidedata
import genutils

setup(
    name="Lolguides",
    packages=['genwok', 'getguidedata'],
    version="1.0",
    url="http://www.lolguides.net/",
    author="Joel Carlbark",
    author_email="joelcb@gmail.com"
)


@task
@consume_args
def index(args):
    genwok.genIndex(args[0])


@task
@consume_args
def champs(args):
    dataz = genutils.loadJSONs()  # ('guide_data.json')
    genwok.genAllChampPages(dataz, args[0])


@task
@consume_args
def data(args):
    getguidedata.getGuideData(args)


@task
def git():
    msg = 'Automated git commit from paver'
    os.system("git commit -a -m '{0}'".format(msg))


@task
def publish():
    os.system("./publish.sh")


@task
def test():
    print("Hello")


@task
@consume_args
def all(args):
    data(['solomid', 'clg', 'lolpro', 'lolking'])

    indexNotice = ""
    if len(args) > 0:
        indexNotice = args[0]

    champNotice = indexNotice
    if len(args) > 1:
        champNotice = args[1]

    champs(champNotice)
    index(indexNotice)
    git()
    publish()
