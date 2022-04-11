import socket
import hashlib

host = socket.gethostname()
port = 6666


# 将字符串转换为对应的16进制,这样才能进行异或运算
def str2hex(s):
    return int(s, 16)


def md5(string):
    md5_var = hashlib.md5()
    md5_var.update(string.encode("utf-8"))
    return md5_var.hexdigest()


def pre_process(secretpass, seed):
    md5_digest = md5(secretpass + seed)
    left_part = str2hex(md5_digest[:16])
    right_part = str2hex(md5_digest[16:])
    S = left_part ^ right_part
    return hex(S)  # 返回16进制字符才能进一步被


def init():  # 初始化函数，主要完成初始化口令和协商N的值的任务
    while True:
        secretpass = input("请输入SecretPASS(长度大于8字符)")
        if len(secretpass) > 8:
            break
    print("接收服务器发来的明文种子")
    recv_seed = client_socket.recv(8).decode("utf-8")
    S = pre_process(secretpass, recv_seed)
    while True:
        N = input("请输入协商的N的值(一个整数):")
        if not N.isdigit():
            print("请重新输入一个整数")
        elif int(N) <= 1:
            print("请重新输入一个整数")
        else:
            judge = input(f"请确认协商的N的值为{N},yes/no:")
            if "y" in judge.lower():
                break
    generate_keys(client_socket, S, int(N))
    exit(0)


def generate_keys(client_socket, S, N):
    key_list = []
    for i in range(N):
        S_new = md5(S)
        key_list.append(S_new)
        S = S_new
    key_list.reverse()  # 口令反转
    # print("向服务器发送协商的N的值")
    # client_socket.send(N.encode("utf-8"))
    print("向服务器发送初始口令")
    client_socket.send(key_list[0].encode("utf-8"))
    for i in range(1, N):
        print(f"请顺序使用第{i}个口令{key_list[i]}")


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))  # 尝试进行网络连接
    except Exception as e:
        print(e)
        exit(0)
    username = input("请输入用户名:")
    client_socket.send(username.encode("utf-8"))
    flag = client_socket.recv(1).decode("utf-8")
    if flag == '0':
        # 首次注册
        init()
    if flag == '1':
        # 登录验证
        password = input("请输入口令:")
        client_socket.send(password.encode("utf-8"))
        status = client_socket.recv(5).decode("utf-8")
        if status == "right":
            print("口令正确，登录成功")
            choice = input("避免口令用完，请确认是否需要重新协商口令(yes/no):")
            if "y" in choice.lower():
                client_socket.send("1".encode("utf-8"))
                init()
            elif "n" in choice.lower():
                client_socket.send("0".encode("utf-8"))
                exit(0)
        else:
            print("口令错误，程序退出")
            exit(1)
