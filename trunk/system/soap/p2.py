'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
# $Id: p2.py,v 1.15a 2002/05/11 10:07:18 phr Exp phr $

# Simple p2 encryption "algorithm": it's just SHA used as a stream
# cipher in output feedback mode.  

# Author: Paul Rubin, Fort GNOX Cryptography, <phr-crypto at nightsong.com>.
# Algorithmic advice from David Wagner, Richard Parker, Bryan
# Olson, and Paul Crowley on sci.crypt is gratefully acknowledged.

# Copyright 2002 by Paul Rubin

# License: For review and testing purposes only.  Distribution
# unrestricted until June 1, 2002.  Do not use or distribute after
# June 1, 2002.  Do not distribute with the date check (time bomb)
# below disabled.

# Reason: I don't want this code to circulate if bugs are discovered
# in it.  I will release a new version under a free software license
# without the date restriction, sometime before June 1, 2002.  Once
# the new version is available, please use it instead of this version.

# WARNING: DO NOT EXPECT SECURITY FROM THIS CODE.  Wait for a version
# that's been reviewed and tested more.  This code is circulated for
# review and testing purposes ONLY.

# Please include this revision number in any bug reports: $Revision: 1.15 $

from string import join
from array import array
import sha
from time import time

class CryptError(Exception): pass
def _hash(str): return sha.new(str).digest()

_ivlen = 16
_maclen = 8
_state = _hash(`time()`)

try:
    import os
    _pid = `os.getpid()`
except ImportError, AttributeError:
    _pid = ''

def _expand_key(key, clen):
    blocks = (clen+19)/20
    xkey=[]
    seed=key
    for i in xrange(blocks):
        seed=sha.new(key+seed).digest()
        xkey.append(seed)
    j = join(xkey,'')
    return array ('L', j)

def p2_encrypt(plain,key):
    global _state
    H = _hash

    # change _state BEFORE using it to compute nonce, in case there's
    # a thread switch between computing the nonce and folding it into
    # the state.  This way if two threads compute a nonce from the
    # same data, they won't both get the same nonce.  (There's still
    # a small danger of a duplicate nonce--see below).
    _state = 'X'+_state

    # Attempt to make nlist unique for each call, so we can get a
    # unique nonce.  It might be good to include a process ID or
    # something, but I don't know if that's portable between OS's.
    # Since is based partly on both the key and plaintext, in the
    # worst case (encrypting the same plaintext with the same key in
    # two separate Python instances at the same time), you might get
    # identical ciphertexts for the identical plaintexts, which would
    # be a security failure in some applications.  Be careful.
    nlist = [`time()`, _pid, _state, `len(plain)`,plain, key]
    nonce = H(join(nlist,','))[:_ivlen]
    _state = H('update2'+_state+nonce)
    k_enc, k_auth = H('enc'+key+nonce), H('auth'+key+nonce)
    n=len(plain)                        # cipher size not counting IV

    stream = array('L', plain+'0000'[n&3:]) # pad to fill 32-bit words
    xkey = _expand_key(k_enc, n+4)
    for i in xrange(len(stream)):
        stream[i] = stream[i] ^ xkey[i]
    ct = nonce + stream.tostring()[:n]
    auth = _hmac(ct, k_auth)
    return ct + auth[:_maclen]

def p2_decrypt(cipher,key):
    H = _hash
    n=len(cipher)-_ivlen-_maclen        # length of ciphertext
    if n < 0:
        raise CryptError, "invalid ciphertext"
    nonce,stream,auth = \
      cipher[:_ivlen], cipher[_ivlen:-_maclen]+'0000'[n&3:],cipher[-_maclen:]
    k_enc, k_auth = H('enc'+key+nonce), H('auth'+key+nonce)
    vauth = _hmac (cipher[:-_maclen], k_auth)[:_maclen]
    if auth != vauth:
        raise CryptError, "invalid key or ciphertext"

    stream = array('L', stream)
    xkey = _expand_key (k_enc, n+4)
    for i in xrange (len(stream)):
        stream[i] = stream[i] ^ xkey[i]
    plain = stream.tostring()[:n]
    return plain

# RFC 2104 HMAC message authentication code
# This implementation is faster than Python 2.2's hmac.py, and also works in
# old Python versions (at least as old as 1.5.2).
from string import translate
def _hmac_setup():
    global _ipad, _opad, _itrans, _otrans
    _itrans = array('B',[0]*256)
    _otrans = array('B',[0]*256)    
    for i in xrange(256):
        _itrans[i] = i ^ 0x36
        _otrans[i] = i ^ 0x5c
    _itrans = _itrans.tostring()
    _otrans = _otrans.tostring()

    _ipad = '\x36'*64
    _opad = '\x5c'*64

def _hmac(msg, key):
    if len(key)>64:
        key=sha.new(key).digest()
    ki = (translate(key,_itrans)+_ipad)[:64] # inner
    ko = (translate(key,_otrans)+_opad)[:64] # outer
    return sha.new(ko+sha.new(ki+msg).digest()).digest()

#
# benchmark and unit test
#

def _time_p2(n=1000,len=20):
    plain="a"*len
    t=time()
    for i in xrange(n):
        p2_encrypt(plain,"abcdefgh")
    dt=time()-t
    print "plain p2:", n,len,dt,"sec =",n*len/dt,"bytes/sec"

def _speed():
    _time_p2(len=5)
    _time_p2()
    _time_p2(len=200)
    _time_p2(len=2000,n=100)

def _test():
    e=p2_encrypt
    d=p2_decrypt

    plain="test plaintext"
    key = "test key"
    c1 = e(plain,key)
    c2 = e(plain,key)
    assert c1!=c2
    assert d(c2,key)==plain
    assert d(c1,key)==plain
    c3 = c2[:20]+chr(1+ord(c2[20]))+c2[21:] # change one ciphertext character

    try:
        print d(c3,key)         # should throw exception
        print "auth verification failure"
    except CryptError:
        pass

    try:
        print d(c2,'wrong key')         # should throw exception
        print "test failure"
    except CryptError:
        pass

_hmac_setup()
_test()
#_speed()                                # uncomment to run speed test
