To run the the contianer you have to specify the port on the container and the target port (in this case port 5002 on my machine maps to port 5000 on the container).
````
docker run -p 5002:5000 beep-app:1.1
```
If you use this command, it won't print the beeps.

To print the beeps you need the -it (interactive & terminal) flagas:
````
docker run -it -p 5002:5000 beep-app:1.1
```
Otherwise the stdout gets sent to a buffer. 

If you make a few thousand requests (`for i in range(2000): requests.get('http://127.0.0.1:5002')`) then it will eventually empty out the buffer.

In principle it will also empty the buffer if you kill the app process, but in practice if you kill process 1 on the container (the app process) then the container will die.

