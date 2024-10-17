#!/usr/bin/env python3
# encoding: utf-8
from __future__ import annotations

import os
import json

from workflow import Workflow3, MATCH_SUBSTRING

def main(wf: Workflow3):
    try:
        # 获取配置
        host_group_conf = os.environ.get('hosts')

        # 解析配置
        if host_group_conf:
            all_host_group = json.loads(host_group_conf)
        else:
            all_host_group = []

        # 创建查询
        query = None
        if len(wf.args):
            query = wf.args[0]

        # 过滤查询
        host_groups = wf.filter(query, all_host_group, filter_for_host_group, match_on=MATCH_SUBSTRING)

        # 空结果
        if not host_groups:
            wf.add_item('No host group matches')

        # 排序
        host_groups.sort(key=sort_for_profile)

        # 添加主机组选项
        for group in host_groups:

            # 拼接标题
            title = group['name'] + ' - ' + ', '.join(map(str, group['tag']))

            # 拼接子标题
            host_size = len(group['host'])
            subtitle = '× ' + str(host_size)

            # 拼接主机
            host_str = ','.join(map(str, group['host']))

            # 拼接参数
            delimiter = '_&_'
            arg = title + delimiter + group['command'] + delimiter + host_str

            # 构建选项
            wf.add_item(title=title,
                        subtitle=subtitle,
                        arg=arg,
                        valid=True,
                        icon=group['icon'])

        # 反馈结果
        wf.send_feedback()

    except Exception as e:
        # 异常
        wf.logger.exception(e)
        raise


# 过滤
def filter_for_host_group(group):
    return group['name'] + ' ' + str(group['tag'])

# 排序
def sort_for_profile(group):
    return group['name']


if __name__ == "__main__":
    # 创建 Alfred 工作流对象
    wf = Workflow3()

    # 记录日志
    wf.logger.info(__name__)

    # 运行主函数
    wf.run(main)
