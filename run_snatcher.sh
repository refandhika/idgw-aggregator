#!/bin/bash

cd /home/refandhika/snatcher

source venv/bin/activate

cd snatcher/snatcher

scrapy crawl kotakgame

scrapy crawl duniagames

scrapy crawl gamebrott

deactivate

