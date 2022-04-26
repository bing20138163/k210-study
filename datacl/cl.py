import os
import sys
import shutil
from xml.etree.ElementTree import parse, Element
import zipfile

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
      # 备注root返回当前目录路径；dirs返回当前路径下所有子目录；files返回当前路径下所有非目录子文件
        #print(root)  # 当前目录路径
        #print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        return root, dirs, files

if __name__ == '__main__':

    #0.获取原始图片文件名列表
    file_dir = "./firstpic/"
    dataimg_dir = "./datasets/images/"
    dataxml_dir = "./datasets/xml/"
    root, dirs, files = file_name(file_dir)

    #1.生成指定的模板xml数量
    for i in range(1,len(files)+1):
        shutil.copyfile("./mode.xml",  dataxml_dir + str(i) + ".xml")

    #2.依次生成1~N对应图片和修改对应XML内容
    j = 1
    for line in files:
        shutil.copyfile(file_dir + line, dataimg_dir + str(j) + ".jpg")
        #strline = line[0] + line[2] + line[4] + line[6] + line[8] + line[10]

        newStr = os.path.join(dataxml_dir, str(j) + ".xml")
        dom = parse(newStr)  # 获取xml文件中的参数
        root = dom.getroot()  # 获取数据结构

        for obj in root.iter('object'):  # 获取object节点中的name子节点（此处如果要换成别的比如bndbox）
            name = obj.find('name').text  # 获取相应的文本信息
            #  以下为自定义的修改规则，我这里把文本信息为[1]~[6]的内容改成对应位置数字
            if name == '[1]':
                new_name = line[0]
            elif name == '[2]':
                new_name = line[2]
            elif name == '[3]':
                new_name = line[4]
            elif name == '[4]':
                new_name = line[6]
            elif name == '[5]':
                new_name = line[8]
            elif name == '[6]':
                new_name = line[10]
            obj.find('name').text = new_name  # 修改
        dom.write(dataxml_dir + str(j) + ".xml", xml_declaration=True)  # 保存到指定文件
        j = j + 1
        pass

    #3.压缩文件夹
    path = './datasets.zip'  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)

    z = zipfile.ZipFile('datasets.zip', 'w', zipfile.ZIP_DEFLATED)
    startdir = "./datasets"
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            z.write(os.path.join(dirpath, filename))
    z.close()