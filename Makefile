.PHONY: build run instance start stop ssh-config erase

## run
run:
	docker run -it --rm -p 8080:8080 --env-file .env \
	-v $(PWD)/src:/app/src \
	-v ~/.config:/root/.config \
	only-once-translator
	# poetry run python src/app.py

## build
build:
	docker build -t only-once-translator .

## make instance
instance:
	gcloud compute instances create ${INSTANCE_NAME} \
	--zone=${ZONE} \
	--image-family=debian-10 \
    --image-project=debian-cloud \
	--boot-disk-type="pd-standard" \
	--boot-disk-size="40GB" \
	--machine-type="n2-standard-4" \
	--network="outbound-internet" \
	--subnet="subnet1" \
	--labels="stop_if_not_active=false"

## erase
erase:
	gcloud compute instances delete ${INSTANCE_NAME} \
	--zone=${ZONE}

## start
start:
	gcloud compute instances start --zone=${ZONE} ${INSTANCE_NAME}

## stop
stop:
	gcloud compute instances stop --zone=${ZONE} ${INSTANCE_NAME}

## ssh config
ssh-config:
	gcloud compute config-ssh

## scp
scp:
	gcloud compute scp --zone=${ZONE} --recurse $(shell pwd) ${INSTANCE_NAME}:~/only-once-translator

## cp
cp:
	gcloud compute copy-files --zone=${ZONE} $(shell pwd) ${INSTANCE_NAME}:~/only-once-translator

## echo
echo:
	@echo $(shell pwd)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

