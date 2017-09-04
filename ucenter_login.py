#!/usr/bin/python
# -*- coding: utf8 -*-

from splinter.driver.webdriver.firefox import WebDriver as Browser
import os, sys
import platform

#####################################################
# global instance
GBK = "gbk"
UTF8 = "utf8"
isWindows = platform.system() == 'Windows'

def output(x, f=None):
    if f is None:
        f = sys.stdout

    f.write(u'%s\n' % (x.decode(UTF8) if isinstance(x, str) else x))
    f.flush()

def resultMsg(x):
    """
        judge result and print, x : True or False
    """
    if x == True:
        output('pass')
    else:
        output('[X]not pass')

def checkresult(x):
    """
        check result message, x : the error message u want
    """
    for tr in browser.find_by_css('.has-error'):
        try:
            output(u'\t%s: %s\n' % (tr.find_by_css('.form-control')['name'], tr.find_by_css('.help-block-error').text), f=sys.stderr)
        except Exception, e:
            output(e)
    resultMsg(browser.is_text_present(unicode(x, UTF8)))

def fillById(id, val):
    browser.find_by_id(id).first.value = unicode(val, UTF8)

def screenshot(name):
    browser.screenshot(os.path.join(os.path.dirname(__file__), '%s-' % (name.decode(UTF8).encode(GBK) if isWindows else name)))

def testLogin(desc, username, password, result):
    """
        fill login form message and submit, check result message and print
    """
    output('\n==========================')
    output(desc)
    output('--------------------------')
    fillById('loginform-username', username)
    fillById('loginform-password', password)
    browser.find_by_name('login-button').first.click()
    screenshot(desc)
    checkresult(result)

# chrome driver : http://code.google.com/p/selenium/wiki/ChromeDriver
# already support firefox 55+
browser = Browser()

try:
    browser.visit('http://ucenter.espacetime.com/index.php?r=site%2Flogin')
    output("测试页面: " + browser.title.encode(UTF8))

    # test login
    testLogin('01-测试未输入用户名', '', '', '用户名不能为空。')
    testLogin('02-测试未输入密码', 'qd_test_001', '', '密码不能为空。')
    testLogin('03-测试帐户不存在', '这是一个不存在的名字哦', 'xxxxxxx', '用户名或密码错误！')
    testLogin('04-测试成功登录', 'admin', 'a123456', '退出 (admin)')

except Exception, x:
    output(x)
    screenshot('00-except')

finally:
    browser.quit()
