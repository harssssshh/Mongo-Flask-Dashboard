# Introduction to Prometheus Exporters

Prometheus is an open-source monitoring and alerting toolkit designed to monitor systems and generate alerts based on defined thresholds. Prometheus exporters are utilities that collect metrics from various systems and expose them in a format that Prometheus can ingest and analyze.

Prometheus exporters facilitate monitoring by extracting specific metrics from various software systems, making it easy to monitor their performance, health, and other key parameters.

## WMI Exporter

**Windows Management Instrumentation (WMI) Exporter** is a Prometheus exporter designed to collect metrics from Windows systems. It utilizes WMI, which is a management infrastructure provided in Windows operating systems. The WMI Exporter allows users to monitor various aspects of a Windows system, such as CPU usage, memory utilization, disk activity, and network statistics.

To use the WMI Exporter, you configure it to collect specific WMI metrics and expose them in a format compatible with Prometheus.

## Nginx Exporter

The **Nginx Exporter** is used to collect metrics from Nginx web servers. Nginx is a popular open-source web server known for its high performance, stability, and extensive feature set. The Nginx Exporter helps monitor key Nginx metrics like request rate, connection statistics, error rates, and more.

By using the Nginx Exporter, Prometheus can scrape and store Nginx metrics, allowing operators to gain insights into the performance and health of their Nginx web servers.

## MySQL Exporter

The **MySQL Exporter** enables the collection of metrics from MySQL databases. MySQL is a widely used open-source relational database management system known for its reliability, scalability, and ease of use. The MySQL Exporter gathers critical MySQL metrics such as query performance, connection statistics, cache usage, and more.

Integrating the MySQL Exporter with Prometheus allows operators to monitor and analyze the performance of MySQL databases, helping in proactive maintenance and performance optimization.

These exporters are essential tools for effectively monitoring Windows systems (WMI Exporter), Nginx web servers (Nginx Exporter), and MySQL databases (MySQL Exporter) within an ecosystem. By utilizing Prometheus and these exporters, operators can ensure the reliability, performance, and health of their systems and applications.



## Steps to Install WMI Exporter

### Disable Defender in IIS:

1. Search for Server Manager > Local Server > Real-Time Protection Off



### Disable Windows Firewall / Defender
Open the Control Panel on your Windows server.
Navigate to "System and Security" and then "Windows Defender Firewall."
Click on "Turn Windows Defender Firewall on or off" from the left sidebar.
Select the "Turn off Windows Defender Firewall" option for both private and public networks.
Click "OK" to save the settings.
Disable Windows Defender:

### Install WMI Exporter from WMI Release Page:

1. Go to the WMI Exporter GitHub release page to download the latest [Release](https://github.com/prometheus-community/windows_exporter/releases).
2. Download the appropriate version of the exporter for your operating system (e.g., wmi_exporter-<version>.windows-amd64.zip for Windows).

3. Extract the downloaded ZIP file to a directory of your choice.

4. Go into directory & execute the file.

5. By Default, WMI Exporter runs on Port 9182 

6. In order for it to be scraped by Prometheus, we need to open Port 9182

4. Expose Port Number 9182 in Security Group in AWS:

### Sign in to the AWS Management Console.

1.  Navigate to the EC2 dashboard and click on "Security Groups" in the left sidebar.
2.  Select the security group associated with your Windows server instance.
3.  Click on the "Inbound rules" tab and then click "Edit inbound rules."
4.  Add a rule to allow inbound traffic on port 9182 (the default port for WMI Exporter) by specifying the port (9182) and the source (e.g., your IP address or a custom range).


### Registering the target in `prometheus.yaml`
```
global:
  scrape_interval: 15s  # Scrape targets every 15 seconds.

scrape_configs:
  - job_name: 'wmi_exporter'
    static_configs:
      - targets: ['windows_machine_ip:9182']
```

Replace windows_machine_ip with the public IP of Windows Server

Here's a quick break down of the configuration :- 
1. job_name: This is a label for this particular job. We're calling it 'wmi_exporter' in this example.
2. static_configs: This specifies a list of static targets to scrape.
3. targets: This is an array of targets in the format address:port. In this case, it's the IP address of the Windows machine and port 9182 where the WMI Exporter is running.


## Steps to cross-check in Prometheus
1. Check if target is up & running state.

2. Check metrics exposed by WMI Exporter

3.  In order to visualize the metrics collected by Prometheus, Use this [Dashboard](https://grafana.com/grafana/dashboards/14694-windows-exporter-dashboard/) available in the list of dashboards from Grafana Marketplace. 

4. Import this dashboard and you'll be able to see the metrics exported by WMI Exprter.




# Steps to install MySQL Exporter.

1. Go into `exporter/mysql-exporter` directory. 
2. Run `kubectl apply -f .`
3. It'll create MySQL Deployment & MySQL Exporter with associated services as well.
4. Configure prometheus.yaml to include mysql-exporter target.
5. Add one more target in `prometheus.yaml`
```
- job_name: 'mysql'
    scrape_interval: 5s
    static_configs:
      - targets: ['mysql_exporter.ns.svc.cluster.local:9104']
```


#### Replace mysql_exporter.ns.svc.cluster.local with the appropriate service name and namespace.



## All  Exporters can be installed the same way as above ! Now, let's get some hands-on and practical implementation of exporters.


# Steps to Deploy MongoDB-Flask-Dashboard Application 

1. Clone this [Github Repository](https://github.com/harssssshh/Mongo-Flask-Dashboard)
2. 3. Go into `MongoDB Flask Dashboard` directory
3. Switch to monitoring branch using `git switch monitoring`.
4. Go into `eks-deployments` directory.
5. Go through each of these manifests thoroughly and keep applying the manifests.
6. Apply manifests in directory `kubectl apply -f .`
7. ## IMPORTANT :- After applying each of those manifests, update prometheus.yaml with appropriate exporter URL's. For eg:-
Nginx Exporter URL will be `nginx-exporter.dashboard.svc.cluster.local:9113`
MongoDB Exporter URL  will be `mongodb-exporter.dashboard.svc.cluster.local:9216`


