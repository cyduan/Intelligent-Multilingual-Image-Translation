# Intelligent-Multilingual-Image-Translation
This is a big task of university course.
1. “报告”文件夹里含**作业报告文件**以及**课堂报告ppt**
2. “代码”文件夹里包含以下内容

<!-- ### 代码 -->

##### 正常使用本作业项目需要：

1. 使用IDE软件打开**“代码”**文件夹（不能直接打开整个作业文件，不然会出现图标路径错误）
2. 运行**“main.py”**文件
3. 出现GUI
4. 点击使用各个功能

##### 文件介绍

1.  "icon"文件夹包含了该项目GUI的所有图标
2.  pytesseract 与Tesseract-OCR 文件夹为python的两个库。为了避免调用这两个关键库出现问题，将其直接放置在这里便于使用。
3.  “pictures”文件夹收录**截图**功能所得图片
4.  “test”文件夹里存放有测试本程序功能所需的图片
5.  “translate.py”文件用于实现翻译功能
6.  "screenshot.py"文件用于实现截图功能
7.  “wordscloud.py”文件用于实现生产词云功能
8.  **“main.py”**为该项目的**主程序**，用于创建本程序的**GUI**,并**统合各个功能**
9.  “get_dpi.py”文件用于获取电脑的屏幕**缩放比例**，以用来修正使用pyQt库导致的一个bug（GUI缩放比例被初始化，导致显示异常）

