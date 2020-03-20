
# default to TRADE DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

PYLINKVALIDATE_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="\
	$${DOMESTIC_URL}international/static/,\
	$${DOMESTIC_URL}find-a-buyer/static/,\
	$${DOMESTIC_URL}profile/static/,\
	$${DOMESTIC_URL}profile/enrol/?next=,\
	$${DOMESTIC_URL}sso/accounts/login/?next,\
	$${DOMESTIC_URL}sso/accounts/password/reset/?next,\
	$${DOMESTIC_URL}sso/accounts/signup/?next,\
	$${DOMESTIC_URL}sso/static/,\
	$${DOMESTIC_URL}static/,\
	$${DOMESTIC_URL}international/trade/search/?term=,\
	$${DOMESTIC_URL}international/trade/static/,\
	$${DOMESTIC_URL}international/trade/suppliers/,\
	$${DOMESTIC_URL}international/invest/static/,\
	$${DOMESTIC_URL}international/investment-support-directory/0,\
	$${DOMESTIC_URL}international/investment-support-directory/O,\
	$${DOMESTIC_URL}international/investment-support-directory/S,\
	$${DOMESTIC_URL}international/investment-support-directory/search/?,\
	$${DOMESTIC_URL}international/investment-support-directory/?q=,\
	$${DOMESTIC_URL}selling-online-overseas/static/,\
	$${DOMESTIC_URL}contact/selling-online-overseas/static/,\
	$${DOMESTIC_URL}export-opportunities/opportunities?,\
	$${DOMESTIC_URL}export-opportunities/opportunities/a,\
	$${DOMESTIC_URL}export-opportunities/opportunities/b,\
	$${DOMESTIC_URL}export-opportunities/opportunities/c,\
	$${DOMESTIC_URL}export-opportunities/opportunities/d,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/f,\
	$${DOMESTIC_URL}export-opportunities/opportunities/g,\
	$${DOMESTIC_URL}export-opportunities/opportunities/h,\
	$${DOMESTIC_URL}export-opportunities/opportunities/j,\
	$${DOMESTIC_URL}export-opportunities/opportunities/k,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/n,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/p,\
	$${DOMESTIC_URL}export-opportunities/opportunities/r,\
	$${DOMESTIC_URL}export-opportunities/opportunities/s,\
	$${DOMESTIC_URL}export-opportunities/opportunities/t,\
	$${DOMESTIC_URL}export-opportunities/opportunities/w,\
	$${DOMESTIC_URL}export-opportunities/opportunities/z,\
	$${DOMESTIC_URL}export-opportunities/opportunities?s=,\
	$${DOMESTIC_URL}export-opportunities/opportunities?paged=,\
	$${DOMESTIC_URL}export-opportunities/assets/,\
	http://www.linkedin.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.facebook.com,\
	https://www.facebook.com/login.php,\
	https://www.linkedin.com\
	" && \
	export TEST_URLS="\
	$${DOMESTIC_URL} \
	$${DOMESTIC_URL}advice/ \
	$${DOMESTIC_URL}markets/ \
	$${DOMESTIC_URL}services/ \
	$${DOMESTIC_URL}community/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/markets/results/ \
	$${DOMESTIC_URL}export-opportunities/ \
	$${DOMESTIC_URL}export-opportunities/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	$${DOMESTIC_URL}find-a-buyer/ \
	$${DOMESTIC_URL}international/ \
	$${DOMESTIC_URL}international/content/about-uk/ \
	$${DOMESTIC_URL}international/invest/ \
	$${DOMESTIC_URL}international/content/capital-invest/ \
	$${DOMESTIC_URL}international/content/trade/how-we-help-you-buy/ \
	$${DOMESTIC_URL}international/content/about-us/ \
	$${DOMESTIC_URL}profile/about/ \
	$${DOMESTIC_URL}sso/accounts/login/ \
	"

