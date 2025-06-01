from machine import Pin, I2C, UART
import time
import json
import PicoMotorDriver


import utime
import math
import _thread
import uasyncio as asyncio

#GP２５のLEDを出力ピンとして設定 
led = machine.Pin(25, machine.Pin.OUT)

#出力ピンのスイッチをオン（１）
led.value(1)
 
#指定の秒数待機（５）
utime.sleep(5)
 
#出力ピンのスイッチをオフ（０）
led.value(0)

#GPIOピン番号(左モーター)
LEFT_ENC_A = 0
LEFT_ENC_B = 1

#GPIOピン番号(右モーター)
RIGHT_ENC_A = 27
RIGHT_ENC_B = 26

# 変数の初期化
prev_data=[0,0]
gear_ratio = 46.8 # 使用モーター JGA25-371(12v130RPM)
ppr = 11 # 使用モーター JGA25-371(12v130RPM)
delta=2*math.pi/(4*ppr*gear_ratio)
counter=[0,0]
prev_counter=[0,0]
angle = [0,0]
prev_angle = [0,0]
prev_time = 0 #time.time()
prev_phi = [0,0]
velocity = [0,0]
rpm = [0,0]

left_enc_a = machine.Pin(LEFT_ENC_A, machine.Pin.IN, machine.Pin.PULL_UP)
left_enc_b = machine.Pin(LEFT_ENC_B, machine.Pin.IN, machine.Pin.PULL_UP)

right_enc_a = machine.Pin(RIGHT_ENC_A, machine.Pin.IN, machine.Pin.PULL_UP)
right_enc_b = machine.Pin(RIGHT_ENC_B, machine.Pin.IN, machine.Pin.PULL_UP)


# 左モーター　パルスカウント計算
def callback(channel):
    global prev_data,counter,angle,left_enc_a,left_enc_b
    
    current_a = left_enc_a.value()
    current_b = left_enc_b.value()

    encoded = (current_a<<1)|current_b
    sum=(prev_data[0]<<2)|encoded

    #print(bin(sum))
    if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
        counter[0] -= 1
        angle[0]-=delta
    elif (sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
        counter[0] += 1
        angle[0]+=delta

    prev_data[0]=encoded


# 右モーター　パルスカウント計算
def callback2(channel):
    global prev_data,counter,angle,right_enc_a,right_enc_b
    
    current_a = right_enc_a.value()
    current_b = right_enc_b.value()

    encoded = (current_a<<1)|current_b
    sum=(prev_data[1]<<2)|encoded

    # print(bin(sum)) 左と判定が逆になるはず
    if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
        counter[1] += 1
        angle[1]+=delta
    elif (sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
        counter[1] -= 1
        angle[1]-=delta

    prev_data[1]=encoded
    
    
# カウンター値から速度算出
def calc_velocity():
    global counter, prev_counter, prev_phi, prev_time,angle,prev_angle,dt
    # print("angle="+str(angle))

    now=time.time()
    dt = now - prev_time
    # print("dt="+str(dt))
    print("prev_counter[0]="+str(prev_counter[0]))
    print("now="+str(now))
    print("prev_time"+str(prev_time))
    print("dt="+str(dt))
    if dt == 0:
        print("dt is zero")
    else:        
        for i in range(2):    
            if counter[i] != prev_counter[i]:
                phi = counter[i]*delta
                velocity[i] = (phi - prev_phi[i])/dt
                print("velocity["+str(i)+"]="+str(velocity[i]))
                rpm[i] = velocity[i]*60/(2*math.pi)
                print("rpm["+str(i)+"]="+str(rpm[i])) # for debug
                prev_counter[i] = counter[i]
                prev_phi[i] = phi
                prev_angle[i] = angle[i]
            else:
                velocity[i] = 0
                rpm[i] = 0        
        prev_time = now

async def rpm_send():
    print("rpm_send start!!")
    uart = UART(1,115200)
    while True:
        calc_velocity()
        #uartで応答（回転数）
        json_string = json.dumps({"rpm_l":rpm[0],"rpm_r":rpm[1]})
        print(json_string)
        uart.write(json_string.encode('utf-8'))
        uart.write("\r\n".encode())
        await asyncio.sleep(1)

async def uart_rcv():
    print("uart_rcv start!!")
    uart = UART(1,115200)
    send_counter = 0
    while True:        
        buf = bytearray()
        data_flg = False
        while True:
            char = uart.read(1)
            #print(char)
            if char is None:
                break
            #print(char)
            buf.extend(char)
            if char == b'\n':
                data_flg = True
                break
            # time.sleep(0.001)
            await asyncio.sleep(0.001)

        if data_flg == True:
            byte_data = buf
            data_flg = False
        else:
            await asyncio.sleep(0.001)
            continue        
                
        if byte_data is not None:
            led.value(0) # for debug
            if 'start' in byte_data:
                print("yes start")
                
            elif 'emergency_stop' in byte_data:
                print("emergency_stop")
                board.motorOff(1)
                board.motorOff(2)
                #led.value(0) # for debug
                continue
            else:
                #led.value(0) # for debug
                continue
             
            #led.value(0) # for debug
            
            str_data = byte_data.decode('utf-8').split('$')[1]
            if len(str_data) != 0:
                try:
                    json_data = json.loads(str_data)
                except ValueError as e:
                    print("JSON Error!!")
                    continue

                v_r = json_data["v_r"]
                v_l = json_data["v_l"]

                # add uart --->
                if v_r > 0 and v_l > 0:
    #                 print("forward!!")
                    board.motorOn(1, 'f', abs(v_r))
                    board.motorOn(2, 'f', abs(v_l))

                elif v_r > 0 and v_l < 0:
    #                 print("right!!")
                    board.motorOn(1, 'f', abs(v_r))
                    board.motorOn(2, 'r', abs(v_l))

                elif v_r < 0 and v_l > 0:
#                 print("left!!")
                    board.motorOn(1, 'r', abs(v_r))
                    board.motorOn(2, 'f', abs(v_l))

                elif v_r < 0 and v_l < 0:
#                 print("back!!")
                    board.motorOn(1, 'r', abs(v_r))
                    board.motorOn(2, 'r', abs(v_l))

                else:
                    #led.value(0) # for debug
                    board.motorOff(1)
                    board.motorOff(2)
            else:
                #led.value(0) # for debug
                board.motorOff(1)
                board.motorOff(2)



# 割り込みイベントの設定
left_enc_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,  handler=callback)
left_enc_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,  handler=callback)

right_enc_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,  handler=callback2)
right_enc_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,  handler=callback2)


async def main():
    await asyncio.gather(uart_rcv(),rpm_send())


if __name__ == "__main__":
     board = PicoMotorDriver.KitronikPicoMotor()
     asyncio.run(main())







