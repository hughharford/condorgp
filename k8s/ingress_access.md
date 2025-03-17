# Accessing Services via Ingress

## Browser Access

With the ingress configuration, you can access the services through your browser:

1. Grafana:
   ```
   http://cgp.local/grafana
   ```
   Default credentials: admin/admin

2. RabbitMQ Management Interface:
   ```
   http://cgp.local/rabbitmq
   ```
   Default credentials from secrets: guest/guest

3. Worker Interface:
   ```
   http://cgp.local/worker
   ```

## Code/Application Access

For applications within the cluster:
- Use the internal Kubernetes DNS names:
  ```python
  # RabbitMQ AMQP connection
  rabbitmq_url = "amqp://guest:guest@cgp-rabbitmq:5672/"
  
  # Grafana API
  grafana_url = "http://cgp-grafana:3000/api/v1/..."
  
  # Worker API
  worker_url = "http://cgp-worker-1:2727/..."
  ```

For applications outside the cluster:
- Using ingress host:
  ```python
  # RabbitMQ Management API
  rabbitmq_api_url = "http://cgp.local/rabbitmq/api/"
  
  # Grafana API
  grafana_api_url = "http://cgp.local/grafana/api/v1/..."
  
  # Worker API
  worker_api_url = "http://cgp.local/worker/..."
  ```

## Important Notes

1. DNS Setup:
   - Add to your `/etc/hosts` file:
     ```
     127.0.0.1    cgp.local
     ```

2. RabbitMQ Connections:
   - AMQP connections (port 5672) should use the direct service name `cgp-rabbitmq`
   - Only the management interface (port 15672) is available through ingress

3. Production Setup:
   - Use the TLS-enabled configuration with `cgp.example.com`
   - Replace with your actual domain
   - URLs would use `https://` instead of `http://`
   - TLS configuration is in `tls-config.yaml`

## Testing Connectivity

Using curl:

```bash
curl -k https://cgp.example.com/rabbitmq
```

```bash
curl -k https://cgp.example.com/grafana
```

```bash
curl -k https://cgp.example.com/worker
```

```bash
Test Grafana
curl http://cgp.local/grafana/api/health
```

```bash
Test RabbitMQ Management API
curl -u guest:guest http://cgp.local/rabbitmq/api/overview
```

```bash
Test Worker API
curl http://cgp.local/worker/status # Adjust endpoint based on your worker API


Using Python requests:

```python
import requests

# Grafana health check
response = requests.get('http://cgp.local/grafana/api/health')
print(response.json())

# RabbitMQ management API
auth = ('guest', 'guest')
response = requests.get('http://cgp.local/rabbitmq/api/overview', auth=auth)
print(response.json())

# Worker API
response = requests.get('http://cgp.local/worker/status')  # Adjust endpoint based on your worker API
print(response.json())
```

## Troubleshooting

1. Check ingress status:
   ```bash
   source k8s/ingress-commands.sh
   check_ingress
   ```

2. Verify ingress controller:
   ```bash
   check_controller
   ```

3. Common issues:
   - DNS resolution: Ensure `/etc/hosts` is properly configured
   - TLS certificates: Use `create_tls_secret` command for production setup
   - Service connectivity: Check if services are running with `kubectl get services -n cgp-system`

## Additional Resources

- Setup scripts:
  - `setup-ingress.sh`: Install and configure ingress controller
  - `ingress-commands.sh`: Utility commands for managing ingress
- Configuration files:
  - `ingress.yaml`: HTTP ingress configuration
  - `tls-config.yaml`: HTTPS/TLS ingress configuration