PYLINKVALIDATE_ENV_VARS_UAT := \
	export IGNORED_PREFIXES="\
	$${DOMESTIC_URL}international/static/,\
	$${DOMESTIC_URL}find-a-buyer/static/,\
	$${DOMESTIC_URL}profile/static/,\
	$${DOMESTIC_URL}profile/enrol/?next=,\
	$${DOMESTIC_URL}sso/accounts/login/?next,\
	$${DOMESTIC_URL}sso/accounts/password/reset/?next,\
	$${DOMESTIC_URL}sso/accounts/signup/?next,\
	$${DOMESTIC_URL}sso/static/,\
	$${DOMESTIC_URL}static/,\
	$${DOMESTIC_URL}international/trade/search/?term=,\
	$${DOMESTIC_URL}international/trade/static/,\
	$${DOMESTIC_URL}international/trade/suppliers/,\
	$${DOMESTIC_URL}international/invest/static/,\
	$${DOMESTIC_URL}international/investment-support-directory/0,\
	$${DOMESTIC_URL}international/investment-support-directory/O,\
	$${DOMESTIC_URL}international/investment-support-directory/S,\
	$${DOMESTIC_URL}international/investment-support-directory/search/?,\
	$${DOMESTIC_URL}international/investment-support-directory/?q=,\
	$${DOMESTIC_URL}selling-online-overseas/static/,\
	$${DOMESTIC_URL}contact/selling-online-overseas/static/,\
	$${EXPORT_OPPORTUNITIES_URL}assets/,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities?,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/a,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/b,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/c,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/d,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/m,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/f,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/g,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/h,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/j,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/k,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/m,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/n,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/m,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/p,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/r,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/s,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/t,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/w,\
	$${EXPORT_OPPORTUNITIES_URL}opportunities/z,\
	http://www.linkedin.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.facebook.com,\
	https://www.linkedin.com\
	" && \
	export TEST_URLS="\
	$${DOMESTIC_URL} \
	$${DOMESTIC_URL}advice/ \
	$${DOMESTIC_URL}markets/ \
	$${DOMESTIC_URL}services/ \
	$${DOMESTIC_URL}community/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/markets/results/ \
	$${DOMESTIC_URL}find-a-buyer/ \
	$${DOMESTIC_URL}international/ \
	$${DOMESTIC_URL}international/content/about-uk/ \
	$${DOMESTIC_URL}international/invest/ \
	$${DOMESTIC_URL}international/content/capital-invest/ \
	$${DOMESTIC_URL}international/content/trade/how-we-help-you-buy/ \
	$${DOMESTIC_URL}international/content/about-us/ \
	$${DOMESTIC_URL}profile/about/ \
	$${DOMESTIC_URL}sso/accounts/login/ \
	$${EXPORT_OPPORTUNITIES_URL} \
	$${EXPORT_OPPORTUNITIES_URL}opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	"


