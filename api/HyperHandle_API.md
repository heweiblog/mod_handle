接口规范

## 1.1. 约束

+ 不用大写
+ 使用"-"，不使用"_"
+ `...`: 一个或多个
+ `*`: 跟在参数后面，表示必选
+ `N/A`: 描述参数时，表示不具备默认值
+ key是数据修改的依据，同一key下只有一条数据。

## 1.2. URL规则

+ 格式：http(s)://ip:port/api/应用/版本[/模块...]/资源
+ 面向资源，网络上的任何内容都是资源，尽量不要出现动词，动作交给`method`
+ 加上`api`是为了区分服务，同一个ip、port上可能有其他的http(s)服务
+ 加上版本号是方便程序在不断迭代中方便区分与兼容
+ 路径定义后最好足够的直观，资源表现清晰
+ 命名中如果需要，使用`-`，而不是驼峰式

## 1.3. HTTP方法

- 增删改查使用：

| 方法   | 描述                                                   |
| ------ | ------------------------------------------------------ |
| GET    | 从服务器上获取一项或多项资源                           |
| POST   | 在服务器上新建一个资源                                 |
| PUT    | 在服务器上更新资源，表示覆盖(没有老数据同时传递过来时) |
| DELETE | 从服务器上删除一项或多项资源                           |

## 1.4. 配置接口

### 1.4.1. 配置下发接口

+ 格式：{"contents":[{"source":"ms/cli","id":100,"bt":"xxx","sbt":"xxx","op":"add/delete/update/query/clear","data":{$DATA}}]}

| 名称     | 类型   | 默认值 | 描述                                                         |
| -------- | ------ | ------ | ------------------------------------------------------------ |
| contents | Array  | N/A    | 配置接口的内容数据                                           |
| source   | String | N/A    | 配置数据来源。"ms":来自网管；"cli":来自CLI                   |
| id       | Int    | 0      | 配置数据版本号。由配置客户端填写，当前配置数据来自网管的时候，该字段有意义。 |
| bt       | String | N/A    | 业务类型，接口数据通过"bt"和"sbt"区分是哪种策略              |
| sbt      | String | N/A    | 子业务类型                                                   |
| op       | String | N/A    | 操作码，添加/删除/更新/请求/清空                             |
| data     | Object | N/A    | 配置接口的具体数据，不同的"bt"/"sbt"，定义不同的data格式     |

### 1.4.2. 配置接口返回数据

- 返回参数如下：

| 名称        | 类型                 | 默认值 | 描述                                          |
| ----------- | -------------------- | ------ | --------------------------------------------- |
| rcode       | Int                  | N/A    | 业务执行代码                                  |
| description | String               | N/A    | rcode的文字描述                               |
| data        | String/Bool/Array... | N      | 失败时一定没有 成功时可以根据语义选择是否携带 |

- 删除一条不存在的记录也算作成功
- 添加重复的记录也算作成功

## 1.5. 任务接口

如下配置属于任务类配置，不需要EMS保持配置一致性。

+ 缓存备份
+ 缓存导入
+ 缓存查询
+ 缓存删除

URL格式：http(s)://$HOST:$PORT/handle/v1.0/internal/tasks

### 1.5.1. 任务添加接口

+ 任务添加：

| op   | 方法 | 描述     |
| ---- | ---- | -------- |
| add  | POST | 添加任务 |

+ 格式：{"contents":[{"source":"ms","tasktype":"$TYPE","data":{$DATA}}]}

| 名称     | 类型   | 默认值 | 描述                                         |
| -------- | ------ | ------ | -------------------------------------------- |
| contents | Array  | N/A    | 任务接口的内容数据                           |
| source   | String | N/A    | 配置数据来源。"ms":来自网管；"cli":来自CLI   |
| tasktype | String | N/A    | 任务类型                                   |
| data     | Object | N/A    | 具体任务数据。不同的任务类型，数据格式不同。 |

### 1.5.2. 任务添加接口返回数据

- 返回参数如下：

| 名称        | 类型   | 默认值 | 描述                                              |
| ----------- | ------ | ------ | ------------------------------------------------- |
| rcode       | Int    | N/A    | 业务执行代码                                      |
| description | String | N/A    | rcode的文字描述                                   |
| taskid      | Int    | N/A    | 该任务ID。后续可调用API接口通过taskid查询任务状态 |

### 1.5.3. 任务查询接口

+ 任务查询：

| op    | 方法 | URL                                                     | 描述               |
| ----- | ---- | ------------------------------------------------------- | ------------------ |
| query | GET  | http://$HOST:$PORT/handle/v1.0/internal/tasks?taskid=XX | 根据taskid查询任务 |

- 格式：

| 名称        | 类型   | 默认值 | 描述                                              |
| ----------- | ------ | ------ | ------------------------------------------------- |
| rcode       | Int    | N/A    | 业务执行代码                                      |
| description | String | N/A    | rcode的文字描述                                   |
| taskid      | Int    | N/A    | 该任务ID。后续可调用API接口通过taskid查询任务状态 |

### 1.5.4. 任务查询接口返回数据

+ 格式：

| 名称        | 类型   | 默认值 | 描述                                               |
| ----------- | ------ | ------ | -------------------------------------------------- |
| rcode       | Int    | N/A    | 业务执行代码                                       |
| description | String | N/A    | rcode的文字描述                                    |
| taskid      | Int    | N/A    | 该任务ID。后续可调用API接口通过taskid查询任务状态  |
| tasktype    | String | N/A    | 任务类型                                           |
| status      | String | N/A    | 任务状态。executing/complete/error                 |
| starttime   | String | N/A    | 任务执行起始时间                                   |
| endtime     | String | N/A    | 任务执行结束时间                                   |
| result      | Array  | N/A    | 任务返回的具体结果。不同的tasktype，数据格式不同。 |

# 2. Handle安全子系统

## 2.1. ACL

### 2.1.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据 |
  | -------- | -------- |
  | GET/PUT  | 参考举例 |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | useripwhitelist |
  | sbt  | switch          |

+ data字段定义

  | 名称   | 类型   | 默认值  | 描述                            |
  | ------ | ------ | ------- | ------------------------------- |
  | switch | String | disable | 功能开关，值为：enable或disable |

+ 举例

  ```python
  URL：http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:PUT
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
              "sbt":"switch",
              "op":"update",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  put返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
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


### 2.1.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据 |
  | --------------- | -------- |
  | GET/DELETE/POST | 参考举例 |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | useripwhitelist |
  | sbt  | rules           |

+ data字段定义

  | 名称    | 类型   | 默认值 | 描述             |
  | ------- | ------ | ------ | ---------------- |
  | ipgroup | String | N/A    | ip组名           |
  | ip      | String | N/A    | ipv4或ipv6地址段 |

+ 接口数据举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "ipgroup":"shcmcc",
                  "ip":"192.168.6.0/24"
              }
          }
      ]
  }
  post返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
              "sbt":"rules",
              "op":"delete",
              "data":{
                  "ipgroup":"shcmcc",
                  "ip":"192.168.6.0/24"
              }
          }
      ]
  }
  delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
              "sbt":"rules",
              "op":"clear",
              "data":{}
          }
      ]
  }
  delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"useripwhitelist",
              "sbt":"rules",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  [{"ipgroup":"shcmcc","ip":"192.168.6.0/24"}]
  ```


## 2.2. 源IP限速

### 2.2.1. 功能开关
+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法
    | 请求方法 | 请求数据  |
    | -------- | --------- |
    | GET/PUT  | 参考2.1.1 |
    
+ bt/sbt字段定义

    | 名称 | value       |
    | ---- | ----------- |
    | bt   | ipthreshold |
    | sbt  | switch      |



### 2.2.2. 策略

+ URL

    | URL                                                | 描述 |
    | -------------------------------------------------- | ---- |
    | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

    | 请求方法            | 请求数据 | key  |
    | ------------------- | -------- | ---- |
    | GET/POST/PUT/DELETE | 参考举例 | ip   |

+ bt/sbt字段定义

    | 名称 | value       |
    | ---- | ----------- |
    | bt   | ipthreshold |
    | sbt  | rules       |

