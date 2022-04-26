import sensor, image, lcd, time
import KPU as kpu
import gc, sys
import utime

def numrecog(img,x,y,w,h):
    count = 10
    x_half = w//2
    y_half = h//2
    y_one = h//3 + 1
    y_two = (h//3) * 2 + 1
    xx1_1,xx1_2,xx2_1,xx2_2=0,0,0,0
    yy_1,yy_2,yy_3=0,0,0
    #|线交叉点
    for i0 in range(0,h):
        n0 = img.get_pixel(x+x_half, y+i0)    
        #if not n0:
        #    break    
        if(i0 < y_one):
            if(int(n0) == 255):
                yy_1 = 1
        elif((i0 >= y_one)and(i0 < y_two)):
            if(int(n0) == 255):
                yy_2 = 1
        else:
            if(int(n0) == 255):
                yy_3 = 1
    #-线交叉点
    for i1 in range(0,w):
        n1 = img.get_pixel(x+i1, y+y_one)    
        #if not n1:
        #    break  
        if(i1 < x_half):
            if(int(n1) == 255):
                xx1_1 = 1
        else:    
            if(int(n1) == 255):
                xx1_2 = 1
                
    #-线交叉点
    for i2 in range(0,w):
        n2 = img.get_pixel(x+i2, y+y_two)    
        #if not n2:
        #    break  
        if(i2 < x_half):
            if(int(n2) == 255):
                xx2_1 = 1
        else:    
            if(int(n2) == 255):
                xx2_2 = 1       
    
    if((yy_1 == 1)and(yy_2 == 0)and(yy_3 == 1)and(xx1_1 == 1)and(xx1_2 == 1)and(xx2_1 == 1)and(xx2_2 == 1)):
        count = 0
    elif((yy_1 == 1)and(yy_2 == 0)and(yy_3 == 0)and(xx1_1 == 0)and(xx1_2 == 1)and(xx2_1 == 0)and(xx2_2 == 1)):#1???
        count = 1
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 0)and(xx1_2 == 1)and(xx2_1 == 1)and(xx2_2 == 0)):
        count = 2
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 0)and(xx1_2 == 1)and(xx2_1 == 0)and(xx2_2 == 1)):
        count = 3
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 0)and(xx1_1 == 1)and(xx1_2 == 1)and(xx2_1 == 0)and(xx2_2 == 1)):#4???
        count = 4
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 1)and(xx1_2 == 0)and(xx2_1 == 0)and(xx2_2 == 1)):
        count = 5
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 1)and(xx1_2 == 0)and(xx2_1 == 1)and(xx2_2 == 1)):
        count = 6
    elif((yy_1 == 1)and(yy_2 == 0)and(yy_3 == 1)and(xx1_1 == 0)and(xx1_2 == 1)and(xx2_1 == 0)and(xx2_2 == 1)):
        count = 7
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 1)and(xx1_2 == 1)and(xx2_1 == 1)and(xx2_2 == 1)):
        count = 8
    elif((yy_1 == 1)and(yy_2 == 1)and(yy_3 == 1)and(xx1_1 == 1)and(xx1_2 == 1)and(xx2_1 == 0)and(xx2_2 == 1)):
        count = 9    
    else:
        count = 7
        
    if count == 8:
        n3 = img.get_pixel(x+x_half, y+y_one)
        n4 = img.get_pixel(x+x_half, y+y_two)
        n5 = img.get_pixel(x+x_half, y+y_half)
        if((int(n3) == 0)and(int(n4) == 0)):
            count = 8
        elif((int(n3) == 255)and(int(n4) == 255)and(int(n5) == 255)): 
            count = 1
        else:
            count = 4
            
    return count


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing(size=(224,224))
sensor.set_hmirror(False)
sensor.set_vflip(False)
sensor.run(1)

lcd.init(type=1)
lcd.rotation(0)
lcd.clear(lcd.WHITE)
i = 1

while(True):    
#for i in range(1,201):
    #utime.sleep_ms(1000)
    t = time.ticks_ms()
    img = image.Image("/sd/numdata4/"+str(i)+".jpg")
    img = img.to_rgb565(copy=True)
    img.pix_to_ai()
    
    if(i < 200):
        i = i + 1
    else:
        i = 1
    img2 = img.copy(roi=(26, 126, 170, 25))
    
    img2 = img2.to_grayscale(copy=False)
    #二值化
    for x in range(0,170):
        for y in range(0,25):
            n = img2.get_pixel(x, y)      
            if not n:
                break;
            if( int(n) >= 100):
                #img2 = img2.set_pixel(x, y, (255, 255, 255))
                img2 = img2.set_pixel(x, y, 255)
            else :
                #img2 = img2.set_pixel(x, y, (0, 0, 0))
                img2 = img2.set_pixel(x, y, 0) 
    '''
    img2.draw_rectangle(0+1, 0, 14, 25)
    img2.draw_rectangle(0+32, 0, 14, 25)
    img2.draw_rectangle(0+32*2-1, 0, 14, 25)
    img2.draw_rectangle(0+32*3-2, 0, 14, 25)
    img2.draw_rectangle(0+32*4-3, 0, 14, 25)
    img2.draw_rectangle(0+32*5-4, 0, 14, 25)
    '''
    
    #数字穿线法
    count1 = numrecog(img=img2,x=1,y=0,w=14,h=25)  
    count2 = numrecog(img=img2,x=32,y=0,w=14,h=25)
    count3 = numrecog(img=img2,x=32*2-1,y=0,w=14,h=25) 
    count4 = numrecog(img=img2,x=32*3-2,y=0,w=14,h=25)
    count5 = numrecog(img=img2,x=32*4-3,y=0,w=14,h=25)
    count6 = numrecog(img=img2,x=32*5-4,y=0,w=14,h=25)    
    number = 'num:'+str(count1)+','+str(count2)+','+str(count3)+','+str(count4)+','+str(count5)+','+str(count6)
    img.draw_string(0, 40, number, scale=2, color=(255, 255, 255))
    
    #img2.draw_rectangle(0+32*5-4, 0, 14, 25)
    #count6 = numrecog(img=img2,x=32*5-4,y=0,w=14,h=25)  
    #img2.draw_string(20, 0, str(count6), scale=2, color=(255, 255, 255))
    t = time.ticks_ms() - t
    img.draw_string(0, 180, "t:%dms" %(t), scale=2, color=(255, 0, 0))
    lcd.display(img)
    
gc.collect()    
'''

lcd.init(freq=15000000)
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    #img = sensor.snapshot()         # Take a picture and return the image.
    img = image.Image("/sd/numdata2/1.jpg")
    lcd.display(img)                # Display on LCD
    print(clock.fps())              # Note: MaixPy's Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
'''