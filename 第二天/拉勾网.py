# 打开拉勾网 分析
# 通过搜索栏进行搜索的是动态加载的，通过lable找到的就是静态的了
# https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
from urllib import request,parse


url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
formdata = {
 'first': 'true',
 'pn': 1,
 'kd': 'c++'
}
from fake_useragent import UserAgent
ua = UserAgent().random

# 构造请求头，如果数据没有抓取成功就继续添加请求头中的内容
req_header = {
    'User-Agent':'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=python',
    # 'Cookie': 'WEBTJ-ID=02232019%2C235056-1691b0d6511538-0083ecd868b301-18211c0a-1049088-1691b0d65123c5; _ga=GA1.2.408116959.1550937057; _gat=1; _gid=GA1.2.929568272.1550937057; user_trace_token=20190223235057-cf3ca3fe-3782-11e9-841e-5254005c3644; PRE_HOST=www.baidu.com; LGUID=20190223235057-cf3cab3e-3782-11e9-841e-5254005c3644; LGSID=20190223235101-d1a044ca-3782-11e9-841e-5254005c3644; PRE_UTM=m_cf_cpc_baidu_pc; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.0s0000a7HcV7X_Q0LSwGwFe3HeJnKYv2IHpllvfJK4sFNRTk51NIFCaRcsq0-TON0qXBcnp8dfNp8RI-BhBgkckgfumn_rO54SkbtpLT05sPJhnq5ekUJVsLfTEcueVg7CLOJNCGfR19PQF7t5XXtSuLheqiJU8xTPdCe8wmCy3nagSJhZ3WuGjH6rN3qm9Xt7FOgLqTliIq74nko6.DR_NR2Ar5Od663rj6tJQrGvKD7ZZKNfYYmcgpIQC8xxKfYt_U_DY2yP5Qjo4mTT5QX1BsT8rZoG4XL6mEukmryZZjzL4XNPIIhExztUrzZkdt8A1u9tSMj_qTr1x9tqvZul3xg1sSxW9qx-9LdJN9h9mer5H_z20.U1Yk0ZDqs2v4VnL30ZKGm1Yk0Zfqs2v4VnL30A-V5HcsP0KM5yF-TZns0ZNG5yF9pywd0ZKGujYk0APGujY1rjT0UgfqnH0krNtknjDLg1DsnWPxnH0YP-t1PW0k0AVG5H00TMfqn10L0ANGujYkPjcYg1cknH0zg1c3PHRLg1c3PjDdg1csP1D30AFG5Hfsn-tznjwxnHRd0AdW5HDsnj7xrjDkrHbYP1bzg17xnH0zg100TgKGujYs0Z7Wpyfqn0KzuLw9u1Ys0A7B5HKxn0K-ThTqn0KsTjYs0A4vTjYsQW0snj0snj0s0AdYTjYs0AwbUL0qn0KzpWYs0Aw-IWdsmsKhIjYs0ZKC5H00ULnqn0KBI1Ykn0K8IjYs0ZPl5fK9TdqGuAnqTZnVmvY0IZN15HbvPWf1PHbvn1T1n1c3nHfYn1b0ThNkIjYkPHRsrHnLnjRsnjT10ZPGujY4rj0YuWI-nj0snjR4rAm10AP1UHY4wbu7fRujPDcvn1-jrRc30A7W5HD0TA3qn0KkUgfqn0KkUgnqn0KlIjYs0AdWgvuzUvYqn7tsg1Kxn7ts0Aw9UMNBuNqsUA78pyw15HKxn7tsg1nkrHb1PNts0ZK9I7qhUA7M5H00uAPGujYs0ANYpyfqQHD0mgPsmvnqn0KdTA-8mvnqn0KkUymqn0KhmLNY5H00uMGC5H00uh7Y5H00XMK_Ignqn0K9uAu_myTqnfK_uhnqn0KEm1Yk0APzm1YYnW04P6%26word%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26ck%3D4162.3.86.332.466.336.471.330%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26us%3D1.0.2.0.2.866.0%26bc%3D110101; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_baidu_pc%26m_kw%3Dbaidu_cpc_bj_e110f9_304c7f_%2508%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26bd_vid%3D10608505150305010878; JSESSIONID=ABAAABAAAGGABCB0C31ADE1371E02F9A2A61D47FA435110; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550937058,1550937061,1550937079; LGRID=20190223235721-b45325ac-3783-11e9-b097-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550937442; TG-TRACK-CODE=search_code; SEARCH_ID=1cc71b68a6ff4e8f8f904ce4472e94e4',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Connection': 'keep-alive',
    # 'X-Anit-Forge-Code': '0',
    # 'X-Anit-Forge-Token': 'None',
    # 'X-Requested-With': 'XMLHttpRequest'
}
# 先转表单数据
data_form = parse.urlencode(formdata).encode('utf-8')
# 创建request对象
req = request.Request(url,headers=req_header,data= data_form)
response = request.urlopen(req)
print(response.status)
print(response.read().decode('utf-8'))