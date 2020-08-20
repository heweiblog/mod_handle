#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click,sys,json,threading,time,logging,schedule
from daemonocle.cli import DaemonCLI


logger = logging.getLogger('crm-run')
handler = logging.FileHandler('run.log')
logger.setLevel(logging.INFO) #设置没生效
formatter = logging.Formatter('%(asctime)s|%(filename)s|%(lineno)d|%(levelname)s|%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def main_task():
	num = 1
	while True:
		logger.info('num is {}'.format(num))
		time.sleep(5)
		num += 1
		

def job_a():
	logger.warning('time is 18:15')

def job(status):
	logger.warning('status is {}'.format(status))


@click.command(cls=DaemonCLI, daemon_params={'pidfile': 'test.pid'})
@click.option('-v',help='Show version and exit')
def main():
	schedule.every().day.at("18:15").do(job_a)
	schedule.every(1).minutes.do(job,'good')
	threading._start_new_thread(main_task,())
	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == '__main__':
	if len(sys.argv) == 2 and (sys.argv[1] == '-v' or sys.argv[1] == 'version'):
		print('1.0.21')
		sys.exit(0)
	main()



