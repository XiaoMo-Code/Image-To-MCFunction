# ITM(Image To MCFunction)
这是一个可以把图像转换为MCFunction的工具，你可以自定义图像的比例以及一些其他的参数，那么接下来我将带你使用这个工具
## 使用方法
- 依赖Python
    - 安装Python

        下载地址：[**Python3.6.8**](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)

        安装方式：(点击上面蓝色字体即可)
        
        安装完成后，打开命令提示符(**Win+R**输入**cmd**)，再在命令提示符输入`python --version`，若显示python版本号，则安装成功

    - 安装依赖
        打开命令提示符(**Win+R**输入**cmd**)，再在命令提示符输入以下命令：
        ```bash
        pip install pillow
        pip install requests
        ```
        若显示成功，则安装成功
    安装完以上要素后直接执行以下命令：
        ```bash
        python main.py
        ```
        或者直接运行**main.py**文件，没有报错则成功，报错则失败
    
- 不依赖Python
    - 下载地址：[**ITM**](https://release-assets.githubusercontent.com/github-production-release-asset/1051150364/c7c0304e-991e-4084-9b38-a109c76d6874?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-09-05T15%3A27%3A50Z&rscd=attachment%3B+filename%3Dv7.0.1-ITM7.0-alpha.exe&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-09-05T14%3A27%3A11Z&ske=2025-09-05T15%3A27%3A50Z&sks=b&skv=2018-11-09&sig=etf1NNohsNynzl81YSHkXd08lrBT5zCpP24gsQNSISs%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc1NzA4Mjc0NywibmJmIjoxNzU3MDgyNDQ3LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.sxrSNUg8ssj87rsjVdHav9nlBQvlQT4SxIh3bIlxcb8&response-content-disposition=attachment%3B%20filename%3Dv7.0.1-ITM7.0-alpha.exe&response-content-type=application%2Foctet-stream)

        直接运行**main.exe**文件，只能在windows上执行，Win7及以下不支持

- 打开**main.exe**文件
    - 界面
        界面如下：
        ![深色模式](https://github.com/XiaoMo-Code/Image-To-MCFunction/blob/main/textures/dark_InterFace.png)
    - 菜单
        你在它的非输入部分右键会打开菜单，菜单如下：
        ![菜单](https://github.com/XiaoMo-Code/Image-To-MCFunction/blob/main/textures/menu.png)
        - 色系切换

            点击菜单上的颜色模式可以切换色系，有深色模式和浅色模式
            每次打开默认都是深色模式，你可以根据自己的喜好切换色系
            浅色模式除了画布和菜单的颜色，其他的颜色都和深色模式相反
        - 是否跳过透明像素

            点击菜单上的**跳过透明**可以切换是否跳过透明像素
            点击后会在菜单上的`跳过透明`后面显示的是`✔`则代表跳过透明，在这之后转换的图片如果遇到透明像素就不转换，但如果显示的是`✘`则把透明像素当做那个透明像素的对应颜色
        - 是否添加斜杠

            点击菜单上的**添加斜杠**可以切换是否添加斜杠
            点击后会在菜单上的`添加斜杠`后面显示的是`✔`则代表添加斜杠，在这之后转换出来的指令会在最前面加一个`/`但如果后面显示的是`✘`那么转换出来的指令没有斜杠
        - 是否添加常加载区块

            点击菜单上的**常加载区**可以切换是否添加常加载区块
            点击后会在菜单上的`常加载`后面显示的是`✔`则代表添加常加载区块，在这之后转换出来的指令会及时添加常加载区块并删除上一个常加载区块防止堵塞但如果显示的是`✘`那么转换出来的指令没有常加载区块
        - 二维优化

            点击菜单上的**二维优化**可以切换是否二维优化
            点击后会在菜单上的`二维优化`后面显示的是`✔`则代表二维优化开启，二维优化的同时如果开启了常加载区块的使用那么会删除所有用于删除区块的指令并把常加载区块设置的所有指令最上面，且优化后会看中图像的`X`、`Z`两个轴当一个轴上所有方块的一样时会把这个轴上的指令合并为一个fill指令，当两个轴上一个矩形的方块都一样时会把这两个轴的所有指令合并为一个fill指令，但如果后面显示的是`✘`那么转换出来的指令按照原有的`setblock`
        - 注意

            开启`二维优化`和`常加载区`那么转换速度回比不开慢1.5倍，单开一个优化那么转换速度会比不开慢1.25倍开启二维优化后转换出的文件体积明显下降

        - 转换

            点击主界面的**开始转换**后即可开始转换

        - 注意事项、设置
            - 注意事项
                
                如果把图片的路径(绝对路径/相对路径)填入到了正确输入框内但图片无法在画布里成功加载则代表这张图片无法转换或损坏了

                如果在转换完成后没有见到主界面则代表程序卡了你需要重启程序

                如果点击主界面的`O`后进入小窗口的话5秒内不进行任何操作会开始变得透明，在确认程序可以关闭的情况下无法找到小窗口请留意屏幕

                如果把ITM的大窗口移动到左屏幕一半外那么小窗口会卡在屏幕外

                如果不手动设置地图画的尺寸那么默认会把图片的尺寸设置为地图画的尺寸

                导出的路径可以设置为相对路径或绝对路径，如果导出的路径原本有文件的话会先清除文件的内容然后再把转换后的指令全部放进去

                如果导出的路径原本没有文件的话会自动创建文件

                主界面的`开始转换`默认会在下方标明转换出的长和宽，但如果长和宽的数字太大以至于超出了按钮的宽度时，那么你可以把鼠标悬停在上面，因为那样可以查看完整的长和宽

                主界面的右下角有标明版本号，鼠标悬停可以查看完整信息

            - 设置

                当你在导入的时候可以自定义图片的比例，默认比例和图片的原始比例一样
                - 关于Minecraft地图的冷知识
                    
                    Minecraft的地图分为5级：
                    - 0级：128x128
                    - 1级：256x256
                    - 2级：512x512
                    - 3级：1024x1024
                    - 4级：2048x2048
                
                导入图片的地址必须是正确而且可以在画布中显示的否则无法导入图片




# 开发着&信息
- 原始开发者
    - 开发者：<font color="cyan">**Feeling**</font>
    - 微信：**hcgbchvh_com**
        - 名字：**Feeling**
        - 头像：
        
            <img src="https://github.com/XiaoMo-Code/Image-To-MCFunction/blob/main/textures/FeelWX.png" width=100 height=100 />
    - QQ：**2679711232**
        - 名字：**枫**
        - 头像：

            <img src="https://github.com/XiaoMo-Code/Image-To-MCFunction/blob/main/textures/FeelQQ.png" width=100 height=100 />
- 优化、UI
    - 开发者：<font color="pink">**Peach**</font>
    - QQ：**1096591237**
        - 名字：**ᴸᵒᵛᵉ桃**
        - 头像：
                    
            <img src="https://github.com/XiaoMo-Code/Image-To-MCFunction/blob/main/textures/PeachQQ.png" width=100 height=100 />
- 关于**ITM**
    - 项目地址：[**ITM**](https://github.com/XiaoMo-Code/Image-To-MCFunction)
    - 项目介绍：这是一个可以把图像转换为MCFunction的工具，你可以自定义图像的比例以及一些其他的参数
    - 项目状态：**持续开发中**
    - 当前版本号：*7.0.1*
    - 最后更新：**2024.9.3**

优化的人由于学业无法继续接下来的开发所以接下来的开发工作由原始开发者继续开发
