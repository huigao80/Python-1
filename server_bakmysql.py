import sys
sys.path.append('./lib/')
import os,kl_log
from kl_smtp import send_mail
import time
import zipfile
import threading

'''''
mysqldump
Usage: mysqldump [OPTIONS] database [tables]
OR     mysqldump [OPTIONS] --databases [OPTIONS] DB1 [DB2 DB3...]
OR     mysqldump [OPTIONS] --all-databases [OPTIONS]
For more options, use mysqldump --help
'''
mailto_list=["735579768@qq.com"]
db_host="127.0.0.1"
db_user="root"
db_passwd="adminrootkl"
db_name=['union.0yuanwang.com','0yuanwang_db','5257','blog','ruzhouba','shijiyaolan_db','sjyl','sjyl_hb','sjyl_hc','sjyl_jx','sjyl_qx','sjyl_zz','taier','zhaokeli_db']
db_charset="utf8"

def bakmysql(db_name,sss):
    try:
        global baknum
        baknum=baknum+1
        db_backup_name=r".\data\bakmysql\%s_%s.sql"%(time.strftime("%Y-%m-%d_%H-%M-%S"),db_name)
        if os.path.exists(os.path.dirname(db_backup_name))==False :
            os.makedirs(os.path.dirname(db_backup_name))
        zip_src = db_backup_name
        zip_dest = zip_src + ".zip"
        database.append(zip_dest)

        print("开始备份数据库:%s..."%db_name);
        os.system("mysqldump --skip-comments -h%s -u%s -p%s %s  --default_character-set=%s    > %s" %(db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
        print("开始压缩数据库:%s..."%db_name)
        #zip_files(zip_src,zip_dest)
        f = zipfile.ZipFile(zip_dest, 'w' ,zipfile.ZIP_DEFLATED)
        f.write(zip_src)
        f.close()
        os.remove(zip_src)
        print("数据库%s备份完成!"% db_name)
        zipsize=os.path.getsize(zip_dest)
        if zipsize<50*1024*1024 :
            print('开始发送邮件...')
            if send_mail(mailto_list,db_name+"数据库备份完成",db_name+"数据库备份完成",zip_dest):
                print ("发送成功")
            else:
                print ("发送失败")
        else:
            print('数据库%s大于(%s)50M不能发送'%(db_name,zipsize))
        baknum=baknum-1
    except:
        baknum=baknum-1
        kl_log.write('备份数据库%s时出错'%db_name,'bakmysql')

if __name__ == "__main__":
    baknum=0
    database=[]
    for i in db_name:
        time.sleep(1)
        threading.Thread(target=bakmysql,args=(i,'')).start()
    time.sleep(3)
    while baknum != 0:
        time.sleep(1)
        sys.stdout.write('%s个进程备份中...\r' % baknum)
        sys.stdout.flush()
        pass
    #压缩所有已经备份好的数据库
    print('正在压缩所有数据库为一个文件...')
    db_backup_name=r".\data\bakmysql\%s_all.zip"%(time.strftime("%Y-%m-%d_%H-%M-%S"))
    f = zipfile.ZipFile(db_backup_name, 'w' ,zipfile.ZIP_DEFLATED)
    for i in database:
        f.write(i)
        os.remove(i)
    f.close()
    try:
        input("所有数据库备份完成,按任意键继续...")
    except:
        pass

