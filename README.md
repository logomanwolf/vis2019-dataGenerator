## 简介

### 目的

检测动态图中，相似动态子图查找算法的有效性。

当输入动态子图，检测到它的相似动态子图的precision和recall。

- precision：$P=\frac{TP}{TP+FP}$，即检测到的结果中，真正与原图相似的子图的比例。
- recall：$R=\frac{TP}{TP+FN}$，即检测到的结果中真正与原图相似的子图，占所有分类正确的结果（没有检测到的与原图不相似的子图+检测到的与原图相似的子图）





### 数据构造情况

目前加入的数据结构：

![image-20181227155059166](/Users/jackie/Repository/vis2019/dataGenerator/assets/image-20181227155059166.png)![image-20181227155106575](/Users/jackie/Repository/vis2019/dataGenerator/assets/image-20181227155106575.png)![image-20181227155112006](/Users/jackie/Repository/vis2019/dataGenerator/assets/image-20181227155112006.png)![image-20181227155118263](/Users/jackie/Repository/vis2019/dataGenerator/assets/image-20181227155118263.png)

这些社团会通过一些简单的路径相连，形成一个连通子图。比如，使用环状路径来连接这些子图：

![image-20181227213619115](/Users/jackie/Repository/vis2019/dataGenerator/assets/image-20181227213619115.png)

