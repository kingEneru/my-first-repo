import os
import requests
import subprocess


def login_cluster(cluster):
    os.environ['CLUSTER_DOMAIN'] = "prod.infra.webex.com"
    os.environ['CNC_DOMAIN'] = "prod.infra.webex.com"
    os.environ['CNC'] = "mccprod"
    os.environ['VAULT_ADDR'] = "https://east.keeper.cisco.com"
    os.environ['VAULT_NAMESPACE'] = "meetpaas/mccprod"
    os.environ['VAULT_TOKEN'] = vault_token
    result = subprocess.run(f'kubectl wbx3 login {cluster}', capture_output=True, text=True)
    if result.stderr:
        return False
    return True


def check_monitoring_namespace():
    cmd = f'kubectl get pods -n monitoring | grep -E "alertmanager|m-thanos-query|thanos-ruler"'
    output = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    print('----------------------------------Monitoring status----------------------------------------')
    print(output)
    print('----------------------------------End----------------------------------------')


def check_prometheus(kube_cluster, cookie, split_prom_version):
    url = f'https://prometheus.int.{kube_cluster}.prod.infra.webex.com/api/v1/query'
    data = {
        'query': "helm_chart_info{release='split-prometheus'}",
        'engine': 'prometheus'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }
    res = requests.post(url, params=data, headers=headers)
    if res.status_code != 200:
        print('Error! prometheus query function exception')
    else:
        result = res.json().get('data').get('result')
        if len(result) == 0:
            print(f'Warning! {kube_cluster} cluster missing helm_chart_info metrics, please have a look')
        elif result[0]['metric']['version'] != split_prom_version:
            print(f'Warning! split-prometheus currently version is {result[0]["metric"]["version"]}, not match specify release {split_prom_version}, please check!')
        else:
            print('\n**************************************************************************')
            print(f'Normal! {kube_cluster} cluster prometheus release conforms to the standard')
            print('***************************************************************************\n')


def check_url(cluster, url):
    try:
        print(f'Check {url } beginning')
        res = requests.get(url)
        if res.status_code != 200:
            print(f'{cluster} cluster has exception, please check {url}\n')
    except Exception as e:
        print(f'{cluster} cluster has exception, please check url: {url} (error:{e})\n')
    print(f'{url} check end,there is no exception~\n')


if __name__ == '__main__':
    cluster_list = ['wdfwmw-j-1']
    split_prometheus_release = '1.0.11'
    prometheus_cookie = 'abcdefg'
    vault_token = 'abcdefg'

    for cluster in cluster_list:
        # login cluster
        if not login_cluster(cluster):
            print(f'Login {cluster} cluster failed..')
            continue
        print(f'Currently cluster : {cluster}')

        # Show app/plat-prometheus namespace pods status
        print('----------------------------------Prometheus Status----------------------------------------')
        namespaces = ['app-prometheus', 'plat-prometheus']
        for ns in namespaces:
            cmd = f'kubectl get pods -n {ns}'
            output = subprocess.run(cmd, capture_output=True, text=True).stdout
            print(output)

        # Show monitoring namespace pods status
        print('----------------------------------Monitoring Status----------------------------------------')
        powershell_cmd = f'kubectl get pods -n monitoring | grep -E "alertmanager|m-thanos-query|thanos-ruler"'
        cmd = ['powershell', '-Command', powershell_cmd]
        print(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
        print('---------------------------------------End-------------------------------------------------')

        # Check prometheus and version query function
        check_prometheus(cluster, prometheus_cookie, split_prometheus_release)

        # Check monitoring stack urls
        thanos_query_url = f'https://prometheus.int.{cluster}.prod.infra.webex.com/targets'
        thanos_ruler_url = f'https://thanos-ruler.int.{cluster}.prod.infra.webex.com/alerts'
        alertmanager_url = f'https://prometheusalerts.int.{cluster}.prod.infra.webex.com/#/alerts'
        # print(thanos_query_url, '\n', thanos_ruler_url, '\n', alertmanager_url,'\n')
        [check_url(cluster, url) for url in [thanos_query_url, thanos_ruler_url, alertmanager_url]]
