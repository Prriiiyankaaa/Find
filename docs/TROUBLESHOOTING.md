# Common Setup Troubleshooting Guide

This guide helps contributors resolve common local development and environment setup issues before working on the project.

It is intended for onboarding and contributor workflow troubleshooting only.

For ML-specific debugging and inference troubleshooting, refer to:

- [Real ML Troubleshooting Guide](./REAL_ML_TROUBLESHOOTING.md)

---

# Node.js and pnpm Issues

## `pnpm: command not found`

Install pnpm globally:

```bash
npm install -g pnpm
```

Verify installation:

```bash
pnpm -v
```

---

## Node.js version mismatch

This project requires Node.js 18+.

Check your installed version:

```bash
node -v
```

If needed, install/update Node.js from:

- https://nodejs.org/

---

# Python and uv Issues

## `uv: command not found`

Install uv:

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

---

## Python version issues

Verify Python version:

```bash
python --version
```

The project expects Python 3.12+.

---

# Docker Issues

## Docker daemon not running

Ensure Docker Desktop or Docker Engine is running before starting containers.

Verify Docker status:

```bash
docker ps
```

Start the stack:

```bash
docker compose up --build
```

---

## Docker permission denied

On Linux systems, Docker may require elevated permissions.

Temporary workaround:

```bash
sudo docker compose up --build
```

Optional permanent fix:

```bash
sudo usermod -aG docker $USER
```

Log out and log back in after applying the group change.

---

# Service and Port Issues

## Port already in use

Some ports such as `3000`, `8000`, `6379`, `9200`, or `9201` may already be occupied.

Check active ports:

```bash
netstat -ano
```

Stop conflicting services or change the port mappings if required.

---

## Redis connection issues

Verify running services:

```bash
docker compose ps
```

Restart containers if needed:

```bash
docker compose restart
```

---

## MinIO service unavailable

Ensure MinIO containers are running correctly:

```bash
docker compose ps
```

Expected ports:

- MinIO API: `9200`
- MinIO Console: `9201`

---

# Contributor Notes

- Use the light Docker stack for routine contributor work:

```bash
docker compose -f docker-compose.light.yml up --build
```

- Avoid using the full ML stack unless testing real inference workflows.
- Review the main README and CONTRIBUTING guide before opening issues or pull requests.