Measure contingency of service unavailability
---------------------------------------------

This simple script analyse a "[Dead link checker](../../../README.md#Dead-link-checker)" JSON report file and generates a simple service contingency report.  
The report will give you a rough estimation of how unavailability of one service would affect other Great.gov.uk services.

First you need to run a `Dead link checker` with an option to generate a JSON report:

```bash
source ~/dev.sh;
make dead_links_check_with_json_report
```

As a result a JSON report file will be saved in `./reports/dead_links_report.json`.

Then run `make service_contingency_report` to generate a simple service contingency report.

Below is an example report:

```shell
Number of unique links (without links to static files, translations and queries), per service, scanned by Dead Links Checker:
If a link contains any of following strings: /static/, ?source=, ?lang=, /ar/, /de/, /es/, /fr/, /ja/, /pt/, /zh-hans/ then it won't be included in the contingency report
SSO            :    42 - (excluding    0 ignored links)
SUD            :    46 - (excluding    0 ignored links)
FAB            :     1 - (excluding    0 ignored links)
Great          :  1898 - (excluding    0 ignored links)
FAS            :     3 - (excluding    6 ignored links)
Invest         :     3 - (excluding   14 ignored links)
SOO            :    47 - (excluding    0 ignored links)
ExOpps         :    11 - (excluding    0 ignored links)
Other          :    19 - (excluding    0 ignored links)
Contact        :     4 - (excluding    0 ignored links)
Ignored links  : 20
Total          : 2094 (2074+20)

Service contingency report:
If FAB (https://great.dev.uktrade.digital/find-a-buyer/) was down then if would affect:
         1 pages on Great
If Great (https://great.dev.uktrade.digital/) was down then if would affect:
        19 pages on Other
If FAS (https://great.dev.uktrade.digital/international/trade/) was down then if would affect:
       507 pages on Great
         6 pages on Invest
If Invest (https://great.dev.uktrade.digital/international/invest/) was down then if would affect:
       507 pages on Great
         6 pages on FAS
If SOO (https://great.dev.uktrade.digital/selling-online-overseas/) was down then if would affect:
         5 pages on Great
If SUD (https://great.dev.uktrade.digital/profile/) was down then if would affect:
        42 pages on SSO
If ExOpps (https://great.dev.uktrade.digital/export-opportunities/) was down then if would affect:
         1 pages on Great
If SSO (https://great.dev.uktrade.digital/sso/) was down then if would affect:
         3 pages on SUD
        38 pages on SOO
If Contact (https://great.dev.uktrade.digital/contact/) was down then if would affect:
       375 pages on Great
         2 pages on FAB
        42 pages on SOO
         4 pages on Invest
         4 pages on FAS
         2 pages on Other
         3 pages on ExOpps
         2 pages on SUD
         1 pages on SSO
```
