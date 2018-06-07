# oss_sync
- 目前只支持在windows下运行，linux下未做测试。
- 程序只会上传运行后新加入的文件，不会做删除操作

# 参数说明
```
FILE_PATH             :监控的目录
Prefix                :迁移到oss的路径为destBucket/destPrefix + relativePath
OSS_ACCESS_KEY_ID     :access key
OSS_ACCESS_KEY_SECRET :secret key
OSS_BUCKET_NAME       :bucket 名称
OSS_ENDPOINT          :bucket 对应的endpoint
```
