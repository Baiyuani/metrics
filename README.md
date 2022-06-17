## 简易网站监控程序
> 搭配prometheus使用。 \
> 请求指定url，通过判断返回的http状态码判断网站健康状态。
> 


| 变量名称    | 取值示例                   | 说明                 |
|---------|------------------------|--------------------|
| WM_ENV  | prod                   | 部署环境（固定值）          |
| WM_PORT | 5000                   | 程序监听的端口            |
|  WM_THREADING_NUM       | 10                     | 任务并行数量             |
| WM_PATH| /metrics               | 程序访问路径             | 
|NAMESPACE| default        | 数据来源，监控数据origin的取值 |
| EX_LABELS | {label1="v1",label2="v2"} | 扩展返回数据的label       |