+ data字段定义

    | 名称  | 类型   | 默认值 | 描述             |
    | ----- | ------ | ------ | ---------------- |
    | ip    | String | N/A    | ipv4或ipv6地址段 |
    | meter | Int    | N/A    | 限速阈值         |
    
+ 举例

    ```python
    URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
    METHOD:POST
    BODY:
    {
        "contents":[
            {
                "source":"ms",
                "id":100,
                "bt":"ipthreshold",
                "sbt":"rules",
                "op":"add",
                "data":{
                    "ip":"192.168.6.0/24",
                    "meter":100
                }
            }
        ]
    }
    
    URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
    METHOD:PUT
    BODY:
    {
        "contents":[
            {
                "source":"ms",
                "id":100,
                "bt":"ipthreshold",
                "sbt":"rules",
                "op":"update",
                "data":{
                    "ip":"192.168.6.0/24",
                    "meter":200
                }
            }
        ]
    }
    
    URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
    METHOD:DELETE
    BODY:
    {
        "contents":[
            {
                "source":"ms",
                "id":100,
                "bt":"ipthreshold",
                "sbt":"rules",
                "op":"delete",
                "data":{
                    "ip":"192.168.6.0/24",
                    "meter":200
                }
            }
        ]
    }
    
    URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
    METHOD:DELETE
    BODY:
    {
        "contents":[
            {
                "source":"ms",
                "id":100,
                "bt":"ipthreshold",
                "sbt":"rules",
                "op":"clear",
                "data":{}
            }
        ]
    }
    
    post/put/delete返回:
    {
    	"rcode":0,
    	"description":"recevied"
    }
    
    
    URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
    METHOD:GET
    BODY:
    {
        "contents":[
            {
                "source":"ms",
                "id":100,
                "bt":"ipthreshold",
                "sbt":"rules",
                "op":"query",
                "data":{}
            }
        ]
    }
    get返回:
    [{"ip":"192.168.6.0/24","meter":200}]
    ```


## 2.3. 标识限速

### 2.3.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | handlethreshold |
  | sbt  | switch          |


### 2.3.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法            | 请求数据      | key    |
  | ------------------- | ------------- | ------ |
  | GET/POST/PUT/DELETE | 参考2.2.2举例 | handle |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | handlethreshold |
  | sbt  | rules           |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述       |
  | ------ | ------ | ------ | ---------- |
  | handle | String | N/A    | handle标识 |
  | meter  | Int    | N/A    | 限速阈值   |

+ 接口数据举例

  ```python
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"handlethreshold",
              "sbt":"rules",
              "op":"add/update/delete/clear/query",
              "data":{
                  "handle":"ncstrl.vatech_cs/tr-93-35",
                  "meter":100
              }
          }
      ]
  }
  ```
  

## 2.4. 源IP黑名单

### 2.4.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value              |
  | ---- | ------------------ |
  | bt   | srcipaccesscontrol |
  | sbt  | switch             |

### 2.4.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据     |
  | --------------- | ------------ |
  | GET/DELETE/POST | 参考下列举例 |

+ bt/sbt字段定义

  | 名称 | value              |
  | ---- | ------------------ |
  | bt   | srcipaccesscontrol |
  | sbt  | rules              |

+ data字段定义

  | 名称 | 类型   | 默认值 | 描述             |
  | ---- | ------ | ------ | ---------------- |
  | ip   | String | N/A    | ipv4或ipv6地址段 |
  
+ 举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"srcipaccesscontrol",
              "sbt":"rules",
              "op":"add",
              "data":{
              	"ip":"fe80::ae1f:6bff:fe6d:71d4/64"
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"srcipaccesscontrol",
              "sbt":"rules",
              "op":"delete",
              "data":{
              	"ip":"fe80::ae1f:6bff:fe6d:71d4/64"
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"srcipaccesscontrol",
              "sbt":"rules",
              "op":"clear",
              "data":{}
          }
      ]
  }
  
  post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"srcipaccesscontrol",
              "sbt":"rules",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  [{"ip":"fe80::ae1f:6bff:fe6d:71d4/64"},{"ip":"1.1.1.0/24"}]
  ```


## 2.5. 标识黑名单

### 2.5.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value               |
  | ---- | ------------------- |
  | bt   | handleaccesscontrol |
  | sbt  | switch              |


### 2.5.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据     |
  | --------------- | ------------ |
  | GET/DELETE/POST | 参考下列举例 |

+ bt/sbt字段定义

  | 名称 | value               |
  | ---- | ------------------- |
  | bt   | handleaccesscontrol |
  | sbt  | rules               |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述       |
  | ------ | ------ | ------ | ---------- |
  | handle | String | N/A    | handle标识 |
  
+ 举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"handleaccesscontrol",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech_cs/tr-93-35",
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"handleaccesscontrol",
              "sbt":"rules",
              "op":"delete",
              "data":{
                  "handle":"ncstrl.vatech_cs/*",
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"handleaccesscontrol",
              "sbt":"rules",
              "op":"clear",
              "data":{}
          }
      ]
  }
  
  post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"handleaccesscontrol",
              "sbt":"rules",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  [{"handle":"ncstrl.vatech_cs/tr-93-35"},{"handle":"ncstrl.vatech_cs/*"}]
  ```


# 3. 递归转发

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据     |
  | --------------- | ------------ |
  | GET/DELETE/POST | 参考下列举例 |

+ bt/sbt字段定义

  | 名称 | value         |
  | ---- | ------------- |
  | bt   | backend       |
  | sbt  | forwardserver |

+ data字段定义

  | 名称  | 类型   | 默认值 | 描述                    |
  | ----- | ------ | ------ | ----------------------- |
  | group | String | N/A    | 转发服务器组            |
  | ip    | String | N/A    | 转发服务器IPV4/IPV6地址 |
  | proto | String | N/A    | 转发服务器服务协议      |
  | port  | Int    | N/A    | 转发服务器服务端口      |

+ 接口数据举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backend",
              "sbt":"forwardserver",
              "op":"add",
              "data":{
                  "group":"group1",
                  "ip":"192.168.6.100",
                  "proto":"udp",
                  "port":2641
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backend",
              "sbt":"forwardserver",
              "op":"delete",
              "data":{
                  "group":"group1",
                  "ip":"192.168.6.101",
                  "proto":"udp",
                  "port":2641
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backend",
              "sbt":"forwardserver",
              "op":"clear",
              "data":{}
          }
      ]
  }
  
  post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backend",
              "sbt":"forwardserver",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  [{"group":"group1","ip":"192.168.6.101","proto":"udp","port":2641}]
  ```
  
  
  

# 4. 系统管理

## 4.1. Handle服务管理

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+  方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | businessservice |
  | sbt  | switch          |
  

## 4.2. Handle协议管理

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+  方法

  | 请求方法        | 请求数据     |
  | --------------- | ------------ |
  | GET/DELETE/POST | 参考下列举例 |

+ bt/sbt字段定义

  | 名称 | value         |
  | ---- | ------------- |
  | bt   | businessproto |
  | sbt  | rules         |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                              |
  | ------ | ------ | ------ | --------------------------------- |
  | proto  | String | N/A    | 协议，例如：tcp、udp、http、https |
  | action | String | N/A    | 执行动作，enable/disable          |
  | port   | Int    | N/A    | 端口                              |
  | ipv4   | List   | N/A    | ipv4业务ip地址数组                |
  | ipv6   | List   | N/A    | ipv4业务ip地址数组                |

+ 举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"businessproto",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "proto":"tcp",
                  "action":"disable",
                  "port":2641,
                  "ipv4":["192.168.6.100","192.168.6.101"],
                  "ipv6":[]
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"businessproto",
              "sbt":"rules",
              "op":"delete",
              "data":{
                  "proto":"tcp",
                  "action":"disable",
                  "port":2641,
                  "ipv4":["192.168.6.100","192.168.6.101"],
                  "ipv6":[]
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"businessproto",
              "sbt":"rules",
              "op":"clear",
              "data":{}
          }
      ]
  }
  
  post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"businessproto",
              "sbt":"rules",
              "op":"query",
              "data":{}
          }
      ]
  }
  get返回:
  [{"proto":"tcp","action":"disable","port":2641,"ipv4":["192.168.6.100","192.168.6.101"],"ipv6":[]}]
  ```


