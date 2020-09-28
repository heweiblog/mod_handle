# 1 系统管理

+ URL

  | URL                                            | 描述 |
  | ---------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/api/v1.0/internal/manage |      |

+ 方法

  | 请求方法 | 请求数据 |
  | -------- | -------- |
  | POST     | 参考举例 |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                                                  |
  | ------ | ------ | ------ | ----------------------------------------------------- |
  | module | String | 无     | 模块名称 proxy/xforward/recursion                     |
  | delay  | Int    | 无     | 秒数，表示在多少秒后执行，0即立刻执行                 |
  | action | String | 无     | 执行动作  stop停止服务/restart重启/exit结束/reset复位 |

+ 举例

  ```python
  URL：http://192.168.5.41:9999/api/v1.0/internal/manage       
  METHOD:POST
  BODY:
  {
      "module":"proxy",
      "delay":60,
      "action":"restart"
  }
  
  post返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  ```



