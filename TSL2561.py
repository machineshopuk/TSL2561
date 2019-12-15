###########################################
# Created by The Machine Shop 2019        #
# Visit our website TheMachineShop.uk     #
# This script interfaces the Zio Qwiic    #
# ZIO QWIIC LIGHT SENSOR TSL2561	  #
# to a Raspberry Pi over i2c and converts #
# the data to visible light, invisible    #
# light (IR) and full light.	          #
# requires python-smbus to be installed:  #
# sudo apt-get install python-smbus       #
###########################################

#import the required libraries
import smbus
import time

# Start the i2c bus and label as 'bus'
bus = smbus.SMBus(1)

# Setup the control register
bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)

# Setup the timing register
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

# Allow a short delay
time.sleep(0.5)

# Perform an I2C data transfer by sending the command register and retrieving 
# 2 bytes of data. The command register comprises of the CMD bit (0x80) and 
# the address of the data you wish to acquire (0x0C), when they are OR'd 
# together they create the command register. This is transmitted to the TSL2561
# and the response is the lower and upper byte of ADC Channel 0 (full spectrum) 
data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

# Then do the same for the ADC Channel 1 (IR light)
data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

# The data currently comprises of two bytes. The upper byte is bit shifted by 8 bits
# to the right by multiplying it by 256 and then the lower byte is added thus 
# creating a 16-bit value. This is then repeated for the other Channel.
ch0 = data[1] * 256 + data[0]
ch1 = data1[1] * 256 + data1[0]

# Then the data is outputted in a nice human readable form. To generate the visible
# only value, the IR light value is subtracted from the full spectrum light value.
print "Full Spectrum(IR + Visible) :%d lux" %ch0
print "Infrared Value :%d lux" %ch1
print "Visible Value :%d lux" %(ch0 - ch1)