## 4.3. DNS服务管理

+ URL

  | URL                                             | 描述 |
  | ----------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/dns/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value           |
  | ---- | --------------- |
  | bt   | businessservice |
  | sbt  | switch          |

## 4.4. DNS协议管理

+ URL

  | URL                                             | 描述 |
  | ----------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/dns/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据    |
  | --------------- | ----------- |
  | GET/DELETE/POST | 参考4.2举例 |

+ bt/sbt字段定义

  | 名称 | value         |
  | ---- | ------------- |
  | bt   | businessproto |
  | sbt  | rules         |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                     |
  | ------ | ------ | ------ | ------------------------ |
  | proto  | String | N/A    | 协议，例如：tcp、udp     |
  | action | String | N/A    | 执行动作，enable/disable |
  | port   | Int    | N/A    | 端口                     |
  | ipv4   | List   | N/A    | ipv4业务ip地址数组       |
  | ipv6   | List   | N/A    | ipv6业务ip地址数组       |


## 4.5. CA证书管理

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法        | 请求数据     |
  | --------------- | ------------ |
  | GET/DELETE/POST | 参考以下举例 |

+ bt/sbt字段定义

  | 名称 | value       |
  | ---- | ----------- |
  | bt   | certificate |
  | sbt  | rules       |

+ data字段定义

  | 名称    | 类型   | 默认值 | 描述                 |
  | ------- | ------ | ------ | -------------------- |
  | ca_cert | String | N/A    | 证书信息，BASE64转码 |
  | rsa_key | String | N/A    | 私钥，BASE64转码     |
  
+ 举例

  ```python
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:POST
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"certificate",
              "sbt":"rules",
              "op":"add",
              "data":{				"ca_cert":"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNUekNDQWJnQ0NRRFpNM2l2ZWd2YnVEQU5CZ2txaGtpRzl3MEJBUVVGQURCck1Rc3dDUVlEVlFRR0V3SkQKVGpFUk1BOEdBMVVFQ0F3SVUyaGhibWRvWVdreEVUQZ05WQkFjTUNGTm9ZVzVuYUdGcE1SRXdEd1lEVlFRSwpEQWhaWVcxMVZHVmphREVNTUFvR0ExVUVDd3dEUkUxVE1SVXdFd1lEVlFRRERBeGtiWE11ZVdGdGRTNWpiMjB3CklCY05NVGt4TURFeU1EWTBOalE1V2hnUE1qRXhPVEE1TVRnd05qUTJORGxhTUdzeEN6QUpCZ05WQkFZVEFrTk8KTVJFd0R3WURWUVFJREFoVGFHRnVaMmhoYVRFUk1BOEdBMVVFQnd3SVUyaGhibWRvWVdreEVUQVBCZ05WQkFvTQpDRmxoYlhWVVpXTm9NUXd3Q2dZRFZRUUxEQU5FVFZNeEZUQVRCZ05WQkFNTURHUnRjeTU1WVcxMUxtTnZiVENCCm56QU5CZ2txaGtpRzl3MEJBUUVGQUFPQmpRQXdnWWtDZ1lFQXVxckhJcWtYYTR1Ylo5Q0lxaVVwVEZFTExSSTYKS2V4eTdpMDJHK1R3VVlaNGlvSXl2RUtrTi9raTZhRVBoanhnb0szNk8wQnZjNVNoVitsNmg5MHU0VWo4Y2hkZwo2dy9EbmI4MHYwRlc0T3h1cWFRU0w5RjVrN2RLZjJjS3liSWtiSlR0S3RYUW5NRlR2T0dzZU5WRzN3QktsRmV4CnFLblZuSENURU5Ocnp4MENBd0VBQVRBTkJna3Foa2lHOXcwQkFRVUZBQU9CZ1FDWVA2c1R2RkpLUjNhZXVmZ2wKQlZEa3VMK1dnbENJWWQrZjRGWXlicU9JL0ZJaGxxTVo1SWtkY0gydHJJaHFRVWdWYmFOd1J1WmUvVHlxVG5mUgpOdzFVK1NpNUVlQkNKVzBmcUNXdXFmQlpVLzB5Nkt0c3N0M1NtaE9kWU11SW83OXp3SGR0NU1nd3BMcDkzS3JGCnA4dFFvZUxRelhxdGcrVUxVQ3ZJU3A5UVpBPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",		"rsa_key":"LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWEFJQkFBS0JnUUM2cXNjaXFSZHJpNXRuMElpcUpTbE1VUXN0RWpvcDdITHVMVFliNVBCUmhuaUtnaks4ClFxUTMrU0xwb1ErR1BHQ2dyZm83UUc5emxLRlg2WHFIM1M3aFNQeHlGMkRyRDhPZHZ6Uy9RVmJnN0c2cHBCSXYKMFhtVHQwcC9ad3JKc2lSc2xPMHExZENjd1ZPODRheDQxVWJmQUVxVVY3R29xZFdjY0pNUTAydlBIUUlEQVFBQgpBb0dCQUpMR001eGFUcEwraSt4K09PZG9IdWZtRlo2VDVXNFBnSE1zMDQzdFh0VUxvZjV1ejR2ZDdwZ2dha1kvCm9TQlFtejNjYnBSbVh2d0hrekczNE9PeGsraXYvVE5lY1hFWTVrZDhnTzhJUjVYVGxLc1RZek55RTkycHZtSjYKSi9yMkp3QWxza2ZxUklwUFAxSmcrUThKcmw2dFhCTEtsN09KaERLMUJJV0RRVzFoQWtFQTkyWEdPZGNiRHhNRgozVGtVTTJmQ1JBK0pwRHVvai9lRjJqTDZ3cFFyR1IrSTBLd05DaXRoQ0NkdlRnY0p6WDhQMzB5UkZtWDZHOWdZCnkxSFZzQ2hTbFFKQkFNRW9hRXREMFR1b0h3S2YvUHFPWmtZZFJIa3BpdUdOUTFNeGNILzhwSHFpdmlMcms0cWkKS2sxUk1rYlp1d2FBY1pSN1cwd3NQOWxvdHcvaVl2Sk9NR2tDUUJrcjFidFUwMy81STRPYXB4K0QweFF4c0lOeApQbmxIYWVzRmZOWUhWVXM5RmlLRkh0NkdBMTFkQmNvZWxUUy9WTklYYkR1bkxJZGd1VVVXa25OVjV2RUNRQjhlCklWOHV0OENDbnl4UEZmUlBpSTUzSEpiZ2FHMVowcVRPYkM5U1JqVXpqcW9WaFpscDhxS3VHQWx0L2tGWDQvUmwKd3htTWIyVFpCOVRaUmROL1lURUNRRVBsYVhtamNJcnppV3EwN0ZXd21teWovNVhlTURlK2s1QWd4KytqNmw4bAozQjZaQWUzY2RENVpoTXA0cGxjM25PUjFHSXIxdWlwV0JNRk1VNDNOZ1VzPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo="
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"certificate",
              "sbt":"rules",
              "op":"delete",
              "data":{				"ca_cert":"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNUekNDQWJnQ0NRRFpNM2l2ZWd2YnVEQU5CZ2txaGtpRzl3MEJBUVVGQURCck1Rc3dDUVlEVlFRR0V3SkQKVGpFUk1BOEdBMVVFQ0F3SVUyaGhibWRvWVdreEVUQZ05WQkFjTUNGTm9ZVzVuYUdGcE1SRXdEd1lEVlFRSwpEQWhaWVcxMVZHVmphREVNTUFvR0ExVUVDd3dEUkUxVE1SVXdFd1lEVlFRRERBeGtiWE11ZVdGdGRTNWpiMjB3CklCY05NVGt4TURFeU1EWTBOalE1V2hnUE1qRXhPVEE1TVRnd05qUTJORGxhTUdzeEN6QUpCZ05WQkFZVEFrTk8KTVJFd0R3WURWUVFJREFoVGFHRnVaMmhoYVRFUk1BOEdBMVVFQnd3SVUyaGhibWRvWVdreEVUQVBCZ05WQkFvTQpDRmxoYlhWVVpXTm9NUXd3Q2dZRFZRUUxEQU5FVFZNeEZUQVRCZ05WQkFNTURHUnRjeTU1WVcxMUxtTnZiVENCCm56QU5CZ2txaGtpRzl3MEJBUUVGQUFPQmpRQXdnWWtDZ1lFQXVxckhJcWtYYTR1Ylo5Q0lxaVVwVEZFTExSSTYKS2V4eTdpMDJHK1R3VVlaNGlvSXl2RUtrTi9raTZhRVBoanhnb0szNk8wQnZjNVNoVitsNmg5MHU0VWo4Y2hkZwo2dy9EbmI4MHYwRlc0T3h1cWFRU0w5RjVrN2RLZjJjS3liSWtiSlR0S3RYUW5NRlR2T0dzZU5WRzN3QktsRmV4CnFLblZuSENURU5Ocnp4MENBd0VBQVRBTkJna3Foa2lHOXcwQkFRVUZBQU9CZ1FDWVA2c1R2RkpLUjNhZXVmZ2wKQlZEa3VMK1dnbENJWWQrZjRGWXlicU9JL0ZJaGxxTVo1SWtkY0gydHJJaHFRVWdWYmFOd1J1WmUvVHlxVG5mUgpOdzFVK1NpNUVlQkNKVzBmcUNXdXFmQlpVLzB5Nkt0c3N0M1NtaE9kWU11SW83OXp3SGR0NU1nd3BMcDkzS3JGCnA4dFFvZUxRelhxdGcrVUxVQ3ZJU3A5UVpBPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",		"rsa_key":"LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWEFJQkFBS0JnUUM2cXNjaXFSZHJpNXRuMElpcUpTbE1VUXN0RWpvcDdITHVMVFliNVBCUmhuaUtnaks4ClFxUTMrU0xwb1ErR1BHQ2dyZm83UUc5emxLRlg2WHFIM1M3aFNQeHlGMkRyRDhPZHZ6Uy9RVmJnN0c2cHBCSXYKMFhtVHQwcC9ad3JKc2lSc2xPMHExZENjd1ZPODRheDQxVWJmQUVxVVY3R29xZFdjY0pNUTAydlBIUUlEQVFBQgpBb0dCQUpMR001eGFUcEwraSt4K09PZG9IdWZtRlo2VDVXNFBnSE1zMDQzdFh0VUxvZjV1ejR2ZDdwZ2dha1kvCm9TQlFtejNjYnBSbVh2d0hrekczNE9PeGsraXYvVE5lY1hFWTVrZDhnTzhJUjVYVGxLc1RZek55RTkycHZtSjYKSi9yMkp3QWxza2ZxUklwUFAxSmcrUThKcmw2dFhCTEtsN09KaERLMUJJV0RRVzFoQWtFQTkyWEdPZGNiRHhNRgozVGtVTTJmQ1JBK0pwRHVvai9lRjJqTDZ3cFFyR1IrSTBLd05DaXRoQ0NkdlRnY0p6WDhQMzB5UkZtWDZHOWdZCnkxSFZzQ2hTbFFKQkFNRW9hRXREMFR1b0h3S2YvUHFPWmtZZFJIa3BpdUdOUTFNeGNILzhwSHFpdmlMcms0cWkKS2sxUk1rYlp1d2FBY1pSN1cwd3NQOWxvdHcvaVl2Sk9NR2tDUUJrcjFidFUwMy81STRPYXB4K0QweFF4c0lOeApQbmxIYWVzRmZOWUhWVXM5RmlLRkh0NkdBMTFkQmNvZWxUUy9WTklYYkR1bkxJZGd1VVVXa25OVjV2RUNRQjhlCklWOHV0OENDbnl4UEZmUlBpSTUzSEpiZ2FHMVowcVRPYkM5U1JqVXpqcW9WaFpscDhxS3VHQWx0L2tGWDQvUmwKd3htTWIyVFpCOVRaUmROL1lURUNRRVBsYVhtamNJcnppV3EwN0ZXd21teWovNVhlTURlK2s1QWd4KytqNmw4bAozQjZaQWUzY2RENVpoTXA0cGxjM25PUjFHSXIxdWlwV0JNRk1VNDNOZ1VzPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo="
              }
          }
      ]
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:DELETE
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"certificate",
              "sbt":"rules",
              "op":"clear",
              "data":{}				
          }
      ]
  }
  
  post/delete返回:
  {
  	"rcode":0,
  	"description":"recevied"
  }
  
  URL:http://192.168.5.41:9999/handle/v1.0/internal/configs        
  METHOD:GET
  BODY:
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"certificate",
              "sbt":"rules",
              "op":"query",
              "data":{}				
          }
      ]
  } 
  get返回:
  [{				"ca_cert":"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNUekNDQWJnQ0NRRFpNM2l2ZWd2YnVEQU5CZ2txaGtpRzl3MEJBUVVGQURCck1Rc3dDUVlEVlFRR0V3SkQKVGpFUk1BOEdBMVVFQ0F3SVUyaGhibWRvWVdreEVUQZ05WQkFjTUNGTm9ZVzVuYUdGcE1SRXdEd1lEVlFRSwpEQWhaWVcxMVZHVmphREVNTUFvR0ExVUVDd3dEUkUxVE1SVXdFd1lEVlFRRERBeGtiWE11ZVdGdGRTNWpiMjB3CklCY05NVGt4TURFeU1EWTBOalE1V2hnUE1qRXhPVEE1TVRnd05qUTJORGxhTUdzeEN6QUpCZ05WQkFZVEFrTk8KTVJFd0R3WURWUVFJREFoVGFHRnVaMmhoYVRFUk1BOEdBMVVFQnd3SVUyaGhibWRvWVdreEVUQVBCZ05WQkFvTQpDRmxoYlhWVVpXTm9NUXd3Q2dZRFZRUUxEQU5FVFZNeEZUQVRCZ05WQkFNTURHUnRjeTU1WVcxMUxtTnZiVENCCm56QU5CZ2txaGtpRzl3MEJBUUVGQUFPQmpRQXdnWWtDZ1lFQXVxckhJcWtYYTR1Ylo5Q0lxaVVwVEZFTExSSTYKS2V4eTdpMDJHK1R3VVlaNGlvSXl2RUtrTi9raTZhRVBoanhnb0szNk8wQnZjNVNoVitsNmg5MHU0VWo4Y2hkZwo2dy9EbmI4MHYwRlc0T3h1cWFRU0w5RjVrN2RLZjJjS3liSWtiSlR0S3RYUW5NRlR2T0dzZU5WRzN3QktsRmV4CnFLblZuSENURU5Ocnp4MENBd0VBQVRBTkJna3Foa2lHOXcwQkFRVUZBQU9CZ1FDWVA2c1R2RkpLUjNhZXVmZ2wKQlZEa3VMK1dnbENJWWQrZjRGWXlicU9JL0ZJaGxxTVo1SWtkY0gydHJJaHFRVWdWYmFOd1J1WmUvVHlxVG5mUgpOdzFVK1NpNUVlQkNKVzBmcUNXdXFmQlpVLzB5Nkt0c3N0M1NtaE9kWU11SW83OXp3SGR0NU1nd3BMcDkzS3JGCnA4dFFvZUxRelhxdGcrVUxVQ3ZJU3A5UVpBPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",		"rsa_key":"LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWEFJQkFBS0JnUUM2cXNjaXFSZHJpNXRuMElpcUpTbE1VUXN0RWpvcDdITHVMVFliNVBCUmhuaUtnaks4ClFxUTMrU0xwb1ErR1BHQ2dyZm83UUc5emxLRlg2WHFIM1M3aFNQeHlGMkRyRDhPZHZ6Uy9RVmJnN0c2cHBCSXYKMFhtVHQwcC9ad3JKc2lSc2xPMHExZENjd1ZPODRheDQxVWJmQUVxVVY3R29xZFdjY0pNUTAydlBIUUlEQVFBQgpBb0dCQUpMR001eGFUcEwraSt4K09PZG9IdWZtRlo2VDVXNFBnSE1zMDQzdFh0VUxvZjV1ejR2ZDdwZ2dha1kvCm9TQlFtejNjYnBSbVh2d0hrekczNE9PeGsraXYvVE5lY1hFWTVrZDhnTzhJUjVYVGxLc1RZek55RTkycHZtSjYKSi9yMkp3QWxza2ZxUklwUFAxSmcrUThKcmw2dFhCTEtsN09KaERLMUJJV0RRVzFoQWtFQTkyWEdPZGNiRHhNRgozVGtVTTJmQ1JBK0pwRHVvai9lRjJqTDZ3cFFyR1IrSTBLd05DaXRoQ0NkdlRnY0p6WDhQMzB5UkZtWDZHOWdZCnkxSFZzQ2hTbFFKQkFNRW9hRXREMFR1b0h3S2YvUHFPWmtZZFJIa3BpdUdOUTFNeGNILzhwSHFpdmlMcms0cWkKS2sxUk1rYlp1d2FBY1pSN1cwd3NQOWxvdHcvaVl2Sk9NR2tDUUJrcjFidFUwMy81STRPYXB4K0QweFF4c0lOeApQbmxIYWVzRmZOWUhWVXM5RmlLRkh0NkdBMTFkQmNvZWxUUy9WTklYYkR1bkxJZGd1VVVXa25OVjV2RUNRQjhlCklWOHV0OENDbnl4UEZmUlBpSTUzSEpiZ2FHMVowcVRPYkM5U1JqVXpqcW9WaFpscDhxS3VHQWx0L2tGWDQvUmwKd3htTWIyVFpCOVRaUmROL1lURUNRRVBsYVhtamNJcnppV3EwN0ZXd21teWovNVhlTURlK2s1QWd4KytqNmw4bAozQjZaQWUzY2RENVpoTXA0cGxjM25PUjFHSXIxdWlwV0JNRk1VNDNOZ1VzPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo="
              }]
  ```