PYLINKVALIDATE_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="\
	$${DOMESTIC_URL}international/static/,\
	$${DOMESTIC_URL}find-a-buyer/static/,\
	$${DOMESTIC_URL}profile/static/,\
	$${DOMESTIC_URL}profile/enrol/?next=,\
	$${DOMESTIC_URL}sso/accounts/login/?next,\
	$${DOMESTIC_URL}sso/accounts/password/reset/?next,\
	$${DOMESTIC_URL}sso/accounts/signup/?next,\
	$${DOMESTIC_URL}sso/static/,\
	$${DOMESTIC_URL}static/,\
	$${DOMESTIC_URL}international/trade/search/?term=,\
	$${DOMESTIC_URL}international/trade/static/,\
	$${DOMESTIC_URL}international/trade/suppliers/,\
	$${DOMESTIC_URL}international/invest/static/,\
	$${DOMESTIC_URL}international/investment-support-directory/0,\
	$${DOMESTIC_URL}international/investment-support-directory/O,\
	$${DOMESTIC_URL}international/investment-support-directory/S,\
	$${DOMESTIC_URL}international/investment-support-directory/search/?,\
	$${DOMESTIC_URL}international/investment-support-directory/?q=,\
	$${DOMESTIC_URL}selling-online-overseas/static/,\
	$${DOMESTIC_URL}contact/selling-online-overseas/static/,\
	$${DOMESTIC_URL}export-opportunities/opportunities?,\
	$${DOMESTIC_URL}export-opportunities/opportunities/a,\
	$${DOMESTIC_URL}export-opportunities/opportunities/b,\
	$${DOMESTIC_URL}export-opportunities/opportunities/c,\
	$${DOMESTIC_URL}export-opportunities/opportunities/d,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/f,\
	$${DOMESTIC_URL}export-opportunities/opportunities/g,\
	$${DOMESTIC_URL}export-opportunities/opportunities/h,\
	$${DOMESTIC_URL}export-opportunities/opportunities/j,\
	$${DOMESTIC_URL}export-opportunities/opportunities/k,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/n,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/p,\
	$${DOMESTIC_URL}export-opportunities/opportunities/r,\
	$${DOMESTIC_URL}export-opportunities/opportunities/s,\
	$${DOMESTIC_URL}export-opportunities/opportunities/t,\
	$${DOMESTIC_URL}export-opportunities/opportunities/w,\
	$${DOMESTIC_URL}export-opportunities/opportunities/z,\
	$${DOMESTIC_URL}export-opportunities/opportunities?s=,\
	$${DOMESTIC_URL}export-opportunities/opportunities?paged=,\
	$${DOMESTIC_URL}export-opportunities/assets/,\
	http://www.linkedin.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.facebook.com,\
	https://www.linkedin.com\
	" && \
	export TEST_URLS="\
	$${DOMESTIC_URL} \
	$${DOMESTIC_URL}advice/ \
	$${DOMESTIC_URL}markets/ \
	$${DOMESTIC_URL}services/ \
	$${DOMESTIC_URL}community/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/ \
	$${DOMESTIC_URL}contact/selling-online-overseas/markets/results/ \
	$${DOMESTIC_URL}export-opportunities/ \
	$${DOMESTIC_URL}export-opportunities/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	$${DOMESTIC_URL}find-a-buyer/ \
	$${DOMESTIC_URL}international/ \
	$${DOMESTIC_URL}international/content/about-uk/ \
	$${DOMESTIC_URL}international/invest/ \
	$${DOMESTIC_URL}international/content/capital-invest/ \
	$${DOMESTIC_URL}international/content/trade/how-we-help-you-buy/ \
	$${DOMESTIC_URL}international/content/about-us/ \
	$${DOMESTIC_URL}profile/about/ \
	$${DOMESTIC_URL}sso/accounts/login/ \
	"

