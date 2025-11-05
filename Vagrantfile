Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-22.04"
    config.vm.network "forwarded_port", guest:30080, host:8080, auto_correct: true
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

        # Setup kubeconfig
        sudo mkdir -p /home/vagrant/.kube
        sudo cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
        sudo chown -R vagrant:vagrant /home/vagrant/.kube
    SHELL
end