# 5. 缓存子系统

## 5.1. 强制解析

### 5.1.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法 | 请求数据  |
  | -------- | --------- |
  | GET/PUT  | 参考2.1.1 |

+ bt/sbt字段定义

  | 名称 | value  |
  | ---- | ------ |
  | bt   | xforce |
  | sbt  | switch |

### 5.1.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ 方法

  | 请求方法            | 请求数据     |
  | ------------------- | ------------ |
  | GET/PUT/POST/DELETE | 参考下列举例 |

+ bt/sbt字段定义

  | 名称 | value  |
  | ---- | ------ |
  | bt   | xforce |
  | sbt  | rules  |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                                         |
  | ------ | ------ | ------ | -------------------------------------------- |
  | handle | String | N/A    | handle标识                                   |
  | ttl    | Int    | N/A    | ttl，绝对时间                                |
  | index  | Int    | N/A    | handle index值                               |
  | type   | String | N/A    | handle type值                                |
  | data   | String | N/A    | handle value值，不同的type，data字段格式不同 |
  
+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"xforce",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech_cs/tr-93-35",
                  "ttl":86400,
                  "index":10,
                  "type":"url",
                  "data":"http://www.handle.net"
              }
          },
          {
              "source":"ms",
              "id":101,
              "bt":"xforce",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech_cs/*",
                  "ttl":86400,
                  "index":3,
                  "type":"hs_site",
                  "data":{
                  	"version":1,
                  	"protoversion":"2.10",
                  	"serialnum":2,
                  	"primarymask":192,
                  	"hashoption":2,
                  	"hashfilter":0,
                  	"attrlist":"doi oak",
                  	"serverlist":[
                  		{
                  			"serverid":1,
                  			"address":"38.100.138.133",
                  			"publickey":{
                  				"type":"HS_DSAKEY",
                  				"key":"iQCuR2R",
                  			},
                  			"serviceinterface":[
                  				{
                  					"type":3,
                  					"transproto":1,
                  					"port":2641,
                  				},
                  				{
                  					"type":2,
                  					"transproto":0,
                  					"port":2641,
                  				},
                  			],
                  		},
                  	],
                  },
              }
          }
      ]
  }
  ```

  

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

## 5.2. 缓存智能更新

### 5.2.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value            |
  | ---- | ---------------- |
  | bt   | cachesmartupdate |
  | sbt  | switch           |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                            |
  | ------ | ------ | ------ | ------------------------------- |
  | switch | String | enable | 功能开关，值为：enable或disable |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"cachesmartupdate",
              "sbt":"switch",
              "op":"add",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

## 5.3. 缓存预取

### 5.3.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value         |
  | ---- | ------------- |
  | bt   | cacheprefetch |
  | sbt  | switch        |

+ data字段定义

  | 名称   | 类型   | 默认值  | 描述                            |
  | ------ | ------ | ------- | ------------------------------- |
  | switch | String | disable | 功能开关，值为：enable或disable |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"cacheprefetch",
              "sbt":"switch",
              "op":"add",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

### 5.3.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value         |
  | ---- | ------------- |
  | bt   | cacheprefetch |
  | sbt  | rules         |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述       |
  | ------ | ------ | ------ | ---------- |
  | handle | String | N/A    | handle标识 |
  |        |        |        |            |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"cacheprefetch",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech_cs/tr-93-35",
              }
          },
          {
              "source":"ms",
              "id":101,
              "bt":"cacheprefetch",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech/*",
              }
          }
      ]
  }
  ```

  

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

## 5.4. 缓存备份

+ URL

  | URL                                              | 描述 |
  | ------------------------------------------------ | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/tasks |      |

+ data字段定义

  | 名称 | 类型   | 默认值 | 描述         |
  | ---- | ------ | ------ | ------------ |
  | file | String | N/A    | 备份的文件名 |
  |      |        |        |              |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "tasktype":"cachebackup",
              "data":{
                  "file":"202008072217123",
              }
          },
      ]
  }
  ```
  
  
  
+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied",
  	"taskid":1
  }
  ```

## 5.5. 缓存导入

+ URL

  | URL                                              | 描述 |
  | ------------------------------------------------ | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/tasks |      |

+ data字段定义

  | 名称 | 类型   | 默认值 | 描述         |
  | ---- | ------ | ------ | ------------ |
  | file | String | N/A    | 备份的文件名 |
  |      |        |        |              |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "tasktype":"cacheimport",
              "data":{
                  "file":"202008072217123",
              }
          },
      ]
  }
  ```

  

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied",
  	"taskid":2
  }
  ```



## 5.6. 缓存查询

+ URL

  | URL                                              | 描述 |
  | ------------------------------------------------ | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/tasks |      |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                                    |
  | ------ | ------ | ------ | --------------------------------------- |
  | handle | String | N/A    | handle标识                              |
  | index  | Array  | N/A    | handle index 列表。为空，则表示查询全部 |
  | type   | Array  | N/A    | handle type列表。为空，则表示查询全部   |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "tasktype":"cachequery",
              "data":{
              	"handle":"10.serv/crossref",
             	 	"index":[],
              	"type":[],
              }
          },
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied",
  	"taskid":2
  }
  ```

  

+ 缓存查询taskid返回值

  ```
  
  {
  	"rcode":0,
  	"description":"cache query successful",
  	"taskid":2,
      "tasktype":"cachequery",
      "status":"Complete",
      "startTime":"2020/06/22 09:51:10",
      "endTime":"2020/06/22 09:52:10"
  	"result":[
  		{
  		"handle": "10.serv/crossref",
  		"values": [
  			{
  			"index": 1,
  			"type": "EMAIL",
  			"data": {
  				"format": "string",
  				"value": "hdladmin@cnri.reston.va.us"
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 2,
  			"type": "HS_SITE",
  			"data": {
  				"format": "site",
  				"value": {
  				"version": 1,
  				"protocolVersion": "2.1",
  				"serialNumber": 2,
  				"primarySite": false,
  				"multiPrimary": false,
  				"attributes": [
  					{
  					"name": "desc",
  					"value": "CrossRef secondary"
  					}
  				],
  				"servers": [
  					{
  					"serverId": 1,
  					"address": "208.254.38.90",
  					"publicKey": {
  						"format": "key",
  						"value": {
  						"kty": "DSA",
  						"y": "pMbs83U175Qo-FncLpuMn_5l75mu89H4wrmUGyd0hcikGCjTITAT9Eue4nnkniDy18BEvBg9P3OikIAtHR-nxgSXT9n8jzz-ShAYAJHT90Dh4O9wem6mftC8f5CuTINQxDC5lC3zSGb_OK5abrqKBtUPVBgPz-Y8_2aoCJ6DJno",
  						"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  						"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  						"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  						}
  					},
  					"interfaces": [
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "TCP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": false,
  						"protocol": "UDP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "HTTP",
  						"port": 8000
  						}
  					]
  					}
  				]
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 3,
  			"type": "10320/ra_name",
  			"data": {
  				"format": "string",
  				"value": "Crossref"
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 4,
  			"type": "10320/loc",
  			"data": {
  				"format": "string",
  				"value": "<locations http_sc=\"302\">\n<location weight=\"0\" http_role=\"conneg\" href_template=\"https://data.crossref.org/{hdl}\" />\n<xlocation weight=\"0\" role=\"metadata\" href_template=\"http://metadata.labs.crossref.org/?dois={hdl}&format=unixref\" />\n</locations>"
  			},
  			"ttl": 86400,
  			"timestamp": "2018-05-02T02:51:55Z"
  			},
  			{
  			"index": 5,
  			"type": "HS_SITE",
  			"data": {
  				"format": "site",
  				"value": {
  				"version": 1,
  				"protocolVersion": "2.10",
  				"serialNumber": 1,
  				"primarySite": false,
  				"multiPrimary": true,
  				"attributes": [
  					{
  					"name": "desc",
  					"value": "crossref frankfurt aws"
  					}
  				],
  				"servers": [
  					{
  					"serverId": 1,
  					"address": "18.196.155.89",
  					"publicKey": {
  						"format": "key",
  						"value": {
  						"kty": "DSA",
  						"y": "YRnpX8DpbFVi1r2R4ZaHWfRMimneDcvuyVWyDPlsVuw-TzCouEuy2gSq92bDCAIIiKVwvn1pzkEsmGM1zlvHaXPlgtYX0JriNASWAy3OBb0jrrPa8szWwzA2JHfVOMEKF7uZnKOwChyXYsSaDG_NLQmJWLEBLtZJexdAzu6lZM0",
  						"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  						"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  						"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  						}
  					},
  					"interfaces": [
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "TCP",
  						"port": 2644
  						},
  						{
  						"query": true,
  						"admin": false,
  						"protocol": "UDP",
  						"port": 2644
  						},
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "HTTP",
  						"port": 8003
  						}
  					]
  					}
  				]
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2020-04-09T01:42:11Z"
  			},
  			{
  			"index": 6,
  			"type": "HS_SITE",
  			"data": {
  				"format": "site",
  				"value": {
  				"version": 1,
  				"protocolVersion": "2.10",
  				"serialNumber": 1,
  				"primarySite": true,
  				"multiPrimary": true,
  				"attributes": [
  					{
  					"name": "desc",
  					"value": "crossref nova aws"
  					}
  				],
  				"servers": [
  					{
  					"serverId": 1,
  					"address": "34.237.107.54",
  					"publicKey": {
  						"format": "key",
  						"value": {
  						"kty": "DSA",
  						"y": "RJn7FxX8tKMei6LOuC2Y2uQfm8ykNP5P1OJla8jSFWgshWCaW-12_CFbj3BDYXd8OHSTshLNnEtQYDL1SKgOjoBuNPjmEkNbrPzhEzszUhGvvRrLpiaripTrUAzSP35b1zfXk8lBRbHNmVbCF6deYovkgN0WRmRstymHlnBYD-A",
  						"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  						"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  						"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  						}
  					},
  					"interfaces": [
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "TCP",
  						"port": 2644
  						},
  						{
  						"query": true,
  						"admin": false,
  						"protocol": "UDP",
  						"port": 2644
  						},
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "HTTP",
  						"port": 8003
  						}
  					]
  					}
  				]
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2018-09-11T11:11:11Z"
  			},
  			{
  			"index": 7,
  			"type": "PROXY_ERROR_URL",
  			"data": {
  				"format": "string",
  				"value": "https://apps.crossref.org/DOIComplaint/"
  			},
  			"ttl": 86400,
  			"timestamp": "2017-02-03T16:06:42Z"
  			},
  			{
  			"index": 8,
  			"type": "DESC",
  			"data": {
  				"format": "string",
  				"value": "There is also a silent primary running at Crossref in Boston - 10/26/12. \nRobert and Tim set it up - JHE"
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 9,
  			"type": "#HS_SITE#Denver",
  			"data": {
  				"format": "base64",
  				"value": "AAECAQABAAIAAAAAAAAAAQAAAARkZXNjAAAAFkNyb3NzUmVmIE1pcnJvciBEZW52ZXIAAAABAAAAAQAAAAAAAAAAAAAAAD97mPgAAAG5AAAAC0RTQV9QVUJfS0VZAAAAAAAVAJdgUI8VIwvMspK5gqLrhAvwWBz1AAAAgQD9f1OBHXUSKVLfSpwu7OTn9hG3UjzvRADDHj+AtlEmaUVdQCJR+1k9jVj6v8X1ujD2y5tVbNeBO4AdNG/yZmC3a5lQpaSfn+gEexAiwk+7qdf+t8Yb+DtX58aophUPBPuD9tPFHsMCNVQTWhaRMvZ1864rYdcq7/IiAxmd0UgBxwAAAIEA9+GghdabPd7LvKtcNrhXuXmUr7v6OuqC+VdMCz0HgmdRWVeOutRZT+ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN/C/ohNWLx+2J6ASQ7zKTxvqhRkImog9/hWuWfBpKLZl6Ae1UlZAFMO/7PSSoAAACBAJOopl56CBVDfnso5hKD/ei71eXE9vOdO/Q1BPtSLAp73WcftwFnEyAXqR7tKJLzMpn0CBwplaSL03zpsHpKnppiGkpm0Ic5CsIRZsJA+SER07SUn1myzh9lndp4hK0LfTFB+WUDYuf6FbrlL49Ea3IauTbtD3uri9rbM2yvAbXtAAAAAwMBAAAKUQAAAAAKUQMCAAAfQA=="
  			},
  			"ttl": 86400,
  			"timestamp": "2018-06-18T20:07:39Z"
  			},
  			{
  			"index": 11,
  			"type": "HS_SITE",
  			"data": {
  				"format": "site",
  				"value": {
  				"version": 1,
  				"protocolVersion": "2.10",
  				"serialNumber": 2,
  				"primarySite": false,
  				"multiPrimary": true,
  				"attributes": [
  					{
  					"name": "desc",
  					"value": "xref oak"
  					}
  				],
  				"servers": [
  					{
  					"serverId": 1,
  					"address": "38.100.138.134",
  					"publicKey": {
  						"format": "key",
  						"value": {
  						"kty": "DSA",
  						"y": "rmkuzMD5-3vbsEBxsRBWauFbPPEHDp_hm5Bwrn2z9ha7W0YyoWA7ZMFqspotg9lhj4aJJtZ065TItM_Fe6bVQu_imAK8n1ZsfSDQotDz33vNkqUXEr0hmVtxKaoV3BdwWY4iMdlUQigSsG8Z0nGsqAi5epdaSiCoS5Y_IA78JpA",
  						"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  						"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  						"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  						}
  					},
  					"interfaces": [
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "TCP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": false,
  						"protocol": "UDP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "HTTP",
  						"port": 8000
  						}
  					]
  					}
  				]
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2020-03-04T22:37:54Z"
  			},
  			{
  			"index": 12,
  			"type": "#HS_SITE#redwood1",
  			"data": {
  				"format": "base64",
  				"value": "AAECCgABQAIAAAAAAAAAAQAAAARkZXNjAAAAGHhyZWYgcHJpbWFyeSBvbiByZWR3b29kMQAAAAEAAAABAAAAAAAAAAAAAAAAJmSKiQAAAbgAAAALRFNBX1BVQl9LRVkAAAAAABUAl2BQjxUjC8yykrmCouuEC/BYHPUAAACBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAAAAgQD34aCF1ps93su8q1w2uFe5eZSvu/o66oL5V0wLPQeCZ1FZV4661FlP5nEHEIGAtEkWcSPoTCgWE7fPCTKMyKbhPBZ6i1R8jSjgo64eK7OmdZFuo38L+iE1YvH7YnoBJDvMpPG+qFGQiaiD3+Fa5Z8GkotmXoB7VSVkAUw7/s9JKgAAAIBlex4kanhm9mxRmf5toPA4uNjvmm48A4xAsCA00jaeuxSUyXHeB0jBNyFPVMM9TZ9F+BWwq77k7YCDszCvzTtSbLG3xK8KGW5arFykTAQ1Gx+DNCKefgLzUaI8zcL2KuLNxOnDHt2yn6A+XTNcv0/FWNkMHt8NOZjG6HQvtNcIigAAAAMDAQAAClECAAAAClEDAgAAH0A="
  			},
  			"ttl": 86400,
  			"timestamp": "2020-02-29T08:24:42Z"
  			},
  			{
  			"index": 13,
  			"type": "HS_SITE",
  			"data": {
  				"format": "site",
  				"value": {
  				"version": 1,
  				"protocolVersion": "2.10",
  				"serialNumber": 2,
  				"primarySite": false,
  				"multiPrimary": true,
  				"attributes": [
  					{
  					"name": "desc",
  					"value": "xref mirror singapore"
  					}
  				],
  				"servers": [
  					{
  					"serverId": 1,
  					"address": "54.169.7.16",
  					"publicKey": {
  						"format": "key",
  						"value": {
  						"kty": "DSA",
  						"y": "HInGsOrsqNaD1NJTuOIHAIH9xIvFVrN4CEIq-VSGfPC1sHPUk0R3sYDmoYcSQPb9UkhPe3EfYscpOEkVuq1f5IcJfjh6BfzySkb32rPHpGnx4pqgEEUwg_3Vr-VBg3IdzJcFg8-moN4LhQ9OdhlFYn1LEImK6rY5xQoxCoqYiIA",
  						"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  						"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  						"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  						}
  					},
  					"interfaces": [
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "TCP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": false,
  						"protocol": "UDP",
  						"port": 2641
  						},
  						{
  						"query": true,
  						"admin": true,
  						"protocol": "HTTP",
  						"port": 8000
  						}
  					]
  					}
  				]
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2019-05-14T20:41:20Z"
  			},
  			{
  			"index": 14,
  			"type": "#HS_SITE#rackspace",
  			"data": {
  				"format": "base64",
  				"value": "AAECCgABAAIAAAAAAAAAAQAAAARkZXNjAAAAFXhyZWYgbG9uZG9uIHJhY2tzcGFjZQAAAAEAAAABAAAAAAAAAAAAAAAAog1RDwAAAbkAAAALRFNBX1BVQl9LRVkAAAAAABUAl2BQjxUjC8yykrmCouuEC/BYHPUAAACBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAAAAgQD34aCF1ps93su8q1w2uFe5eZSvu/o66oL5V0wLPQeCZ1FZV4661FlP5nEHEIGAtEkWcSPoTCgWE7fPCTKMyKbhPBZ6i1R8jSjgo64eK7OmdZFuo38L+iE1YvH7YnoBJDvMpPG+qFGQiaiD3+Fa5Z8GkotmXoB7VSVkAUw7/s9JKgAAAIEAmlOywMbb+MfdCSrzpsh21lcVmeq09BVmakHgSGGk7eWNLromoxd8oy8Raqqh9l9VF9Zfms0rFdm52AA4WTwfpknsTi3fr+sAjEY9md7n2qcpMrCRQQxdilprClTYDWg5+owbRN65A3K6GtzdI9IjAt012IfC85YZs08VJVD1PWkAAAADAwEAAApRAgAAAApRAwIAAB9A"
  			},
  			"ttl": 86400,
  			"timestamp": "2017-04-03T17:25:10Z"
  			},
  			{
  			"index": 100,
  			"type": "HS_ADMIN",
  			"data": {
  				"format": "admin",
  				"value": {
  				"handle": "0.NA/10.SERV",
  				"index": 200,
  				"permissions": "111111110010"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 200,
  			"type": "HS_VLIST",
  			"data": {
  				"format": "vlist",
  				"value": [
  				{
  					"handle": "200/1",
  					"index": 300
  				},
  				{
  					"handle": "200/4",
  					"index": 300
  				},
  				{
  					"handle": "200/23",
  					"index": 300
  				},
  				{
  					"handle": "200/27",
  					"index": 300
  				},
  				{
  					"handle": "0.SERV/10.crossref",
  					"index": 311
  				},
  				{
  					"handle": "10.cradmin/cruser",
  					"index": 300
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 303
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 305
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 307
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 311
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 312
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 313
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 314
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 315
  				},
  				{
  					"handle": "10.SERV/CROSSREF",
  					"index": 316
  				},
  				{
  					"handle": "200/28",
  					"index": 300
  				}
  				]
  			},
  			"ttl": 86400,
  			"timestamp": "2018-04-20T14:30:26Z"
  			},
  			{
  			"index": 303,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "jvujg9dFy3HCRUPcWNquM6Nzk9iIq-atgMf0bNUr_urGgKDyHIwGKuNs3wIZHvcJiKijRX9Vqn6SOfXrP9f1HeT9aa5ry8oeszvLnPzgdNkJ4jWZlzdnmtIu0ebdVKK_oOiKbLW65-kCG1J4ustBzPMF-j8DXjqOrSkChRXzcSc",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 305,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "r9_fiS6ykQrv09uJKutxyNSt8EItpG0ASepSVIPrLbgE1pNhIFy-3cxDtj2hNfMF8zKCz3v09Ndez9ukXcl1CO3kPJFYv8XSC4FqhgSy3cH6Q8qkvCG_l_pP92DjsVe8LGN6A0_5qU7YkAtoNhvOokuEw6liLB9v4KeV77-WUPE",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 307,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "6xC066B8KlVrxx7xRJrzo4geuxVgDNWeopnXHqAB92V54L04vf2v8HOmOOZRExvKy3zsVSF4Z_iTjiVUViJdX3eQUIBRl4671E5wbCNI5XcTH51HfbdhRA-sGNoS4jjba_MF2Md7VtGGEZXzN6vr-9XZVktSFksCORfEo-P9KFo",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 311,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "RSA",
  				"n": "g_Ky6X-4uh-8YuoL6Da56YfIWJHm0RdKwPNizyXOvpd1_FZBYH5NV4KZTy_ObtT5NKeX2mLeaVrC3CXd2zgs2kgbjJ7ahWyZbzZdzP_uRgPr1NdF_hnIpdmLqxCm5vTzbPZydJg0Gd5YOJwbqnL9bcxKC8ygpA9HljYDaTSc9gXvDrh6TCMdNnhiOPbW3vFbTyxi5TqJw5g3yLlFKkalQeGTzooq_ZWb8pT-TpcZJiPTGcKP1VulT35PxVNqLpMUJp0H3T4oW6OddcY6WcBPS4Ldy1kXKqosemb2GcL_Mk_Mp_66F33hYb06Y1hHqMQotQl2ysuXl7fmS8aTgmS38w",
  				"e": "AQAB"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 312,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "zOtfV33bEmtWL-utcJ9vzYe87vWh526Ax9XLftanvTyxX347dcrlY20vJfNAFVGfTXv3b5IWA8dQfiPieyy52L6dGg-mXeKlxivEHCoJGqXxrXdhrJpCXjfUkR7OrSVgTKseGOOeEEn7hpefv-xoQpdBjkacP8bDHqkHpvNMhXo",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 313,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "HeEFl5UKHkLKC2yazQasIi-obVtvsgzRSneBy9w_sSJXdMQFhWS95CY0F1jwiAbL7tQeU_bZHkddenH6O6CFfZdmAENcuvqcUD7loG1bkFPI7okEJK9bNxbKbtpJnsj1ywsBQFrtaghOJvMgabaXcnrpaxGQ5BBzupeDfN2Wx9k",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 314,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "DSA",
  				"y": "mFda9l6HS-vyErGdEzxJ9uLqCbYbWfDCkscbzZLyDbDMRf2k1oeSxKc8s0Ay0HPRD_T-9f6iL_lPvK8Oq5116-Z8O-ZUouGjvfSCulogtKsDIp9E1gZl7WMukkzJL6b4Qx3kU5LGSZewjjGaXTDi992x9nDuWUBKiG4v8P_kOtE",
  				"p": "_X9TgR11EilS30qcLuzk5_YRt1I870QAwx4_gLZRJmlFXUAiUftZPY1Y-r_F9bow9subVWzXgTuAHTRv8mZgt2uZUKWkn5_oBHsQIsJPu6nX_rfGG_g7V-fGqKYVDwT7g_bTxR7DAjVUE1oWkTL2dfOuK2HXKu_yIgMZndFIAcc",
  				"q": "l2BQjxUjC8yykrmCouuEC_BYHPU",
  				"g": "9-GghdabPd7LvKtcNrhXuXmUr7v6OuqC-VdMCz0HgmdRWVeOutRZT-ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN_C_ohNWLx-2J6ASQ7zKTxvqhRkImog9_hWuWfBpKLZl6Ae1UlZAFMO_7PSSo"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2016-09-21T17:37:43Z"
  			},
  			{
  			"index": 315,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "RSA",
  				"n": "l8LFfQjHMn5sSK757mUH332Q_XbivN0mGkXkn8MURMEoVke-ziI4hyeiWgbZxfhwR8ALBnY0ESNKdNV4BSUUBoT2vxcvEL7e1jC1TP3c2emjZMgrq2cIUfrhjC6Q3BYWrgRzq9PsPADIDzc7xeXDCE6MXrJZP4vsYVCJ7oN4hmKSZmilWNy8iFpgM9nUsm4jMB1E3eUxVJRbfa2lrfEogSfCOejbVuahc5q_X7Fjb2cmse_TV0-D8V2RZ5etcx558ibUFqoK4Nqe8sbhO5r_diXi99bXdFM-kcnGKXX3evDEzkxXE9nRp0wz3xEq9nbiZAajGvJ76_UAbd2PadedcQ",
  				"e": "AQAB"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2018-01-26T19:59:39Z"
  			},
  			{
  			"index": 316,
  			"type": "HS_PUBKEY",
  			"data": {
  				"format": "key",
  				"value": {
  				"kty": "RSA",
  				"n": "hZ2kwWprs4x2KlPwWVIgvHq22mT07B-WxLK3erGfQk5uWDBtfnsDb3nJPQvvZOJAyaeXLt7WPr60DxED-AcjGqIp_bUUegO4jiQUW9OXWpkXZ7VZdwAe4rHamvizMzPGv-FrhjexxbQoyBHmT-0PTnLWqiRvBPqv7cku9lZfNH4vccMHPrYNzjuS6HPzou66EZqLYhu-mWdjf0tNi9Vib0emVF8IO7iTZEIngdWmDoNedFBKrY6_uJvYvs81TfAewCOIXZynQLTmMdrgoWPNvgQnnMQ0mzOMRDIWg0cUKGFv26tfUkvtEQr5A_zgQZgrEHjVKI1rUixwXGZcQJOpmw",
  				"e": "AQAB"
  				}
  			},
  			"ttl": 86400,
  			"timestamp": "2018-01-26T20:09:50Z"
  			}
  		]
  		}
  	],	
  }
  ```



## 5.7. 缓存删除

+ URL

  | URL                                              | 描述 |
  | ------------------------------------------------ | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/tasks |      |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                                    |
  | ------ | ------ | ------ | --------------------------------------- |
  | handle | String | N/A    | handle标识                              |
  | index  | Array  | N/A    | handle index 列表。为空，则表示查询全部 |
  | type   | Array  | N/A    | handle type列表。为空，则表示查询全部   |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "tasktype":"cachedelete",
              "data":{
              	"handle":"10.serv/crossref",
             	 	"index":[],
              	"type":[],
              }
          },
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied",
  	"taskid":3
  }
  ```

  

## 5.8. 应答结果检查

### 5.8.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value     |
  | ---- | --------- |
  | bt   | selfcheck |
  | sbt  | switch    |

+ data字段定义

  | 名称   | 类型   | 默认值  | 描述                            |
  | ------ | ------ | ------- | ------------------------------- |
  | switch | String | disable | 功能开关，值为：enable或disable |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"selfcheck",
              "sbt":"switch",
              "op":"add",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

### 5.8.2. 策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value     |
  | ---- | --------- |
  | bt   | selfcheck |
  | sbt  | rules     |

+ data字段定义

  | 名称         | 类型   | 默认值 | 描述                                           |
  | ------------ | ------ | ------ | ---------------------------------------------- |
  | type         | String | N/A    | handle标识类型                                 |
  | responsecode | Int    | 1      | handle应答结果返回码，默认保存"successful"应答 |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"selfcheck",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "type":"url",
                  "responsecode":1
              }
          }
      ]
  }
  ```

  

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

## 

## 5.9. 后端限速

### 5.9.1. 功能开关

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value        |
  | ---- | ------------ |
  | bt   | backendmeter |
  | sbt  | switch       |

+ data字段定义

  | 名称   | 类型   | 默认值  | 描述                            |
  | ------ | ------ | ------- | ------------------------------- |
  | switch | String | disable | 功能开关，值为：enable或disable |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backendmeter",
              "sbt":"switch",
              "op":"add",
              "data":{
                  "switch":"enable"
              }
          }
      ]
  }
  ```


+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

### 5.9.2. 后端限速策略

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value        |
  | ---- | ------------ |
  | bt   | backendmeter |
  | sbt  | rules        |

+ data字段定义

  | 名称  | 类型 | 默认值 | 描述           |
  | ----- | ---- | ------ | -------------- |
  | meter | Int  | N/A    | 未命中限速阈值 |
  |       |      |        |                |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":100,
              "bt":"backendmeter",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "meter":1000
              }
          }
      ]
  }
  ```

  

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```



# 6. 递归子系统

## 6.1. 存根管理

+ URL

  | URL                                                | 描述 |
  | -------------------------------------------------- | ---- |
  | http(s)://$HOST:$PORT/handle/v1.0/internal/configs |      |

+ bt/sbt字段定义

  | 名称 | value |
  | ---- | ----- |
  | bt   | stub  |
  | sbt  | rules |

+ data字段定义

  | 名称   | 类型   | 默认值 | 描述                                         |
  | ------ | ------ | ------ | -------------------------------------------- |
  | handle | String | N/A    | handle标识                                   |
  | ttl    | Int    | N/A    | ttl，绝对时间                                |
  | index  | Int    | N/A    | handle index值                               |
  | type   | String | N/A    | handle type值                                |
  | data   | String | N/A    | handle value值，不同的type，data字段格式不同 |
  |        |        |        |                                              |

+ 接口数据举例

  ```
  {
      "contents":[
          {
              "source":"ms",
              "id":101,
              "bt":"stub",
              "sbt":"rules",
              "op":"add",
              "data":{
                  "handle":"ncstrl.vatech_cs/*",
                  "ttl":86400,
                  "index":3,
                  "type":"hs_site",
                  "data":{
                  	"version":1,
                  	"protoversion":"2.10",
                  	"serialnum":2,
                  	"primarymask":192,
                  	"hashoption":2,
                  	"hashfilter":0,
                  	"attrlist":"doi oak",
                  	"serverlist":[
                  		{
                  			"serverid":1,
                  			"address":"38.100.138.133",
                  			"publickey":{
                  				"type":"HS_DSAKEY",
                  				"key":"iQCuR2R",
                  			},
                  			"serviceinterface":[
                  				{
                  					"type":3,
                  					"transproto":1,
                  					"port":2641,
                  				},
                  				{
                  					"type":2,
                  					"transproto":0,
                  					"port":2641,
                  				},
                  			],
                  		},
                  	],
                  },
              }
          }
      ]
  }
  ```

+ 返回值

  ```
  {
  	"rcode":0,
  	"description":"recevied"
  }
  ```

## 6.2. 健康检查

## 6.3. 可信解析









