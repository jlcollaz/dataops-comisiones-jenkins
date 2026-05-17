# Diagrama del flujo DataOps

```text
GitHub Repository
      |
      | Push / Commit
      v
GitHub Webhook
      |
      v
Jenkins Pipeline
      |
      | 1. Checkout
      | 2. Docker Build
      | 3. Docker Run
      | 4. Validación del output
      v
Artefacto final: output/comisiones_calculadas.xlsx
```
