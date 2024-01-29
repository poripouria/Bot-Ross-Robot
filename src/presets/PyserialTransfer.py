import time
from pySerialTransfer import pySerialTransfer as txfer


if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('COM3')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        
        while True:
            send_size = 0
            
            ###################################################################
            # Send a string
            ###################################################################
            str_ = '1+-'
            str_size = link.tx_obj(str_, send_size) - send_size
            send_size += str_size
            
            link.send(send_size)
            
            ###################################################################
            # Wait for a response and report any errors while receiving packets
            ###################################################################
            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))
            

            ###################################################################
            # Parse response string
            ###################################################################
            rec_str_   = link.rx_obj(obj_type=type(str_),
                                     obj_byte_size=str_size,
                                     start_pos=0)
            
            ###################################################################
            # Display the received data
            ###################################################################
            print('SENT: {}'.format(str_))
            print('RCVD: {}'.format(rec_str_))
            print(' ')
    
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass
