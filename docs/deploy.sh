

pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

pybabel init -i messages.pot -d app/translations -l es

pybabel compile -d app/translations




pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
pybabel update -i messages.pot -d app/translations

