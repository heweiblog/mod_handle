# 1 DNS配置

## 1.1 dnssec

### 1.1.1 功能开关

+ URL

  | URL                                             | 描述 |
  | ----------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/api/v1.0/internal/configs |      |

+ 方法

  | 请求方法            | 请求数据 |
  | ------------------- | -------- |
  | GET/PUT/POST/DELETE | 参考举例 |

+ bt/sbt字段定义

  | 名称 | value  |
  | ---- | ------ |
  | bt   | dnssec |
  | sbt  | switch |

+ data字段定义

  | 名称   | 类型   | 默认值  | 描述                            |
  | ------ | ------ | ------- | ------------------------------- |
  | switch | String | disable | 功能开关，值为：enable或disable |

+ 举例

  ```python
  URL：http://192.168.5.41:9999/api/v1.0/internal/configs        
  METHOD:PUT/POST/DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":1,
              "service":"dns",
              "bt":"dnssec",
              "sbt":"switch",
              "op":"update",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  delete不执行任何动作
  put/post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/api/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "service":"dns",
              "bt":"dnssec",
              "sbt":"switch",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  {
  	"switch":"enable"
  }
  ```



### 2.1 递归最大并发数

+ URL

  | URL                                             | 描述 |
  | ----------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/api/v1.0/internal/configs |      |

+ 方法

  | 请求方法            | 请求数据 |
  | ------------------- | -------- |
  | GET/PUT/POST/DELETE | 参考举例 |

+ bt/sbt字段定义

  | 名称 | value        |
  | ---- | ------------ |
  | bt   | concurrent   |
  | sbt  | rules        |

+ data字段定义

  | 名称 | 类型 | 默认值 | 描述               |
  | ---- | ---- | ------ | ------------------ |
  | max  | Int  | 无     | 0 < v < 0xffffffff |

+ 举例

  ```python
  URL：http://192.168.5.41:9999/api/v1.0/internal/configs        
  METHOD:PUT/POST/DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":1,
              "service":"dns",
              "bt":"concurrent",
              "sbt":"rules",
              "op":"update",
              "data":{
                  "max":1000
              }
          }
      ]
  }
  delete不执行任何动作
  put/post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/api/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "service":"dns",
              "bt":"concurrent",
              "sbt":"rules",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  {
  	"max":1000
  }
  ```


