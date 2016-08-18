__author__ = 'Fengys'
#_*_ coding: utf-8 _*_

import re

pattern = re.compile(r'stockings')

result1 = re.match(pattern, 'stocking')
result2 = re.match(pattern, 'Yuan Ying, I love your stockings')
result3 = re.search(pattern, 'Wang Yan, your legs wearing black stockings are so hot')
result4 = re.search(pattern, 'stockings, Jia Jun\'s white stockings')

if result1:
    print result1.group()
else:
    print "1, fail"

if result2:
    print result2.group()
else:
    print "2, fail"

if result3:
    print result3.group()
else:
    print "3, fail"

if result4:
    print result4.group(0)
else:
    print "4, fail"
