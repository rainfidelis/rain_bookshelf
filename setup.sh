pip3 install flask_sqlalchemy
pip3 install flask_cors
pip3 install flask --upgrade
pip3 uninstall flask-socketio -y
service postgresql start
su - postgres bash -c "psql < C:/Users/RAIN/PycharmProjects/bookshelf_api/backend/setup.sql"
su - postgres bash -c "psql bookshelf < C:/Users/RAIN/PycharmProjects/bookshelf_api/backend/books.psql"