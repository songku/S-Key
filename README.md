# S-Key

协商的应该是对N进行协商。服务器端只保存hash值。

单独一个用户名拼接seed后哈希，得到结果是不安全的。

当用户刚好使用完全部口令字时，需要重新初始化时，此时，攻击者单独知道用户名但即可模仿原用户进行登录，并获得全部口令字。

所以，应当是输入用户名和密码，输入的密码和seed进行拼接并得到哈希结果。

我现在想做一个客户端用来登录。但是由于涉及到要用S/key协议来实现登录，所以登录时不是采用简单的客户端和数据库交互，而是在一开始用户输入账号和密码点击登录按钮后，服务端这边会接收到客户端发送来的用户账号，然后调用数据库原先保存的该账号对应的IC（int）和seed（string）在发送给客户端。客户端在接收到这两个信息后，把原先输入的密码和IC以及seed进行散列运算，在发送给服务端，服务端最后进行一次处理与数据库保存的散列值进行比对，当通过后，会给客户端发送一个确认信息，登录认证成功！''

发送seed时索引错误。KeyError: 'songku'。

原因是往字典中添加记录必须要添加完整的记录。不能单独赋值。 解决办法：将seed值，作为全局变量，等待完整一条用户记录插入数据库。
