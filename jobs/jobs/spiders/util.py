# -*- coding:utf-8 -*-
import re


def CompanyScale(text):
    group = re.match(r'(\d+)-(\d+)人', text, re.M | re.I)
    if group is not None:
        return group.group(1), group.group(2)
    group = re.match(r'少于(\d+)人', text, re.M | re.I)
    if group is not None:
        return 0, group.group(1)
    group = re.match(r'(\d+)人以上', text, re.M | re.I)
    if group is not None:
        return group.group(1), 0
    return 0, 0


if __name__ == '__main__':
    # CompanyScale('500-1000人')
    g1, g2 = CompanyScale('少于50人')
    print(g1, g2)
