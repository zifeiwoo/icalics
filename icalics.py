#!/usr/bin/python  
#-*-coding:utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from urllib2 import urlopen
import socket,json
from ics import Calendar, Event

import Config
class Holiday(Calendar):
    """
    generate Chinese Holiday
    """
    def __init__(self, imports=None, events=None, creator="介川"):
        super(Holiday,self).__init__(imports,events,creator)
    def __get_holiday(self,year):
        months=[year+ "%02d" % x for x in range(1,13)]
        holiday_url = 'http://www.easybots.cn/api/holiday.php?m=%s' % ",".join(months)

        DateInfos={}
        try:
            response = urlopen(holiday_url,timeout=5)
        #except socket.timeout as e:
        except Exception as e:
            print e
            return {}
        #输出json格式：工作日对应结果为 0,休息日对应结果为 1, 节假日对应的结果为 2；
        resp_json = json.loads(response.read())
        for month in resp_json:
            for day in resp_json[month]:
                if "0" == resp_json[month][day]:
                    DateInfos[month+day] = '工作日'
                elif "1" == resp_json[month][day] or "2" == resp_json[month][day]:
                    DateInfos[month+day] = '休息日'
        return DateInfos

    def append(self,year):
        for _date,_info in self.__get_holiday(year).iteritems():
            e = Event()
            e.name = _info
            e.begin = '%s-%s-%s 00:00:00' % (year,_date[4:6],_date[6:8])
            e.make_all_day()
            e.description="edited by 介川"
            self.events.append(e)

    def dump(self,file):
        with open(file, 'w') as f:
            f.writelines(self)
        
class LumarTaboo(Calendar):
    """
    The almanac and taboo class
    """
    def __init__(self, imports=None, events=None, creator="介川"):
        super(LumarTaboo,self).__init__(imports,events,creator)
    def __get_lumar_taboo(self,year):
        #宜凶
        yj_url = 'http://51wnl.com/YJData/%s.json' % year 
        #命理
        lumar_url = 'http://51wnl.com/moreLumarData/%s.json' % year

        DateInfos={}
        try:
            response = urlopen(yj_url,timeout=5)
        except Exception as e:
            print "Fail to get YJData,E:",e
            return DateInfos
        resp_json = json.loads(response.read())
        for _mmdd,_info in resp_json.iteritems():
            DateInfos[year+_mmdd[1:]] = _info

        try:
            response = urlopen(lumar_url,timeout=5)
        except Exception as e:
            print "Fail to get LumarData,E:",e
            return DateInfos
        resp_json = json.loads(response.read())
        for _mmdd,_info in resp_json.iteritems():
            DateInfos[year+_mmdd] = _info
            
        return DateInfos

    def append(self,year):
        for _date,_info in self.__get_lumar_taboo(year).iteritems():
            e = Event()
            e.name = _info
            e.begin = '%s-%s-%s 00:00:00' % (year,_date[4:6],_date[6:8])
            e.make_all_day()
            e.description="edited by 介川"
            self.events.append(e)

    def dump(self,file):
        with open(file, 'w') as f:
            f.writelines(self)

def main():
    h=Holiday()
    h.append("2015")
    h.dump(Config.holiday_file)

    # lt=LumarTaboo()
    # lt.append("2015")
    # print lt
if __name__ == "__main__":
    main()
