mosquitto_pub -h raspberrypigio2.zapto.org -p 8883 -u giobart -P qwerty99 -t 'door/open' -m '{"open":false,"to":"door_lock_1","user":"test"}' -q 0
