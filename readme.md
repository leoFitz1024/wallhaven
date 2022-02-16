### 问题反馈qq群：908029055

#### 待添加功能

1、本地列表显示文件夹占用大小

2、本地列表增加删除按钮

3、本地列表增加打开文件夹按钮

#### 打包

##### 使用 nuitka

1. 执行以下命令

2. 把import_libs下的全部内容复制到生成的dist文件夹下

3. 把静态资源icon文件夹复制到dist文件夹下

   参数：--windows-uac-admin 申请admin权限
   
   

```commandline
nuitka --standalone --windows-disable-console --mingw64 --show-memory --show-progress --plugin-enable=qt-plugins --include-qt-plugins=sensible,styles --plugin-enable=numpy --windows-uac-admin  --follow-import-to=lib --output-dir=out2 --windows-icon-from-ico=icon.ico WallhavenIcon.py
```

debug

```commandline
nuitka --standalone --mingw64 --nofollow-imports --show-memory --show-progress --plugin-enable=qt-plugins --include-qt-plugins=sensible,styles --plugin-enable=numpy --windows-uac-admin  --follow-import-to=lib --output-dir=out --windows-icon-from-ico=icon.ico WallhavenIcon.py
```



##### 使用 pyinstaller

-w 无命令行
--uac-admin

```commandline
pyinstaller -D -w --i icon.ico  Wallhaven.py
```
