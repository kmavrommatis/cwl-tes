import urllib
import os
import cwltool.argparser
import json
from typing import (
    AnyStr,
    cast
)
from cwltool.stdfsaccess import StdFsAccess
from cwltool.utils import CWLObjectType
from schema_salad.ref_resolver import file_uri
import boto3
from urllib.parse import urlparse


# Patch functions in argparse to enable parsing of s3:// URIs as inputs
def FSActioncall(
    self,
    parser,
    namespace,
    values,
    option_string=None,
):
    url = urllib.parse.urlparse(values)
    if url.scheme == '':
        setattr(
            namespace,
            self.dest,
            {
                "class": self.objclass,
                "location": file_uri(str(
                    os.path.abspath(cast(AnyStr, values)))),
            },
            )
    else:
        setattr(
            namespace,
            self.dest,
            {
                "class": self.objclass,
                "location": values,
            },
            )


cwltool.argparser.FSAction.__call__ = FSActioncall


def FSAppendActioncall(
    self,
    parser,
    namespace,
    values,
    option_string=None,
):

    g = getattr(namespace, self.dest)
    if not g:
        g = []
        setattr(namespace, self.dest, g)
    url = urllib.parse.urlparse(values)
    if url.scheme == "":
        g.append(
            {
                "class": self.objclass,
                "location": file_uri(str(
                    os.path.abspath(cast(AnyStr, values)))),
            }
            )
    else:
        g.append(
            {
                "class": self.objclass,
                "location":  values,
            }
            )


cwltool.argparser.FSAppendAction.__call__ = FSAppendActioncall


def replaceURI(mapper: str, cwl_output: str , compute_checksum: bool):
    ''' convert the location of the output from cwltool to the original URI '''
    pathmap = {}
    #print("mapper is {}".format(mapper))
    #print("cwl_output is {}".format( cwl_output ))
    def getMapper():
        lines = mapper.splitlines()
        for line in lines:
            if line.startswith("Mapper:"):
                dd = line.replace("Mapper: ", "")
                pm_dict = json.loads(dd)
                pathmap[pm_dict['target_uri']] = pm_dict

    getMapper()
    client=boto3.client('s3')
    #print("Pathmap {}".format(pathmap))
    for k in pathmap:
        etag=getEtag( pathmap[k]['resolved'] ,client )
        repstr=pathmap[k]['resolved']
        if etag:
            repstr="{}\", \"etag\": \"{}".format( repstr, etag)
        cwl_output = cwl_output.replace(k, repstr)
        
        
    #print("cwloutput {}".format(cwl_output))
    if cwl_output:
        
        return json.dumps( json.loads( cwl_output ),default=str, indent=4)
    else:
        return None



def getEtag( f:str, client):
    s3obj_etag=None
    if f.startswith("s3:"):
        
        s3_frag=urlparse( f, allow_fragments=False)
        try:
            if s3_frag.path.startswith('/'):
                p=s3_frag.path[1:]
            else:
                p=s3_frag.path
            s3_resp =  client.head_object(Bucket=s3_frag.netloc, Key=p)
            s3obj_etag = s3_resp['ETag'].strip('" ')
        except Exception as e:
            #print("Unable to get Etag for object {}".format(f))
            pass
    #print("Found etag {} for file {}".format( s3obj_etag, f))
    return s3obj_etag
