import pandas as pd
from dbtools.dbbase import Oracle, MsSql
import sendMail


def contrast():
    # 接收人
    mailto_list = '**********@**.**,***@**.***'
    
    # 附件路径名
    filename = './excel/E3+与IWMS库存对比.xlsx'

    try:
        # 建立数据库连接
        oracle = Oracle(dbtype='oracle', db='E3ZS')
        mssql = MsSql(dbtype='mssql', db='IWMS')

        # 执行脚本，并返回数据帧对象
        e3 = oracle.get_DataFrame('./sql/E3+inventory.sql')
        iwms = mssql.get_DataFrame('./sql/IWSinventory.sql')
    finally:
        if oracle:
            del oracle
        if mssql:
            del mssql

    # 通过仓库和SKU进行连接
    rs = pd.merge(e3, iwms, how='outer', left_on=['仓库', 'SKU'], right_on=['仓库', 'SKU'],
                  sort=False, suffixes=['_E3', '_IWMS'])
    # 筛选数量不一致的记录
    rs = rs[(rs['库存数量_E3'] != rs['库存数量_IWMS']) | (rs['可用数量_E3'] != rs['可用数量_IWMS'])]

    # 将结果写入EXCEL
    writer = pd.ExcelWriter(filename)
    rs.to_excel(writer, '对比结果', index=False)
    e3.to_excel(writer, 'E3+库存', index=False)
    iwms.to_excel(writer, 'IWMS库存', index=False)
    writer.save()  # 保存文件

    # 将结果附件通过邮件发送出去
    sendMail.send(mailto_list, 'E3+与IWMS库存对比', None, filelist=[filename])
