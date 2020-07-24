# 安装
```shell script
docker push 88382078/ips_process_web:test

docker run -it --rm -p 80:80 88382078/ips_process_web:test
```

# api
```shell script
curl http://0.0.0.0:80/getpacket 

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