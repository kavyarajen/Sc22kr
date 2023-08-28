faas-cli new mongo-to-blob --lang python3-flask-debian
faas-cli new blob-to-pg --lang python3-flask-debian
faas-cli new run1 --lang python3-flask-debian

mv mongo-to-blob.py ./mongo-to-blob/handler.py
mv blob-to-pg ./blob-to-pg/handler.py
mv run1 ./run1/handler.py

sed -i 's/image: mongo-to-blob:latest/image: sc22kr\/mongo-to-blob:latest/g' mongo-to-blob.yml
sed -i 's/image: blob-to-pg:latest/image: sc22kr\/blob-to-pg:latest/g' blob-to-pg.yml
sed -i 's/image: run1:latest/image: sc22kr\/run1:latest/g' run1.yml

faas-cli up -f mongo-to-blob.yml
faas-cli up -f blob-to-pg.yml
faas-cli up -f run1.yml

