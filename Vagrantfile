Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-22.04"
    config.vm.network "forwarded_port", guest:30080, host:8080, auto_correct: true
    config.vm.network "forwarded_port", guest: 30081, host: 30081, auto_correct: true
    config.vm.synced_folder ".", "/vagrant", type: "rsync"

    config.vm.provider "virtualbox" do |vb|
        vb.cpus = 2
        vb.memory = 3072
    end

    config.vm.provision "shell", inline: <<-SHELL
        sudo apt-get update -y
        sudo apt-get install -y ca-certificates curl gnupg python3 python3-pip python3-venv
        
        #Install and configure Docker
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc

        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
            $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update -y
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        sudo usermod -aG docker vagrant
        
        #install K3s
        curl -sfL https://get.k3s.io | sh -

        # Wait for K3s to be ready
        echo "Waiting for K3s to be ready..."
        until sudo k3s kubectl get nodes 2>/dev/null; do
            sleep 5
        done
        echo "K3s is ready!"

        # Setup kubeconfig permissions
        sudo chmod 644 /etc/rancher/k3s/k3s.yaml

        # Setup ArgoCD
        kubectl create namespace argocd
        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

        # Wait for ArgoCD server pod to be ready
        echo "Waiting for ArgoCD to be ready (this takes 2-3 minutes)..."
        kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
        echo "ArgoCD is ready!"

        #Patch the service to Nodeport
        kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort", "ports": [{"port" : 443, "nodePort" : 30081, "name" : "https"}]}}'
    SHELL
end