curl -sLS https://get.arkade.dev | sudo sh
arkade get kubectl
echo "export PATH=$PATH:$HOME/.arkade/bin/" >> ~/.bashrc
source ~/.bashrc
arkade get kind
arkade get faas-cli
arkade install openfaas
kubectl get pods -n openfaas
faas-cli new testing --lang node14
faas-cli build -f testing.yml
export OPENFAAS_URL=http://127.0.0.1:8080/
export OPENFAAS_PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
faas-cli login --gateway=$OPENFAAS_URL --password=$OPENFAAS_PASSWORD
echo $OPENFAAS_PASSWORD