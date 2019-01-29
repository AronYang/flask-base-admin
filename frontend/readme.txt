此为EyeOps前端web文件, 使用webpack打包，使用node运行环境  

前端所涉及技术：  
  vue, vuex, vue-router, axios, webpack, javascript, css, html等

1、安装node: 
yum install node  
yum install npm  

2、安装淘宝工具cnpm:
npm install -g cnpm --registry=https://registry.npm.taobao.org

3、安装依赖：
cnpm install  
#安装完后的依赖都会在node_modules目录下  

4、运行开发环境：
npm run dev  

5、运行生产环境：
npm run build  
#生成后的web文件存放在dist目录下，把dist下的文件放到nginx的web目录下即可。  


