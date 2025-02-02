# upager - UART Pager
Asynchronously send messages from your Raspberry Pi to the Analog Discovery board and vice-versa.

In order to make recieving non-blocking it is done in another thread. These functions read non-null bytes until the delimeter (`SIG_END`) is sent `\x03` and after recieving the full message, they pass it to the main thread.

## Raspberry Pi
Utilises ANSI Escape Codes to asynchronously write the messages recievied in another thread to stdout.

## Analog Discovery
Because it runs locally (not using SSH) a simple GUI using tkinter was made, which clutters up the code. Important parts of that program:
- `Window.msg_q` - a Queue used for passing messages from the recieving thread
- `Window.rx_thread()` - the function running in the recieving thread
- `Window.check_msg_q()` - every 250ms checks if there are any messages in the queue and displays the most recent one
