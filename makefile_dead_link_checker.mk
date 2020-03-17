
# default to TRADE DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

PYLINKVALIDATE_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="\
	https://www.great.gov.uk/profile/static/,\
	https://www.great.gov.uk/sso/accounts/login/,\
	https://www.great.gov.uk/sso/accounts/login/?next=,\
	https://www.great.gov.uk/sso/accounts/password/reset/,\
	https://www.great.gov.uk/sso/accounts/signup/,\
	https://www.great.gov.uk/sso/static/,\
	https://www.great.gov.uk/international/static/,\
	https://www.great.gov.uk/international/trade/search/?term=,\
	https://www.great.gov.uk/international/trade/static/,\
	https://www.great.gov.uk/international/trade/suppliers/,\
	https://www.great.gov.uk/international/invest/static/,\
	https://www.great.gov.uk/international/investment-support-directory/0,\
	https://www.great.gov.uk/international/investment-support-directory/O,\
	https://www.great.gov.uk/international/investment-support-directory/S,\
	https://www.great.gov.uk/international/investment-support-directory/search/?,\
	https://www.great.gov.uk/international/investment-support-directory/?q=,\
	https://www.great.gov.uk/static/,\
	https://cms.trade.great.gov.uk/documents/,\
	https://directory-cms-public.s3.amazonaws.com,\
	https://selling-online-overseas.export.great.gov.uk/static/,\
	https://www.great.gov.uk/export-opportunities/opportunities?paged=,\
	https://www.great.gov.uk/export-opportunities/opportunities/1,\
	https://www.great.gov.uk/export-opportunities/opportunities/2,\
	https://www.great.gov.uk/export-opportunities/opportunities/3,\
	https://www.great.gov.uk/export-opportunities/opportunities/4,\
	https://www.great.gov.uk/export-opportunities/opportunities/5,\
	https://www.great.gov.uk/export-opportunities/opportunities/6,\
	https://www.great.gov.uk/export-opportunities/opportunities/7,\
	https://www.great.gov.uk/export-opportunities/opportunities/8,\
	https://www.great.gov.uk/export-opportunities/opportunities/9,\
	https://www.great.gov.uk/export-opportunities/opportunities/b,\
	https://www.great.gov.uk/export-opportunities/opportunities/c,\
	https://www.great.gov.uk/export-opportunities/opportunities/d,\
	https://www.great.gov.uk/export-opportunities/opportunities/e,\
	https://www.great.gov.uk/export-opportunities/opportunities/f,\
	https://www.great.gov.uk/export-opportunities/opportunities/g,\
	https://www.great.gov.uk/export-opportunities/opportunities/h,\
	https://www.great.gov.uk/export-opportunities/opportunities/j,\
	https://www.great.gov.uk/export-opportunities/opportunities/k,\
	https://www.great.gov.uk/export-opportunities/opportunities/l,\
	https://www.great.gov.uk/export-opportunities/opportunities/m,\
	https://www.great.gov.uk/export-opportunities/opportunities/n,\
	https://www.great.gov.uk/export-opportunities/opportunities/o,\
	https://www.great.gov.uk/export-opportunities/opportunities/p,\
	https://www.great.gov.uk/export-opportunities/opportunities/r,\
	https://www.great.gov.uk/export-opportunities/opportunities/s,\
	https://www.great.gov.uk/export-opportunities/opportunities/t,\
	https://www.great.gov.uk/export-opportunities/opportunities/u,\
	https://www.great.gov.uk/export-opportunities/opportunities/w,\
	https://www.great.gov.uk/export-opportunities/opportunities/z,\
	https://www.great.gov.uk/export-opportunities/opportunities?s=,\
	https://www.great.gov.uk/export-opportunities/opportunities?areas,\
	https://www.great.gov.uk/selling-online-overseas/markets/results/?operating_countries,\
	https://opportunities.export.great.gov.uk/opportunities?paged=,\
	https://opportunities.export.great.gov.uk/opportunities/1,\
	https://opportunities.export.great.gov.uk/opportunities/2,\
	https://opportunities.export.great.gov.uk/opportunities/3,\
	https://opportunities.export.great.gov.uk/opportunities/4,\
	https://opportunities.export.great.gov.uk/opportunities/5,\
	https://opportunities.export.great.gov.uk/opportunities/6,\
	https://opportunities.export.great.gov.uk/opportunities/7,\
	https://opportunities.export.great.gov.uk/opportunities/8,\
	https://opportunities.export.great.gov.uk/opportunities/9,\
	https://opportunities.export.great.gov.uk/opportunities/b,\
	https://opportunities.export.great.gov.uk/opportunities/c,\
	https://opportunities.export.great.gov.uk/opportunities/d,\
	https://opportunities.export.great.gov.uk/opportunities/e,\
	https://opportunities.export.great.gov.uk/opportunities/f,\
	https://opportunities.export.great.gov.uk/opportunities/g,\
	https://opportunities.export.great.gov.uk/opportunities/h,\
	https://opportunities.export.great.gov.uk/opportunities/j,\
	https://opportunities.export.great.gov.uk/opportunities/k,\
	https://opportunities.export.great.gov.uk/opportunities/l,\
	https://opportunities.export.great.gov.uk/opportunities/m,\
	https://opportunities.export.great.gov.uk/opportunities/n,\
	https://opportunities.export.great.gov.uk/opportunities/o,\
	https://opportunities.export.great.gov.uk/opportunities/p,\
	https://opportunities.export.great.gov.uk/opportunities/r,\
	https://opportunities.export.great.gov.uk/opportunities/s,\
	https://opportunities.export.great.gov.uk/opportunities/t,\
	https://opportunities.export.great.gov.uk/opportunities/u,\
	https://opportunities.export.great.gov.uk/opportunities/w,\
	https://opportunities.export.great.gov.uk/opportunities/z,\
	https://opportunities.export.great.gov.uk/opportunities?paged=,\
	https://www.contactus.trade.gov.uk/office-finder/,\
	https://s3.eu-west-2.amazonaws.com/,\
	https://d3zwahhsvfb28.cloudfront.net,\
	https://seao.ca/OpportunityPublication,\
	http://www.linkedin.com,\
	http://ted.europa.eu,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.facebook.com,\
	https://www.facebook.com/login.php,\
	https://www.linkedin.com,\
	https://manaa.esma.gov.ae/,\
	https://www.businessbankinginsight.co.uk/,\
	https://www.pensionledfunding.com/,\
	https://www.dubaicustoms.gov.ae/en\
	" && \
	export TEST_URLS="\
	https://www.great.gov.uk/ \
	https://www.great.gov.uk/community/ \
	https://www.great.gov.uk/contact/ \
	https://www.great.gov.uk/contact/selling-online-overseas/organisation/ \
	https://www.great.gov.uk/find-a-buyer/ \
	https://www.great.gov.uk/get-finance/ \
	https://www.great.gov.uk/sso/accounts/login/ \
	https://www.great.gov.uk/profile/about/ \
	https://www.great.gov.uk/privacy-and-cookies/ \
	https://www.great.gov.uk/international/trade/ \
	https://www.great.gov.uk/international/investment-support-directory/ \
	https://www.great.gov.uk/international/invest/ \
	https://www.great.gov.uk/international/content/invest/high-potential-opportunities/food-production/ \
	https://www.great.gov.uk/international/content/invest/high-potential-opportunities/lightweight-structures/ \
	https://www.great.gov.uk/international/content/invest/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.gov.uk/ \
	https://selling-online-overseas.export.great.gov.uk/ \
	https://selling-online-overseas.export.great.gov.uk/markets/results/ \
	"

PYLINKVALIDATE_ENV_VARS_UAT := \
	export IGNORED_PREFIXES="\
	https://great.uat.uktrade.digital/international/static/,\
	https://great.uat.uktrade.digital/find-a-buyer/static/,\
	https://great.uat.uktrade.digital/profile/static/,\
	https://great.uat.uktrade.digital/sso/accounts/login/?next,\
	https://great.uat.uktrade.digital/sso/accounts/password/reset/?next,\
	https://great.uat.uktrade.digital/sso/accounts/signup/?next,\
	https://great.uat.uktrade.digital/sso/static/,\
	https://great.uat.uktrade.digital/static/,\
	https://great.uat.uktrade.digital/trade/search/?term=,\
	https://great.uat.uktrade.digital/trade/static/,\
	https://great.uat.uktrade.digital/trade/suppliers/,\
	https://invest.great.uat.uktrade.digital/static/,\
	https://opportunities.export.great.uat.uktrade.digital/assets/,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities?,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/a,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/b,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/c,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/d,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/f,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/g,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/h,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/j,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/k,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/n,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/p,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/r,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/s,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/t,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/w,\
	https://opportunities.export.great.uat.uktrade.digital/opportunities/z,\
	https://great.uat.uktrade.digital/contact/selling-online-overseas/static/,\
	https://www.contactus.trade.gov.uk/office-finder,\
	http://www.export.org.uk/page/Market_Selection,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	http://exportbritain.org.uk/international-directory/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.facebook.com,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.uat.uktrade.digital/international/ \
	https://great.uat.uktrade.digital/international/content/industries/ \
	https://great.uat.uktrade.digital/international/content/how-to-setup-in-the-uk/ \
	https://great.uat.uktrade.digital/international/content/how-to-do-business-with-the-uk/ \
	https://great.uat.uktrade.digital/ \
	https://great.uat.uktrade.digital/community \
	https://great.uat.uktrade.digital/trade/ \
	https://great.uat.uktrade.digital/find-a-buyer/ \
	https://great.uat.uktrade.digital/sso/accounts/login/ \
	https://great.uat.uktrade.digital/profile/about/ \
	https://great.uat.uktrade.digital/contact/selling-online-overseas/ \
	https://great.uat.uktrade.digital/contact/selling-online-overseas/markets/results/ \
	https://invest.great.uat.uktrade.digital/ \
	https://invest.great.uat.uktrade.digital/high-potential-opportunities/lightweight-structures/ \
	https://invest.great.uat.uktrade.digital/high-potential-opportunities/food-production/ \
	https://invest.great.uat.uktrade.digital/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.uat.uktrade.digital/ \
	https://opportunities.export.great.uat.uktrade.digital/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	"


