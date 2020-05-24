from crontab import CronTab

my_cron = CronTab(user='pi')
found_job = False

for job in my_cron:
    print('job', job)
    if job.comment == 'test':
        found_job = True
        job.minute.every(5)

if not(found_job) :
    job = my_cron.new(command='python3 /home/pi/Arrosage/pilot/writeDate.py', comment='test')
    job.minute.every(1)

my_cron.write()

print (my_cron)