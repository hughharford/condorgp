# TLS Setup Guide for Kubernetes Ingress

## What is TLS?
Transport Layer Security (TLS) provides secure communication between clients and your services. When you access a website using `https://`, you're using TLS.

## Prerequisites
Before setting up TLS, you need:
1. A domain name (e.g., cgp.example.com)
2. SSL/TLS certificates for your domain
3. Kubernetes cluster with ingress-nginx controller installed

## Getting SSL/TLS Certificates

### Option 1: Using Self-Signed Certificates (Development Only)
```bash
# Generate private key
openssl genrsa -out tls.key 2048

# Generate self-signed certificate
openssl req -x509 -new -nodes \
  -key tls.key \
  -sha256 \
  -days 365 \
  -out tls.crt \
  -subj "/CN=cgp.example.com"
```

### Option 2: Using Let's Encrypt (Production)
For production, use Let's Encrypt to get free, trusted certificates. This requires:
1. Public domain name
2. DNS records pointing to your cluster
3. cert-manager installed in your cluster

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

## Creating TLS Secret in Kubernetes

### Manual Method (Using existing certificates)
```bash
# Using the create_tls_secret function from ingress-commands.sh
source k8s/ingress-commands.sh
create_tls_secret /path/to/tls.key /path/to/tls.crt
```

This command creates a Kubernetes secret containing your TLS certificate and private key. Under the hood, it runs:
```bash
kubectl create secret tls cgp-tls-secret \
  --key /path/to/tls.key \
  --cert /path/to/tls.crt \
  -n cgp-system
```

### Automatic Method (Using cert-manager)
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cgp-cert
  namespace: cgp-system
spec:
  secretName: cgp-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - cgp.example.com
```

## Verifying TLS Setup

1. Check secret creation:
```bash
kubectl get secret cgp-tls-secret -n cgp-system
```

2. Test HTTPS connection:
```bash
curl -v -k https://cgp.example.com/grafana
```
Note: `-k` flag skips certificate verification (useful for self-signed certs)

## Common Issues

1. Certificate Errors
   ```bash
   # Check certificate details
   openssl x509 -in tls.crt -text -noout
   ```

2. Secret Issues
   ```bash
   # Verify secret contents
   kubectl get secret cgp-tls-secret -n cgp-system -o yaml
   ```

3. Ingress TLS Configuration
   ```bash
   # Check ingress status
   kubectl describe ingress cgp-ingress-tls -n cgp-system
   ```

## Security Best Practices

1. Never commit certificates or private keys to version control
2. Use appropriate file permissions:
   ```bash
   chmod 600 tls.key
   chmod 644 tls.crt
   ```

3. Rotate certificates regularly:
   - Let's Encrypt certificates expire after 90 days
   - Self-signed certificates as specified (365 days in example)

4. Use production-grade certificates for production environments
   - Never use self-signed certificates in production
   - Use Let's Encrypt or commercial certificate providers

## Testing TLS Configuration

1. Browser Test:
   - Open https://cgp.example.com/grafana
   - Check certificate information in browser

2. Command Line Test:
   ```bash
   # Test with curl
   curl -v https://cgp.example.com/grafana

   # Test TLS handshake
   openssl s_client -connect cgp.example.com:443 -servername cgp.example.com
   ```

## Additional Resources

- [Kubernetes TLS Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/) 