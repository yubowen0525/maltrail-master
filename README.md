# 安装部署
## 打上patch
```shell script
# 安装dpkt
pip install dpkt
# 打patch
将./patch/pcap.py 文件替换 dpkt 项目里的 pcap.py文件
```

## 本地Server安装启动
```shell script
git clone https://github.com/yubowen0525/maltrail-master.git
cd maltrail-master
pip install -r requirements -i https://pypi.tuna.tsinghua.edu.cn/simple
sh start.sh
```


# api
```shell script
curl http://127.0.0.1:80/getpacket 

```

# 接口信息
```json
{
    "config":{
        "type":"np"
    },
    "sec": 1595602830,
    "usec": 54325,
    "ip_offset": 20,
    "packet":"------------------"
}
```

# 需要解决的问题
## sensor name
目前的sensor应该怎么样去获取名字呢？注册服务？管理sensor。可以使用mysql