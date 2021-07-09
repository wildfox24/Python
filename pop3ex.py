#!/usr/bin/env python
# -*- coding: cp1251 -*-
import poplib, string, rfc822, StringIO
p = poplib.POP3("10.0.1.17")
print p.getwelcome()
# этап аутентификации
print p.user("barry")
print p.pass_("<thnedhtp")
# этап транзакций
response, lst, octets = p.list()
print response
mxnum, mxsize = 0, 0
for msgnum, msgsize in map(string.split, lst):
  # print msgnum, msgsize
  if int(msgsize) > mxsize:
    mxnum, mxsize = int(msgnum), int(msgsize)
if mxsize:
  print u"Сообщение %(mxnum)s самое длинное: %(mxsize)s байт" % vars()
  print "UIDL =", string.split(p.uidl(mxnum))[2]
  (resp, lines, octets) = p.top(mxnum, 0)
  msgtxt = string.join(lines, "\n")+"\n\n"
  msg = rfc822.Message(StringIO.StringIO(msgtxt))
#  print u"Удаляем сообщение:"  
#  print "* От: %(from)s\n* Кому: %(to)s\n* Тема: %(subject)s\n" % msg
#  print p.dele(mxnum)
else:
  print u"Ящик пуст."
# этап обновления
print p.quit()
