#!/usr/bin/env python
# -*- coding: cp1251 -*-
import poplib, string, rfc822, StringIO
p = poplib.POP3("10.0.1.17")
print p.getwelcome()
# ���� ��������������
print p.user("barry")
print p.pass_("<thnedhtp")
# ���� ����������
response, lst, octets = p.list()
print response
mxnum, mxsize = 0, 0
for msgnum, msgsize in map(string.split, lst):
  # print msgnum, msgsize
  if int(msgsize) > mxsize:
    mxnum, mxsize = int(msgnum), int(msgsize)
if mxsize:
  print u"��������� %(mxnum)s ����� �������: %(mxsize)s ����" % vars()
  print "UIDL =", string.split(p.uidl(mxnum))[2]
  (resp, lines, octets) = p.top(mxnum, 0)
  msgtxt = string.join(lines, "\n")+"\n\n"
  msg = rfc822.Message(StringIO.StringIO(msgtxt))
#  print u"������� ���������:"  
#  print "* ��: %(from)s\n* ����: %(to)s\n* ����: %(subject)s\n" % msg
#  print p.dele(mxnum)
else:
  print u"���� ����."
# ���� ����������
print p.quit()
