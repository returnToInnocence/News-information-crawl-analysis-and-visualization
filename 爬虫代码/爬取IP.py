## coding:gbk
import requests
from lxml import etree
import time


class daili:

    # 1.�������󣬻�ȡ��Ӧ
    def send_request(self, page):
        print("=============����ץȡ��{}ҳ===========".format(page))
        # Ŀ����ҳ�����headers����
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

        # ��������ģ��������������󣬻�ȡ��Ӧ����
        response = requests.get(base_url, headers=headers)
        data = response.content.decode()
        time.sleep(1)

        return data

    # 2.��������
    def parse_data(self, data):

        # ����ת��
        html_data = etree.HTML(data)
        # ��������
        parse_list = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')

        return parse_list

    # 4.������IP
    def check_ip(self, proxies_list):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

        can_use = []
        for proxies in proxies_list:
            try:
                response = requests.get('https://www.baidu.com/', headers=headers, proxies=proxies, timeout=0.1)
                if response.status_code == 200:
                    can_use.append(proxies)

            except Exception as e:
                print(e)

        return can_use

    # 5.���浽�ļ�
    def save(self, can_use):

        file = open('IP.txt', 'w')
        for i in range(len(can_use)):
            s = str(can_use[i]) + '\n'
            file.write(s)
        file.close()

    # ʵ����Ҫ�߼�
    def run(self):
        proxies_list = []
        # ʵ�ַ�ҳ��������ֻ��ȡ����ҳ�������޸�5���ڵ����֣�
        for page in range(1, 5):
            data = self.send_request(page)
            parse_list = self.parse_data(data)
            # 3.��ȡ����
            for tr in parse_list:
                proxies_dict = {}
                http_type = tr.xpath('./td[4]/text()')
                ip_num = tr.xpath('./td[1]/text()')
                port_num = tr.xpath('./td[2]/text()')

                http_type = ' '.join(http_type)
                ip_num = ' '.join(ip_num)
                port_num = ' '.join(port_num)

                proxies_dict[http_type] = ip_num + ":" + port_num

                proxies_list.append(proxies_dict)

        print("��ȡ���Ĵ���IP������", len(proxies_list))

        can_use = self.check_ip(proxies_list)

        print("���õĴ���IP������", len(can_use))
        print("���õĴ���IP:", can_use)

        self.save(can_use)


if __name__ == "__main__":
    dl = daili()
    dl.run()