PYLINKVALIDATE_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="\
	https://great.staging.uktrade.digital/international/static/,\
	https://great.staging.uktrade.digital/find-a-buyer/static/,\
	https://great.staging.uktrade.digital/profile/static/,\
	https://great.staging.uktrade.digital/profile/enrol/?next=,\
	https://great.staging.uktrade.digital/sso/accounts/login/?next,\
	https://great.staging.uktrade.digital/sso/accounts/password/reset/?next,\
	https://great.staging.uktrade.digital/sso/accounts/signup/?next,\
	https://great.staging.uktrade.digital/sso/static/,\
	https://great.staging.uktrade.digital/static/,\
	https://great.staging.uktrade.digital/international/trade/search/?term=,\
	https://great.staging.uktrade.digital/international/trade/static/,\
	https://great.staging.uktrade.digital/international/trade/suppliers/,\
	https://great.staging.uktrade.digital/international/invest/static/,\
	https://great.staging.uktrade.digital/international/investment-support-directory/0,\
	https://great.staging.uktrade.digital/international/investment-support-directory/O,\
	https://great.staging.uktrade.digital/international/investment-support-directory/S,\
	https://great.staging.uktrade.digital/international/investment-support-directory/search/?,\
	https://great.staging.uktrade.digital/international/investment-support-directory/?q=,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities?,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/a,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/b,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/c,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/d,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/f,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/g,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/h,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/j,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/k,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/n,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/p,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/r,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/s,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/t,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/w,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities/z,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities?s=,\
	https://great.staging.uktrade.digital/export-opportunities/opportunities?paged=,\
	https://great.staging.uktrade.digital/export-opportunities/assets/,\
	https://great.staging.uktrade.digital/selling-online-overseas/static/,\
	https://great.staging.uktrade.digital/contact/selling-online-overseas/static/,\
	https://www.contactus.trade.gov.uk/office-finder,\
	http://www.export.org.uk/page/Market_Selection,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	http://exportbritain.org.uk/international-directory/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.facebook.com,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.staging.uktrade.digital/international/ \
	https://great.staging.uktrade.digital/international/trade/ \
	https://great.staging.uktrade.digital/international/investment-support-directory/ \
	https://great.staging.uktrade.digital/international/content/industries/ \
	https://great.staging.uktrade.digital/international/content/how-to-setup-in-the-uk/ \
	https://great.staging.uktrade.digital/ \
	https://great.staging.uktrade.digital/community \
	https://great.staging.uktrade.digital/find-a-buyer/ \
	https://great.staging.uktrade.digital/sso/accounts/login/ \
	https://great.staging.uktrade.digital/profile/about/ \
	https://great.staging.uktrade.digital/contact/selling-online-overseas/ \
	https://great.staging.uktrade.digital/contact/selling-online-overseas/markets/results/ \
	https://great.staging.uktrade.digital/international/invest/ \
	https://great.staging.uktrade.digital/international/content/invest/high-potential-opportunities/lightweight-structures/ \
	https://great.staging.uktrade.digital/international/content/invest/high-potential-opportunities/food-production/ \
	https://great.staging.uktrade.digital/international/content/invest/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.staging.uktrade.digital/ \
	https://opportunities.export.great.staging.uktrade.digital/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	"