PYLINKVALIDATE_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="\
	$${DOMESTIC_URL}selling-online-overseas/static/, \
	$${DOMESTIC_URL}find-a-buyer/static/,\
	$${DOMESTIC_URL}profile/static/,\
	$${DOMESTIC_URL}sso/accounts/login/?next,\
	$${DOMESTIC_URL}sso/accounts/password/reset/?next,\
	$${DOMESTIC_URL}sso/accounts/signup/?next,\
	$${DOMESTIC_URL}sso/static/,\
	$${DOMESTIC_URL}static/,\
	$${DOMESTIC_URL}international/static/,\
	$${DOMESTIC_URL}international/trade/search/?term=,\
	$${DOMESTIC_URL}international/trade/static/,\
	$${DOMESTIC_URL}international/trade/suppliers/,\
	$${DOMESTIC_URL}international/invest/static/,\
	$${DOMESTIC_URL}international/investment-support-directory/0,\
	$${DOMESTIC_URL}international/investment-support-directory/O,\
	$${DOMESTIC_URL}international/investment-support-directory/S,\
	$${DOMESTIC_URL}export-opportunities/opportunities/1,\
	$${DOMESTIC_URL}export-opportunities/opportunities/2,\
	$${DOMESTIC_URL}export-opportunities/opportunities/3,\
	$${DOMESTIC_URL}export-opportunities/opportunities/4,\
	$${DOMESTIC_URL}export-opportunities/opportunities/5,\
	$${DOMESTIC_URL}export-opportunities/opportunities/6,\
	$${DOMESTIC_URL}export-opportunities/opportunities/7,\
	$${DOMESTIC_URL}export-opportunities/opportunities/8,\
	$${DOMESTIC_URL}export-opportunities/opportunities/9,\
	$${DOMESTIC_URL}export-opportunities/opportunities/b,\
	$${DOMESTIC_URL}export-opportunities/opportunities/c,\
	$${DOMESTIC_URL}export-opportunities/opportunities/d,\
	$${DOMESTIC_URL}export-opportunities/opportunities/e,\
	$${DOMESTIC_URL}export-opportunities/opportunities/f,\
	$${DOMESTIC_URL}export-opportunities/opportunities/g,\
	$${DOMESTIC_URL}export-opportunities/opportunities/h,\
	$${DOMESTIC_URL}export-opportunities/opportunities/j,\
	$${DOMESTIC_URL}export-opportunities/opportunities/k,\
	$${DOMESTIC_URL}export-opportunities/opportunities/l,\
	$${DOMESTIC_URL}export-opportunities/opportunities/m,\
	$${DOMESTIC_URL}export-opportunities/opportunities/n,\
	$${DOMESTIC_URL}export-opportunities/opportunities/o,\
	$${DOMESTIC_URL}export-opportunities/opportunities/p,\
	$${DOMESTIC_URL}export-opportunities/opportunities/r,\
	$${DOMESTIC_URL}export-opportunities/opportunities/s,\
	$${DOMESTIC_URL}export-opportunities/opportunities/t,\
	$${DOMESTIC_URL}export-opportunities/opportunities/u,\
	$${DOMESTIC_URL}export-opportunities/opportunities/w,\
	$${DOMESTIC_URL}export-opportunities/opportunities/z,\
	$${DOMESTIC_URL}export-opportunities/opportunities?s=,\
	$${DOMESTIC_URL}export-opportunities/opportunities?paged=,\
	$${DOMESTIC_URL}export-opportunities/assets/,\
	http://exportbritain.org.uk/international-directory/,\
	http://www.linkedin.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.facebook.com,\
	https://www.linkedin.com\
	" && \
	export TEST_URLS="\
	$${DOMESTIC_URL} \
	$${DOMESTIC_URL}community/ \
	$${DOMESTIC_URL}export-opportunities/ \
	$${DOMESTIC_URL}international/ \
	$${DOMESTIC_URL}international/trade/ \
	$${DOMESTIC_URL}international/investment-support-directory/ \
	$${DOMESTIC_URL}find-a-buyer/ \
	$${DOMESTIC_URL}sso/accounts/login/ \
	$${DOMESTIC_URL}profile/about/ \
	$${DOMESTIC_URL}international/content/invest/ \
	$${DOMESTIC_URL}selling-online-overseas/ \
	$${DOMESTIC_URL}selling-online-overseas/markets/results/ \
	"

BASIC_AUTH := $(shell echo -n $($(TEST_ENV)_BASICAUTH_USER):$($(TEST_ENV)_BASICAUTH_PASS) | base64)

## Testing Production systems will check outside links
## Testing non-Production systems will not check outside links & HAWK cookie
## will be used.
ifeq ($(TEST_ENV),PROD)
	AUTH=
	TEST_OUTSIDE=--test-outside
else
ifeq ($(TEST_ENV),UAT)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
ifeq ($(TEST_ENV),STAGE)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
ifeq ($(TEST_ENV),DEV)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
endif

dead_links_check:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo -e "Running pylinkvalidate against: $${TEST_URLS}\n" && \
	echo -e "IGNORED_PREFIXES: `echo $${IGNORED_PREFIXES} | tr -d [:space:]`\n" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
	    --types=a,script,link \
	    $(TEST_OUTSIDE) \
	    --parser=lxml \
	    --format=junit \
	    --output="./reports/dead_links_report.xml" \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="Accept-Language: en-GB,en-US;q=0.9,en;q=0.8" \
	    --header="DNT: 1" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    $(AUTH) \
	    --ignore=`echo $${IGNORED_PREFIXES} | tr -d [:space:]` \
	    $${TEST_URLS} || true

dead_links_check_with_json_report:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo -e "Running pylinkvalidate against: $${TEST_URLS}\n" && \
	echo -e "IGNORED_PREFIXES: `echo $${IGNORED_PREFIXES} | tr -d [:space:]`\n" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
	    --types=a,img,link,script \
	    $(TEST_OUTSIDE) \
	    --report-type=all \
	    --parser=lxml \
	    --format=json \
	    --output="./reports/dead_links_report.json" \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="Accept-Language: en-GB,en-US;q=0.9,en;q=0.8" \
	    --header="DNT: 1" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    $(AUTH) \
	    --ignore=`echo $${IGNORED_PREFIXES} | tr -d [:space:]` \
	    $${TEST_URLS} || true
