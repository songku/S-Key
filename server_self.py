import random
import socket
import hashlib
import os
import time

host = socket.gethostname()
port = 6666
userlist = {}


def md5(string):
    md5_var = hashlib.md5()
    md5_var.update(string.encode("utf-8"))
    return md5_var.hexdigest()


def init_talk(client_socket):
    seed = str(random.randint(10000000, 99999999))
    client_socket.send(seed.encode("utf-8"))
    initial_pass = client_socket.recv(32).decode("utf-8")
    userlist[username] = initial_pass


def init_log(user):
    if not os.path.exists(f"./{user}"):
        os.mkdir(f"./{user}")


def log_message(user, message, addr):
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_text = f"{log_time}用户{user}{message},登录自{addr}\n"
    with open(f'./{user}/log.txt', 'a') as f:
        f.write(log_text)


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print("等待连接...")
    server_socket.listen(3)  # 设置可以监听三个客户端
    while True:
        # 接收客户端连接并保存套接字和ip地址
        client_socket, client_addr = server_socket.accept()
        print(f"监听到来自{client_addr[0]}的连接")
        # 接收用户名
        username = client_socket.recv(16).decode("utf-8")
        if username in userlist.keys():
            # 如果用户注册过
            print(f"用户{username}尝试登录")
            log_message(username, "尝试登录", client_addr[0])
            client_socket.send('1'.encode("utf-8"))
            recv_key = client_socket.recv(32).decode("utf-8")
            hash_key = md5(recv_key)
            if userlist[username] == hash_key:
                print(f"用户{username}登录成功")
                log_message(username, "登录成功", client_addr[0])
                client_socket.send("right".encode("utf-8"))
                userlist[username] = recv_key  # 更新替换username的口令
                print("与客户端协商是否重新初始化N及口令")
                sign = client_socket.recv(1).decode("utf-8")
                if sign == '1':
                    print("与客户端协商N并初始化口令")
                    log_message(username, "重新协商", client_addr[0])
                    init_talk(client_socket)
                else:
                    # 不协商，程序继续正常运行
                    print("不协商，正常退出")
                    continue
            else:
                print(f"口令错误，{username}登录失败")
                log_message(username, "口令错误", client_addr[0])
                # 口令错误，登录失败
                client_socket.send("wrong".encode("utf-8"))
        else:
            # 如果用户首次注册
            init_log(username)
            log_message(username, "首次注册", client_addr[0])
            client_socket.send('0'.encode("utf-8"))
            init_talk(client_socket)
