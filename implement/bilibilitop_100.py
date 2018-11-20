import requests
import smtplib
import socket

from lxml import etree
from implement.settings import *
from smtplib import SMTPRecipientsRefused,SMTPServerDisconnected
from email.header import Header
from email.mime.text import MIMEText


url = 'https://www.bilibili.com/ranking'

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
	'Host':'www.bilibili.com'
}

def get_top_100(url=url):
	html = requests.get(url,headers=headers).text
	selector = etree.HTML(html)
	top_list_xpath = selector.xpath("//ul[@class='rank-list']/li[@class='rank-item']")

	for item in top_list_xpath:
		item_info = {}
		item_info['rank'] = item.xpath("./div[@class='num']/text()")[0] if item.xpath("./div[@class='num']") else ''
		item_info['title'] = item.xpath("./div[@class='content']/div[@class='info']/a/text()")[0] if item.xpath("./div[@class='content']/div[@class='info']/a/text()") else ''
		item_info['score'] = item.xpath("./div[@class='content']/div[@class='info']/div[@class='pts']/div/text()")[0] if item.xpath("./div[@class='content']/div[@class='info']/div[@class='pts']/div/text()") else ''
		item_info['link'] = item.xpath("./div[@class='content']/div[@class='info']/a/@href")[0].replace('//','') if item.xpath("./div[@class='content']/div[@class='info']/a/@href") else ''

		yield '排名: {rank} 标题: {title} 评分: {score} 链接: {link}'.format(rank=item_info['rank'], title=item_info['title'], score=item_info['score'], link=item_info['link']) + '\n'

def send_to_email(email_host=EMAIL_HOST, email_host_user=EMAIL_HOST_USER, email_host_password=EMAIL_HOST_PASSWORD, email_recevier=EMAIL_RECEIVER):

	if IS_SEND:
		content = ''
		for item in get_top_100():
			content += item

		client = smtplib.SMTP(email_host)
		client.login(email_host_user,email_host_password)
		msg = MIMEText(content, 'plain', 'utf-8')
		msg['Subject'] = Header(EMAIL_SUBJECT_PREFIX, 'utf-8')
		msg['From'] = email_host_user
		msg['To'] = email_recevier
		try:
			client.sendmail(email_host_user, [email_recevier,], msg.as_string())
			print('邮件发送成功')
			client.quit()
		except SMTPRecipientsRefused:
			print('邮箱地址错误')
		except socket.gaierror:
			print('网络连接失败') 
		except SMTPServerDisconnected:
			print('服务器发送错误') 
		except Exception as e:
			raise e
	else:
		print('停止发送,若要继续发送请将IS_SEND设置为True')
