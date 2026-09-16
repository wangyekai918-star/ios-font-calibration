def row(name, old, new, note, **extra):
    return dict(name=name, old=old, new=new, note=note, **extra)


modules = [
    dict(key='profile-assets', title='账户资产', old='19811:270182', new='19811:270222', height=186,
         subtitle='余额、卡券、金豆和积分的名称加大一号',
         rows=[row('资产名称',12,13,'「可用余额」「卡券」「金豆」「积分」同步调整；只圈「积分」一个代表。')],
         marks=[dict(label='资产名称',indices=[9],widths=[24,26],x_offsets=[31.875,30.875],old=12,new=13,route='right',ly=104)],
         note='资产数字、余额小数、临期提示和「兑好礼」维持原字号；资产名称文字色仍为 #414345。'),
    dict(key='profile-common', title='常用功能', old='19811:270305', new='19811:270332', height=210,
         subtitle='入口名称加大一号，文字色由 #6F7173 调整为 #414345',
         rows=[row('功能入口名称',12,13,'「我的订单」「开发票」「我的收藏」「最近充电」的字号与文字色同步调整；只圈「最近充电」一个代表。',colors={'old':'#6F7173','new':'#414345'})],
         marks=[dict(label='功能入口名称',indices=[3],widths=[48,52],x_offsets=[19.875,17.875],old=12,new=13,route='right',ly=96,colors={'old':'#6F7173','new':'#414345'})],
         note='四个入口名称均需同时调整字号和文字色；文字不透明度均为 100%。'),
    dict(key='profile-benefits', title='福利活动', old='19811:270359', new='19811:270408', height=225,
         subtitle='右侧两个活动标题加大一号',
         rows=[row('活动标题',12,13,'「认证营运车」「邀好友赚红包」同步调整；只圈上方标题一个代表。')],
         marks=[dict(label='活动标题',indices=[0],old=12,new=13,route='right',ly=78)],
         note='右侧活动副标题仍为 11，标题文字色仍为 #141517；左侧签到图形素材保持原样。'),
    dict(key='profile-private', title='个人桩', old='19923:270457', new='19923:270488', height=176,
         subtitle='我的桩、收到的预约和故障报修加大一号',
         rows=[row('个人桩功能名称',12,13,'三个入口名称同步调整；只圈「故障报修」一个代表。')],
         marks=[dict(label='功能入口名称',indices=[3],widths=[48,52],x_offsets=[19.875,17.875],old=12,new=13,route='right',ly=103)],
         note='左侧「个人桩」标题仍为 15；功能名称文字色仍为 #141517。'),
    dict(key='profile-more', title='更多功能', old='19923:270519', new='19923:270602', height=308,
         subtitle='全部功能入口名称加大一号',
         rows=[row('功能入口名称',12,13,'即插即充、月账单、充电设置、V2G、电池长效守护、行程规划、我的预约、我的评价、申请建桩、更多服务同步调整；只圈「更多服务」一个代表。')],
         marks=[dict(label='功能入口名称',indices=[9],widths=[48,52],x_offsets=[19.875,17.875],old=12,new=13,route='right',ly=243)],
         note='十个功能名称采用相同字号，文字色仍为 #141517。'),
]

for number, mark in enumerate((mark for module in modules for mark in module['marks']), 1):
    mark['number'] = f'{number:02}'
