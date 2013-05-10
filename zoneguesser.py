#!/usr/bin/env python

import argparse
import DNS
import os
import sys

DNS.DiscoverNameServers()

def lookup_dns(name, qtype='A'):
  qtype=qtype.upper();
  ans=DNS.DnsRequest(name,qtype=qtype).req().answers
  return ans

def load_single_file(txtfile):
  lines=open(txtfile,'r').read().split('\n')
  ret=[]
  
  for line in lines:
    line=line.strip()
    if line=='':
      continue
    
    if line.startswith('#'):
      continue
    
    parts=line.split()
    #print parts
    if len(parts)==1:
      tpl=(parts[0],'A')
    else:
      tpl=tuple(parts)
     
    ret.append(tpl)
    
  return ret
  

def load_wordlist(file_or_dir):
  if not os.path.exists(file_or_dir):
    return []
  
  wordlist=[]
  if os.path.isfile(file_or_dir):
    wordlist= load_single_file(file_or_dir)
  elif os.path.isdir(file_or_dir):
    filelist=os.listdir(file_or_dir)
    for f in filelist:
      if f.lower().endswith('.txt'):
	fpath=os.path.join(file_or_dir,f)
	#print "loading file %s"%fpath
	wordlist.extend(load_single_file(fpath))

  uniq=set(wordlist)
  return uniq
	

if __name__=='__main__':
  if len(sys.argv)!=2:
    print "usage: ./zoneguesser.py [domainname]"
    sys.exit(1)
  wl=load_wordlist('wordlists')
  domain=sys.argv[1]
  
  res=[]
  for entry in wl:
    word=entry[0]
    rest=entry[1:]
    hostname='%s.%s'%(word,domain)
    for qtype in rest:
      #print "testing %s, %s"%(hostname,qtype)
      res.extend(lookup_dns(hostname,qtype=qtype))
      
  for result in res:
    print "%s\t%s\t%s" %(result['name'],result['typename'],result['data'])
  
  
		
    