DIRECTORY Header & Footer Visuall Diff tests
--------------------------------------------

## Run containers with headless browsers

```bash
docker run -d -p 4444:4444 --name selenium-hub selenium/hub:3.6.0-bromine
docker run -d -v /dev/shm:/dev/shm --name selenium-hub-chrome --link selenium-hub:hub selenium/node-chrome:3.6.0-bromine
docker run -d --shm-size 2g --name selenium-hub-firefox --link selenium-hub:hub selenium/node-firefox:3.6.0-bromine
docker run -d -e PHANTOMJS_OPTS="--ignore-ssl-errors=true" --name selenium-hub-phantomjs --link selenium-hub:hub selenium/node-phantomjs:3.6.0-bromine
```

## Generate baseline images for specific browser
```bash
BROWSER=chrome nosetests -s tests/ui/header-footer-test.py --with-save-baseline
BROWSER=firefox nosetests -s tests/ui/header-footer-test.py --with-save-baseline
BROWSER=phantomjs nosetests -s tests/ui/header-footer-test.py --with-save-baseline
```

## Run all tests against baseline images for specific browser
```bash
BROWSER=chrome nosetests -s tests/ui/header-footer-test.py
BROWSER=firefox nosetests -s tests/ui/header-footer-test.py
BROWSER=phantomjs nosetests -s tests/ui/header-footer-test.py
```

## Viewing container logs
```bash
docker logs -f --tail 10 selenium-hub-phantomjs
```
