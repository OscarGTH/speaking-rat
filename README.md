This project is a hobby project that makes a plush toy rat speak random things with text-to-speech.
Program is being run on Raspberry Pi and called every hour with Crontab.
When program is being ran, it randomly calls an API and speaks out the result. Currently there are 4 possible APIs.
They are current day's sunrise and sunset time, programming quote, your mom joke and an inspirational quote.

You are free to use this project as you wish.

The program is meant to be run by crontab so you can add this to your crontab. (by running command crontab -e)
*/5 * * * * <path-to-virtual-env>/bin/python <path-to-project>/speaking-rat/src/run_rat.py
