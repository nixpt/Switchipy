# Switchipy Makefile

.PHONY: help install uninstall test run clean docs cli demo

help: ## Show this help message
	@echo "Switchipy Development Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Switchipy to system
	@echo "Installing Switchipy..."
	python3 scripts/install.py

uninstall: ## Uninstall Switchipy from system
	@echo "Uninstalling Switchipy..."
	python3 scripts/uninstall.py

install-deps: ## Install system dependencies
	@echo "Installing system dependencies..."
	@if command -v pacman >/dev/null 2>&1; then \
		echo "Arch/Manjaro detected. Installing with pacman..."; \
		sudo pacman -S xfconf zenity; \
	elif command -v apt >/dev/null 2>&1; then \
		echo "Ubuntu/Debian detected. Installing with apt..."; \
		sudo apt install xfconf zenity; \
	else \
		echo "Please install xfconf and zenity manually"; \
	fi

test: ## Run test suite
	@echo "Running tests..."
	python3 test_runner.py

test-verbose: ## Run tests with verbose output
	@echo "Running tests with verbose output..."
	python3 -m unittest tests.test_all -v

run: ## Run the GUI application
	@echo "Starting Switchipy GUI..."
	python3 app.py

cli: ## Show CLI help
	@echo "Switchipy CLI Commands:"
	@echo "======================"
	python3 switchipy_cli.py --help

cli-current: ## Show current theme via CLI
	@echo "Current theme status:"
	python3 switchipy_cli.py current

cli-list: ## List available themes via CLI
	@echo "Available themes:"
	python3 switchipy_cli.py list

cli-toggle: ## Toggle theme via CLI
	@echo "Toggling theme..."
	python3 switchipy_cli.py toggle

docs: ## Generate documentation
	@echo "Documentation is available in docs/ directory"
	@echo "API Documentation: docs/API.md"
	@echo "Development Guide: docs/DEVELOPMENT.md"
	@echo "CLI Documentation: docs/CLI.md"
	@echo "Installation Guide: docs/INSTALLATION.md"
	@echo "Icons Documentation: docs/ICONS.md"

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -rf switchipy/__pycache__/
	rm -rf .pytest_cache/
	rm -f /tmp/switchipy_icon.png
	find . -name "*.pyc" -delete

setup: ## Initial setup
	@echo "Setting up Switchipy..."
	chmod +x scripts/*.sh
	chmod +x tests/*.py
	chmod +x test_runner.py
	chmod +x switchipy_cli.py
	@echo "Setup complete!"

package: ## Create distribution package
	@echo "Creating package..."
	@mkdir -p dist
	@tar -czf dist/switchipy-$(shell date +%Y%m%d).tar.gz \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		--exclude='dist' \
		--exclude='.idea' \
		.
	@echo "Package created: dist/switchipy-$(shell date +%Y%m%d).tar.gz"

demo: ## Run CLI demo
	@echo "Switchipy CLI Demo"
	@echo "=================="
	@echo "1. Current theme:"
	@python3 switchipy_cli.py current
	@echo ""
	@echo "2. Available themes (first 5):"
	@python3 switchipy_cli.py list | head -20
	@echo ""
	@echo "3. Configuration:"
	@python3 switchipy_cli.py config

# Icon management targets
test-icons: ## Test icon generation and themes
	@echo "Testing icon generation..."
	python3 examples/test_icons.py

clear-icons: ## Clear icon cache
	@echo "Clearing icon cache..."
	python3 -c "from switchipy.icons import clear_icon_cache; clear_icon_cache()"

icon-gallery: ## Create icon gallery
	@echo "Creating icon gallery..."
	python3 examples/test_icons.py

# Enhanced development targets
dev-setup: ## Complete development setup
	@echo "Setting up development environment..."
	make setup
	make install-deps
	pip install --user --break-system-packages pytest flake8 black

format-code: ## Format code with black
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		python3 -m black .; \
	else \
		echo "black not available, install with: pip install black"; \
	fi

lint-code: ## Lint code with flake8
	@echo "Linting code..."
	@if command -v flake8 >/dev/null 2>&1; then \
		python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
	else \
		echo "flake8 not available, install with: pip install flake8"; \
	fi

coverage: ## Run tests with coverage
	@echo "Running tests with coverage..."
	@if command -v pytest >/dev/null 2>&1; then \
		python3 -m pytest --cov=switchipy --cov-report=html --cov-report=term; \
	else \
		echo "pytest not available, install with: pip install pytest pytest-cov"; \
	fi

all: setup install test ## Run setup, install, and test

# Improvement testing targets
test-improvements: ## Test all improvement modules
	@echo "Testing improvement modules..."
	python3 examples/implement_improvements.py

test-logging: ## Test enhanced logging system
	@echo "Testing logging system..."
	python3 -c "from switchipy.logging_config import logger; logger.info('Test message')"

test-config: ## Test enhanced configuration system
	@echo "Testing configuration system..."
	python3 -c "from switchipy.config_enhanced import load_config; print('Config loaded:', len(load_config()), 'keys')"

test-performance: ## Test performance monitoring
	@echo "Testing performance monitoring..."
	python3 -c "from switchipy.performance import get_performance_summary; print('Performance:', get_performance_summary())"

test-ux: ## Test user experience enhancements
	@echo "Testing UX enhancements..."
	python3 -c "from switchipy.ux_enhancements import show_notification; show_notification('Test', 'UX test', 'switchipy')"

# Development improvement targets
improve-setup: ## Set up improvement development environment
	@echo "Setting up improvement development..."
	pip install --user --break-system-packages psutil
	@echo "Improvement modules ready!"

improve-demo: ## Run improvement demonstration
	@echo "Running improvement demonstration..."
	make test-improvements

