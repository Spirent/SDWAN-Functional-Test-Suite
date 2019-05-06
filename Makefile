ATSENV_SUBDIR = pkg/atsenv

.PHONY: all test upgrade

all: $(ATSENV_SUBDIR)

$(ATSENV_SUBDIR):
	@echo "===> Creating python virtual env: $(ATSENV_SUBDIR)"
	@python3 -m venv $(ATSENV_SUBDIR)
	@curl -s https://bootstrap.pypa.io/get-pip.py -o - | $(ATSENV_SUBDIR)/bin/python > /dev/null
	@$(ATSENV_SUBDIR)/bin/pip install --timeout 50 -r requirements.txt > /dev/null

upgrade:
	@echo "===> Installing available upgrades into $(ATSENV_SUBDIR)"
	@$(ATSENV_SUBDIR)/bin/pip install pip -U > /dev/null
	@$(ATSENV_SUBDIR)/bin/pip install --upgrade -r requirements.txt > /dev/null

test:
	@echo "===> Running tests"
	$(ATSENV_SUBDIR)/bin/python -m unittest test.test_stcsession -v

clean: 
	@echo "===> Cleaning python virtual env: $(ATSENV_SUBDIR)"
	@rm -rf $(ATSENV_SUBDIR)
