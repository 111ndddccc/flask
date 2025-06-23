import clr
clr.AddReference("System")
clr.AddReference("System.Data")
clr.AddReference("Kingdee.BOS")
clr.AddReference("Kingdee.BOS.App")
clr.AddReference("Kingdee.BOS.Core")

from System import Decimal
from Kingdee.BOS.App.Data import DBUtils

def AfterExecuteOperationTransaction(e):
    CheckGroupTotal()

def CheckGroupTotal():
    entry_data = this.View.Model.DataObject["FEntity"]
    group_map = {}

    for row in entry_data:
        group = row["FGROUP"]
        rate = row["FZXWLTDBL"]

        # 跳过无效数据
        if group is None or rate is None:
            continue

        group_key = str(group)
        if group_key not in group_map:
            group_map[group_key] = 0

        group_map[group_key] += float(rate)

    invalid_groups = []
    for group, total in group_map.items():
        if abs(total - 1.0) > 0.0001:
            invalid_groups.append("组 %s 合计为 %.4f" % (group, total))

    if invalid_groups:
        raise Exception("【校验失败】以下分组 FZXWLTDBL 合计不为 1，请修改：\n" + "\n".join(invalid_groups))
