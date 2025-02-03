# utag - RFID Tags through UART
Write RFID Tags using the UART protocol. This example in most simple terms is a server and a client. The server is the Raspberry Pi, which is waiting for requests from the client (Analog Discovery).

## Raspberry Pi
Sit in a loop and wait for commands from the client. Based on the recieved signal (`SIG_WRT` or `SIG_REA`) perform writing or reading the tag.

## Analog Discovery
Another GUI app made with tkinter, which clutters the code. Two functions are of interest: `read_tag` and `write_tag`. They coordinate the actions with the server, send or recieve expected data. After all is done display the results to the user.
