# 安装部署
## docker部署
```shell script
docker pull 88382078/ips_process_web:test

docker run -it --rm -p 80:80 88382078/ips_process_web:test
```
## 本地安装
```shell script
git clone https://github.com/yubowen0525/maltrail-master.git
cd maltrail-master
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python3 wsgi.py
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