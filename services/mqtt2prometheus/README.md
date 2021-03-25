to run exporter: docker run -it -v "$(pwd)/config.yaml:/config.yaml"  -p  9641:9641 ghcr.io/hikhvar/mqtt2prometheus:latest 

source: https://github.com/hikhvar/mqtt2prometheus

1. start prometheus
2. change mqtt2prometheus config.yaml file
- server should be PI_IP_ADDRESS:1883
- topic path should be same topic path in HA
3. start exporter
4. send test data from MQTT/HA integration
5. go to PI_IP_ADDRESS:9641/metrics for metrics

