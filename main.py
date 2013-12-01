#coding: utf-8
import os
import gmail
import tornado.ioloop
import tornado.web
from configs import *

def make_feeds(mails):
    res = []
    for x in mails:
        item = {}
        item['date'] = x.sent_at.strftime('%Y-%m-%d %Hh')
        if x.subject == 'Foursquare':
            li = x.body.split(' ')
            if len(li) == 1: li.append('#')
            item['content'] = '我在<a href="%s">%s</a>'%(li[1], li[0])
        elif x.subject == 'Pocket':
            li = x.body.split(' http')
            if len(li) == 1: li.append('#')
            item['content'] = '我在Pocket中加入了<a href="%s">%s</a>'%('http'+li[1], li[0])
        elif x.subject == 'Reminder_add':
            item['content'] = '我添加了一个任务：%s'%x.body
        elif x.subject == 'Reminder_complete':
            item['content'] = '我完成了一个任务：%s'%x.body
        elif x.subject == 'Calendar':
            li = x.body.split(' http')
            item['content'] = '我开始了一个日程：<a href="%s">%s</a>'%('http'+li[1], li[0])
        else:
            item['content'] = '无法识别'
        res.append(item)
        res.reverse()
    return res



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        g = gmail.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        mails = g.label("info").mail()
        res = ''
        for m in mails[:20]:
            m.fetch()
        feeds = make_feeds(mails[:20])
        self.render('index.html', feeds = feeds)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
application = tornado.web.Application([
    (r"/", MainHandler),
    ], **settings)

if __name__ == "__main__":
    application.listen(8882)
    tornado.ioloop.IOLoop.instance().start()
