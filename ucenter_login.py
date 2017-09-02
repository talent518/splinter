#!/usr/bin/python
# -*- coding: utf8 -*-

from splinter.driver.webdriver.firefox import WebDriver as Browser
import sys

#####################################################
# global instance
GBK = "gbk"
UTF8 = "utf8"

def resultMsg(x):
    """
        judge result and print, x : True or False
    """
    if x == True:
        print 'pass'
    else:
        print '[X]not pass'

def checkresult(x):
    """
        check result message, x : the error message u want
    """
    for tr in browser.find_by_css('.has-error'):
        try:
            sys.stderr.write('%s: %s\n' % (tr.find_by_css('.form-control')['name'], tr.find_by_css('.help-block-error').text))
        except Exception, e:
            print e
    resultMsg(browser.is_text_present(unicode(x, UTF8)))

def fillById(id, val):
    browser.find_by_id(id).first.value = unicode(val, UTF8)

def testLogin(desc, username, password, result):
    """
        fill login form message and submit, check result message and print
    """
    print '\n=========================='
    print(desc)
    print '--------------------------'
    fillById('loginform-username', username)
    fillById('loginform-password', password)
    browser.find_by_name('login-button').first.click()
    checkresult(result)

# chrome driver : http://code.google.com/p/selenium/wiki/ChromeDriver
# already support firefox 55+
browser = Browser()

try:
    browser.visit('http://ucenter.espacetime.com/index.php?r=site%2Flogin')
    print("测试页面: " + browser.title.encode(UTF8))

    # test login
    testLogin('测试未输入用户名', '', '', '用户名不能为空。')
    testLogin('测试未输入密码', 'qd_test_001', '', '密码不能为空。')
    testLogin('测试帐户不存在', '这是一个不存在的名字哦', 'xxxxxxx', '用户名或密码错误！')
    testLogin('测试成功登录', 'admin', 'a123456', '退出 (admin)')

except Exception, x:
    print x

finally:
    browser.quit()