PYLINKVALIDATE_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="\
	https://great.dev.uktrade.digital/find-a-buyer/static/,\
	https://great.dev.uktrade.digital/profile/static/,\
	https://great.dev.uktrade.digital/sso/accounts/login/?next,\
	https://great.dev.uktrade.digital/sso/accounts/password/reset/?next,\
	https://great.dev.uktrade.digital/sso/accounts/signup/?next,\
	https://great.dev.uktrade.digital/sso/static/,\
	https://great.dev.uktrade.digital/static/,\
	https://great.dev.uktrade.digital/international/static/,\
	https://great.dev.uktrade.digital/international/trade/search/?term=,\
	https://great.dev.uktrade.digital/international/trade/static/,\
	https://great.dev.uktrade.digital/international/trade/suppliers/,\
	https://great.dev.uktrade.digital/international/invest/static/,\
	https://great.dev.uktrade.digital/international/investment-support-directory/0,\
	https://great.dev.uktrade.digital/international/investment-support-directory/O,\
	https://great.dev.uktrade.digital/international/investment-support-directory/S,\
	https://selling-online-overseas.export.great.dev.uktrade.digital/static/,\
	http://exportbritain.org.uk/international-directory/,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/1,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/2,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/3,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/4,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/5,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/6,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/7,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/8,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/9,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/b,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/c,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/d,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/e,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/f,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/g,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/h,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/j,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/k,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/l,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/m,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/n,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/o,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/p,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/r,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/s,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/t,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/u,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/w,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities/z,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities?s=,\
	https://great.dev.uktrade.digital/export-opportunities/opportunities?paged=,\
	https://great.dev.uktrade.digital/export-opportunities/assets/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.export.org.uk/page/Market_Selection,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.contactus.trade.gov.uk,\
	https://www.facebook.com,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,\
	https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.dev.uktrade.digital/ \
	https://great.dev.uktrade.digital/community/ \
	https://great.dev.uktrade.digital/export-opportunities/ \
	https://great.dev.uktrade.digital/international/ \
	https://great.dev.uktrade.digital/international/trade/ \
	https://great.dev.uktrade.digital/international/investment-support-directory/ \
	https://great.dev.uktrade.digital/find-a-buyer/ \
	https://great.dev.uktrade.digital/sso/accounts/login/ \
	https://great.dev.uktrade.digital/profile/about/ \
	https://great.dev.uktrade.digital/international/content/invest/ \
	https://great.dev.uktrade.digital/selling-online-overseas/ \
	https://great.dev.uktrade.digital/selling-online-overseas/markets/results/ \
	"

BASIC_AUTH := $(shell echo -n $($(TEST_ENV)_BASICAUTH_USER):$($(TEST_ENV)_BASICAUTH_PASS) | base64)

# Testing Production systems will check outside links
# Testing non-Production systems will not check outside links & HAWK cookie
# will be used.
ifndef DEV_BASICAUTH_USER
  $(error DEV_BASICAUTH_USER is undefined)
endif
ifndef DEV_BASICAUTH_PASS
  $(error DEV_BASICAUTH_PASS is undefined)
endif
ifndef STAGE_BASICAUTH_USER
  $(error STAGE_BASICAUTH_USER is undefined)
endif
ifndef STAGE_BASICAUTH_PASS
  $(error STAGE_BASICAUTH_PASS is undefined)
endif
ifndef UAT_BASICAUTH_USER
  $(error UAT_BASICAUTH_USER is undefined)
endif
ifndef UAT_BASICAUTH_PASS
  $(error UAT_BASICAUTH_PASS is undefined)
endif

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
