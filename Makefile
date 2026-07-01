.PHONY: up down infra dbt-run dbt-test logs clean help

# ── Variables ──────────────────────────────────────────────────
COMPOSE = docker compose
TF_IMAGE = hashicorp/terraform:1.9

# ── Docker Compose ─────────────────────────────────────────────
up:
	$(COMPOSE) up -d --build
	@echo ""
	@echo "  Airflow:  http://localhost:8080  (admin / admin)"
	@echo "  API:      http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:3000"

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f

# ── Terraform via Docker (no local install needed) ─────────────
infra-init:
	docker run --rm -v $(PWD)/infra:/workspace -w /workspace \
	  $(TF_IMAGE) init

infra-plan:
	docker run --rm -v $(PWD)/infra:/workspace -w /workspace \
	  --network portfolio-mundial_default \
	  $(TF_IMAGE) plan

infra-apply:
	docker run --rm -v $(PWD)/infra:/workspace -w /workspace \
	  --network portfolio-mundial_default \
	  $(TF_IMAGE) apply -auto-approve

# ── dbt ────────────────────────────────────────────────────────
dbt-run:
	docker run --rm -v $(PWD)/dbt:/usr/app/dbt -w /usr/app/dbt \
	  --env-file .env \
	  ghcr.io/dbt-labs/dbt-databricks:1.8.0 run

dbt-test:
	docker run --rm -v $(PWD)/dbt:/usr/app/dbt -w /usr/app/dbt \
	  --env-file .env \
	  ghcr.io/dbt-labs/dbt-databricks:1.8.0 test

dbt-docs:
	docker run --rm -v $(PWD)/dbt:/usr/app/dbt -w /usr/app/dbt \
	  --env-file .env \
	  -p 8081:8080 \
	  ghcr.io/dbt-labs/dbt-databricks:1.8.0 docs serve

# ── Misc ───────────────────────────────────────────────────────
clean:
	$(COMPOSE) down -v --remove-orphans
	rm -rf airflow/logs/* dbt/target dbt/dbt_packages .localstack

help:
	@echo "  make up            Levantar todo el stack"
	@echo "  make down          Bajar el stack"
	@echo "  make logs          Ver logs en tiempo real"
	@echo "  make infra-init    Inicializar Terraform"
	@echo "  make infra-apply   Aplicar infraestructura en LocalStack"
	@echo "  make dbt-run       Correr modelos dbt"
	@echo "  make dbt-test      Correr tests de calidad dbt"
	@echo "  make dbt-docs      Servir documentacion dbt en :8081"
	@echo "  make clean         Limpiar todo"
