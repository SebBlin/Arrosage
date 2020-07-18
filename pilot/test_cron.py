from crontab import CronTab

my_cron = CronTab(user='pi')
found_job = False

for job in my_cron:
    print('job', job)
    if job.comment == 'test':
        found_job = True
        job.minute.on(23)
        job.hour.on(20)
        job.dow.on('SUN', 'FRI')


if not(found_job) :
    job = my_cron.new(command='python3 /home/pi/Arrosage/pilot/writeDate.py', comment='test')
    job.minute.every(1)

my_cron.write()

print (my_cron)