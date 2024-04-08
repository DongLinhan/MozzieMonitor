#### #### #### #### MozzieMonitor #### #### #### ####
#### Linhan Dong, Duvall Lab, Columbia Unversity ####
# Version hostory:
# 111023: basic preview and picture taking function with 1 min / pic frquency
# 111223: updated: more commandline real-time information; recording time
#         control, and pic_name reflects start recording time. 000000 marks
#         first picture at start time.



#from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2, Preview
import datetime
import time
import os
#from ismember import ismember
#from libcamera import controls

#inputs
experiment_name = 'trial_for_real' # specify genotype and entrainment etc
experiment_duration = 72 # in hours, it's okay to overshoot a bit, default 72
recording_start_hour = 23 # in 24 hour time format

#internal parameters - do not change
min_counter = 61 
hour_counter = 25
hour_elapsed = -1

#parameters derived from inputs:
output_dir = ('/home/pi/' + experiment_name)
os.mkdir(output_dir)

if recording_start_hour > datetime.datetime.now().hour:
    wait_hour = recording_start_hour - datetime.datetime.now().hour - 1
    wait_minute = (60 - datetime.datetime.now().minute) + (wait_hour * 60)
    pic_counter = 0 - wait_minute
elif recording_start_hour < datetime.datetime.now().hour:
    wait_hour = recording_start_hour + (23 - datetime.datetime.now().hour)
    wait_minute = (60 - datetime.datetime.now().minute) + (wait_hour * 60)
    pic_counter = 0 - wait_minute
elif recording_start_hour == datetime.datetime.now().hour:
    print("Warning: the hour to start recording is same as the hour right now - recording will proceed with first pic named 000000")
    pic_counter = 0



# Preview
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.options["quality"] = 95
picam2.start_preview(Preview.QT)
picam2.start()
pause = input('Press Enter to end preview and continue')
picam2.stop_preview()
picam2.stop()


#Taking 1 pic / min until hours_elapsed = experiment duration

while hour_elapsed < experiment_duration:

    if min_counter != datetime.datetime.now().minute:
        print(datetime.datetime.now(), f'This is a new minute')
        print ("Taking picture #" + str(pic_counter) + " now")
        image_name = os.path.join(output_dir, '{:06d}.jpg'.format(pic_counter))
        still_config = picam2.create_still_configuration({"size" : (1200, 800)})
        picam2.configure(still_config)
        picam2.start()
        time.sleep(2) #warm up camera for 2 secs
        picam2.capture_file(image_name)
        picam2.stop()
        pic_counter = pic_counter + 1
        min_counter = datetime.datetime.now().minute
        
    if hour_counter != datetime.datetime.now().hour:
        hour_counter = datetime.datetime.now().hour
        hour_elapsed = hour_elapsed + 1
        print ("This is a new hour. It has been " + str(hour_elapsed) + " / " + str(experiment_duration) + " hours of recording" )
                
        