.PHONY: ags-validate ags-validate-min ags-registry ags-next-id ags-fix-todos ags-change-report

ags-validate:
	python3 scripts/validate_ags.py --profile strict --check-registry --check-drift

ags-validate-min:
	python3 scripts/validate_ags.py --profile minimal --check-registry

ags-registry:
	python3 scripts/validate_ags.py --profile strict --write-registry

ags-next-id:
	python3 scripts/validate_ags.py --next-id gov

ags-fix-todos:
	python3 scripts/validate_ags.py --fix-todo-ids

ags-change-report:
	python3 scripts/validate_ags.py --change-report
