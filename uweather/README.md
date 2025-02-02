# uweather - Reporting weather using UART
For this one the weather is randomised using numpy, but in the `live` branch it is read from the bmp280 sensor.

## Raspberry Pi
Sit in an infinite loop and wait for a `SIG_ENQ` signal (`\x05`), after recieving it, acknowledge with `SIG_ACK` and begin measurement. Once the measurement is complete save the data to a csv file and send it. After sending the file send a `SIG_END` to signal the reciever to finish waiting.

There is no problem with sending the file as is, because it is read as valid bytes by using the `"rb"` flag with the call to open. Traditionally on POSIX systems the `b` modifier has no impact, but Python never ceases to amaze me.

## Analog Discovery
Send a signal to the Raspberry Pi, and wait patiently. A spinner is added for the unpatient. After recieving `SIG_END` save the read file.
